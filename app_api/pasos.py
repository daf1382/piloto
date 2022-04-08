from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from django.db.models import Max, Q
import io, csv, pandas as pd
import numpy as np
#import datetime as dt
from datetime import datetime as dt
import django_excel as excel
from app_api.models import  File, MOB_T_SEC_PROCESS, MOB_T_SEC_PROCESS_AUDIT, MOB_T_SEC_PROCESS_DOC,MOB_T_ALERT 
from app_api.models import MOB_T_OPERATION, MOB_T_PORTFOLIO, MOB_T_TRANCHE, MOB_T_FX,MOB_T_RATING
from app_api.data_process  import processing_data_for_db
from app_api.utils.services import processing_services as ps



def mid(s, offset, amount):
    return s[offset:offset+amount]


class processing_steps:  
    def paso_0(process_id):
        proceso_actual = MOB_T_SEC_PROCESS.objects.get(id=process_id)
        proceso_anterior = MOB_T_SEC_PROCESS.objects.filter(MONTH=proceso_actual.MONTH - 1).filter(YEAR=proceso_actual.YEAR)[0]
        # Acción 1.1:  SAN_DRAWN_CCY(t-1) mayor que SAN_DRAWN_CCY(t) y Protection Type= SRT 
        ### claculo los no SRT 


 
        extrac_1 = MOB_T_OPERATION.objects.filter(PROTECTION_TYPE="SRT",ID_SEC_PROCESS=proceso_actual.id)    #mes actual (ma)
        for ma in extrac_1:
            mant=MOB_T_OPERATION.objects.filter(LOAN=ma.LOAN,ID_SEC_PROCESS=proceso_anterior.id)[0]  #Mes anterior (mant)
            fx_mesant = MOB_T_FX.objects.filter(COUNTERVALUE=ma.CCY,ID_SEC_PROCESS=proceso_anterior.id)[0]
            fx_mes = MOB_T_FX.objects.filter(COUNTERVALUE=ma.CCY,ID_SEC_PROCESS=proceso_actual.id)[0]         
            if str(mant.PROTECTION_TYPE)=="SRT" and np.array(mant.SAN_DRAWN_CCY) != 0 and np.array(mant.SAN_DRAWN_CCY) > np.array(ma.SAN_DRAWN_CCY):
                #Acción 1.1 RONA_ccy: (drawn_ccy (t-1)-drawn_ccy (t))/drawn_ccy(t-1)*RONA_ccy(t-1)
                RONA_ccy = np.array(ma.SAN_DRAWN_CCY) / np.array(mant.SAN_DRAWN_CCY)  * np.array(mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY)
                ma.PROTECTION_TYPE = "SRT" if mant.SAN_DRAWN_CCY !=0 and mant.PROTECTION_TYPE == "SRT" else ""
            else:   #SI NO ES NECESARIO AJUSTE
                RONA_ccy = np.array(mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY) if mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY!=None  else 0 
                RONA_eur = np.array(mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY) * np.array(fx_mes.EUR)   if mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY!=None  else 0
                ma.PROTECTION_TYPE = mant.PROTECTION_TYPE  if mant.PROTECTION_TYPE!=None  else ""
            
            #Acción 1.2 RONA_ccy_FX_Corrected= RONA_ccy(t)*FX(t-1)/FX(t)
            if np.array(fx_mes.EUR) != 0:
                RONA_ccy_fix = min(RONA_ccy * (np.array(fx_mesant.EUR)) / np.array(fx_mes.EUR),RONA_ccy) 
                RONA_eur = (RONA_ccy_fix * np.array(fx_mes.EUR)) 
                if  ma.LOAN=="LO 0009":
                    print("LO 0009:","rona:",RONA_ccy_fix,"conv:",RONA_eur)
            else:
                RONA_eur = 0  
            ma.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY= RONA_ccy_fix    
            ma.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR= RONA_eur
            ma.save()
            #Acción 1.3 PP_ID
            if RONA_eur==0:   #"Se generará una alerta al Portfolio Manager y indicando la operación amortizada en su totalidad"  
                alert =MOB_T_ALERT.objects.create(ID_MD=proceso_actual.id, ID_SEC_PROCESS=proceso_actual.id, ID_ENTITY=ma.LOAN, COD_ALERT_TYPE="SPS_001",  
                NOTES="Operación amortizada en su totalidad", CREATED_BY ="Daniel" ,  CREATED_ON=str(dt.now()),   
                UPDATED_BY="Daniel",  UPDATED_ON=str(dt.now()), ACTIVE=1) 
                alert.save()
            else:    # "Se generará una alerta al Portfolio Manager y indicando la operación  ha sido parcialmente amortizada"
                alert =MOB_T_ALERT.objects.create(ID_MD=proceso_actual.id, ID_SEC_PROCESS=proceso_actual.id, ID_ENTITY=ma.LOAN, COD_ALERT_TYPE="SPS_001",  
                NOTES="Operación  ha sido parcialmente amortizada", CREATED_BY ="Daniel" ,  CREATED_ON=str(dt.now()),   
                UPDATED_BY="Daniel",  UPDATED_ON=str(dt.now()), ACTIVE=1) 
                alert.save()
        respuesta="paso_0_proceso:" + str(proceso_actual.id) + "_ok"
        return respuesta
        
    def paso_1(process_id,fecha_del_calculo):
        proceso_actual = MOB_T_SEC_PROCESS.objects.get(id=process_id)
        proceso_anterior = MOB_T_SEC_PROCESS.objects.filter(MONTH=proceso_actual.MONTH - 1).filter(YEAR=proceso_actual.YEAR)[0]
        fecha_del_calculo = dt.strptime(fecha_del_calculo, '%Y-%m-%d')
        extrac_operation = MOB_T_OPERATION.objects.filter(PROTECTION_TYPE="SRT",ID_SEC_PROCESS=proceso_actual.id,CREDIT_EVENT="Failure to Pay")        
        extrac_porfolio = MOB_T_PORTFOLIO.objects.filter(ID_SEC_PROCESS=proceso_actual.id)
        portfolio_loss_balance=0
        portfolio_adjusted_loss_balance=0
        for o in extrac_operation:
 
        #PASO 1
        #MIN( drawn_eur de la operación con el credit_event="failure to pay"; RONA_eur de la operación con el credit_event="failure to pay")        
            defaulted_amount=min(o.SAN_DRAWN_EUR,o.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR)    
            Replenishment_Period=None      
            for p in extrac_porfolio:
                replenishment_ini_d = dt.strptime(p.REPLENISHMENT_INI, '%Y-%m-%d')
                replenishment_end_d = dt.strptime(p.REPLENISHMENT_END, '%Y-%m-%d')
                if fecha_del_calculo >= replenishment_ini_d and  fecha_del_calculo <= replenishment_end_d:
                    Replenishment_Period = "Yes"
                else:
                    Replenishment_Period = "No"
            print("paso 1: Replenishment_Period:",Replenishment_Period)
            print("paso 1: defaulted_amount:",defaulted_amount)

        #PASO 2
        #Acción 2.1  Alertar al Portfolio Manager de que se ha detectado un evento de crédito                    FALTA
        # Acción 2.2  Cálculo de la perdida Inicial: Initial_Loss= LGD*Defaulted_amount     
            initial_loss = defaulted_amount * o.LGD
            print("Acción 2.2: initial_loss:",initial_loss)
            o.STP_INICIAL_LOSS  = initial_loss
        # Acción 2.3  Cálculo de la pérdida máxima: Max_Loss= Defaulted_amount- Initial_Loss
            max_Loss = defaulted_amount - initial_loss
            print("Acción 2.3 : max_Loss:",max_Loss)
            o.STP_MAX_LOSS = max_Loss
        # Acción 2.4  Cálculo de las recuperaciones totales: Total_Recoveries=Recoveries*(defaulted_amount)
            total_Recoveries = defaulted_amount * o.RECOVERIES
            print("Acción 2.4: total_Recoveries:",total_Recoveries)
            o.STP_TOTAL_RECOVERIES = total_Recoveries

        # Acción 2.5  Cálculo de la perdida final:IF (Final_Loss_%<>"") THEN: Final_Loss= Final_Loss_% * RONA_Eur    
        #              IF (Final_Loss_%<>"") THEN: Final_Loss= ""

            if np.array(o.FINAL_LOSS) != 0 and np.array(o.FINAL_LOSS) != None  and np.array(o.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR) != 0:                
                final_loss = np.array(o.FINAL_LOSS) * np.array(o.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR)
                print("Acción 2.5 final_loss:",final_loss)
                o.FINAL_LOSS = final_loss
            else:
                final_loss = 0
                print("Acción 2.5 no se calculo, final_loss es igual a ",np.array(o.FINAL_LOSS))
                o.FINAL_LOSS = final_loss
         

        # Acción 2.6   Cálculo del Credit Protection Adjustment Amount: IF Final_Loss <> "" Then: Credit_Protection_Adjustment_Amount=Final_Loss- Initial_Loss  
        #              IF Final_Loss = "" Then: Credit_Protection_Adjustment_Amount=""      
            if final_loss != 0:
                credit_Protection_Adjustment_Amount= final_loss - initial_loss
                print("Acción 2.6:",credit_Protection_Adjustment_Amount)
                o.STP_CREDIT_PROTECTION_ADJUSTMENT_AMOUNT = credit_Protection_Adjustment_Amount
            else:
                credit_Protection_Adjustment_Amount = 0
                o.STP_CREDIT_PROTECTION_ADJUSTMENT_AMOUNT = credit_Protection_Adjustment_Amount
                print("Acción 2.6: no se calculo credit_Protection_Adjustment_Amount=0 porque final_loss es igual a 0")

        # Acción 2.7   Cálculo del Verified Adjusted Amount: Verified_Adjusted_Amount=IF(Credit_Protection_Verification_report_issued_Y_N= "YES; Credit_Protection_Adjustment_Amount;0)
        #              La fecha en la que este campo deja de ser 0 se incluirá en el campo workout_date
            if o.CREDIT_PROTECTION_VERIF_REPORT =="YES" and o.STP_CREDIT_PROTECTION_ADJUSTMENT_AMOUNT !=0:
                verified_Adjusted_Amount= o.STP_CREDIT_PROTECTION_ADJUSTMENT_AMOUNT

            else:
                verified_Adjusted_Amount = 0
            print("Acción 2.7: verified_Adjusted_Amount::", verified_Adjusted_Amount)
            o.STP_VERIFIED_ADJUSTMENT_AMOUNT = verified_Adjusted_Amount
        o.save()
    #Acción 2.8  Cálculo del  Portfolio_Loss_ Balance y Loss_ Balance (a nivel tramo)
                #Cálculo del  Portfolio_Loss_ Balance =  SumIFS(Initial_loss; Initial_ Loss_ Verification_Report_Y_N_NA="YES"; Date_Credit_Event_Verification_Report <="D") + (Verified_Adjustement_amount)
                #Loss_Balance = MIN(Portfolio_Loss_ Balance  - ∑(Loss_Balance del tramos con > Tranche seniority) ;initial_tranche_notional - Cumulative_Amortization_Amount_Tranche)

        if o.INITIAL_LOSS_VERIF_REPORT_RESULT =="YES": # ARREGLAR LA BD CON LA FECHA #and  dt.strptime(o.DATE_CREDIT_EVENT_VERIF_REPORT, '%Y-%m-%d') <= fecha_del_calculo:  #si Initial_Loss_Verification_Report_Y_N_NA es igual a yes
            portfolio_loss_balance= portfolio_loss_balance + o.STP_INICIAL_LOSS +  o.STP_VERIFIED_ADJUSTMENT_AMOUNT
        print("Acción 2.8: portfolio_loss_balance: ",portfolio_loss_balance)
            

        t3 = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =3,ID_SEC_PROCESS=proceso_actual.id)[0]
        t3_ant = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =3,ID_SEC_PROCESS=proceso_anterior.id)[0]

        seniority3= min(portfolio_loss_balance, (t3_ant.CLASS_NOTIONAL  - t3_ant.AMORTISATION_AMOUNT)) if t3_ant.CLASS_NOTIONAL!=None  and t3_ant.AMORTISATION_AMOUNT!=None else 0 #Initial Class Notional- Amortisation Amount
        print("Acción 2.8  Loss_Balance TRANCHE_SENIORITY 3",seniority3)
        t3.LOSS_BALANCE=seniority3
        t3.save()


        t2 = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =2,ID_SEC_PROCESS=proceso_actual.id)[0]
        t2_ant = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =2,ID_SEC_PROCESS=proceso_anterior.id)[0]

        seniority2= min((portfolio_loss_balance-seniority3),(t2_ant.CLASS_NOTIONAL  - t2_ant.AMORTISATION_AMOUNT) ) if t2_ant.CLASS_NOTIONAL!=None  and t2_ant.AMORTISATION_AMOUNT!=None else 0 #Initial Class Notional- Amortisation Amount
        print("Acción 2.8   Loss_Balance TRANCHE_SENIORITY 2",seniority2)
        t2.LOSS_BALANCE=seniority2
        t2.save()

        t1 = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =1,ID_SEC_PROCESS=proceso_actual.id)[0]
        t1_ant = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =1,ID_SEC_PROCESS=proceso_anterior.id)[0]

        seniority1= min((portfolio_loss_balance-seniority3-seniority2),(t1_ant.CLASS_NOTIONAL  - t1_ant.AMORTISATION_AMOUNT) )  if t1_ant.CLASS_NOTIONAL!=None  and t1_ant.AMORTISATION_AMOUNT!=None else 0 #Initial Class Notional- Amortisation Amount
        print("Acción 2.8  Loss_Balance TRANCHE_SENIORITY 1",seniority1)
        t1.LOSS_BALANCE=seniority1
        t1.save()
    #Acción 2.9  Cálculo del  Portfolio_Adjusted_Loss_ Balance y Adjusted_Loss_ Balance (a nivel tramo)
                #Cálculo del  Portfolio_Adjusted_Loss_ Balance = SUMIFS( Max_Loss; (Verified_Adjustement_amount <>0)+ Porfolio_Loss_Balance
                #Adjusted_Loss_Balance = MIN(Portfolio_Adjusted_Loss_ Balance ∑(Loss_Balance del tramos con > Tranche seniority); initial_tranche_notional - Cumulative_Amortization_Amount_Tranche)


        portfolio_adjusted_loss_balance = portfolio_adjusted_loss_balance  + o.STP_INICIAL_LOSS +  o.STP_VERIFIED_ADJUSTMENT_AMOUNT   + portfolio_loss_balance
        print("Acción 2.9: portfolio_adjusted_loss_balance: ",portfolio_adjusted_loss_balance)
        

        t3 = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =3,ID_SEC_PROCESS=proceso_actual.id)[0]
        t3_ant = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =3,ID_SEC_PROCESS=proceso_anterior.id)[0]

        seniority3= min(portfolio_adjusted_loss_balance, (t3_ant.CLASS_NOTIONAL  - t3_ant.AMORTISATION_AMOUNT)) if t3_ant.CLASS_NOTIONAL!=None  and t3_ant.AMORTISATION_AMOUNT!=None else 0 #Initial Class Notional- Amortisation Amount
        print("Acción 2.9  adjusted_loss_balance TRANCHE_SENIORITY 3",seniority3)
        t3.LOSS_BALANCE=seniority3
        t3.save()


        t2 = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =2,ID_SEC_PROCESS=proceso_actual.id)[0]
        t2_ant = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =2,ID_SEC_PROCESS=proceso_anterior.id)[0]

        seniority2= min((portfolio_adjusted_loss_balance-seniority3),(t2_ant.CLASS_NOTIONAL  - t2_ant.AMORTISATION_AMOUNT) ) if t2_ant.CLASS_NOTIONAL!=None  and t2_ant.AMORTISATION_AMOUNT!=None else 0 #Initial Class Notional- Amortisation Amount
 #       print("Acción 2.9   adjusted_loss_balance TRANCHE_SENIORITY 2",seniority2)
        t2.LOSS_BALANCE=seniority2
        t2.save()

        t1 = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =1,ID_SEC_PROCESS=proceso_actual.id)[0]
        t1_ant = MOB_T_TRANCHE.objects.filter(TRANCHE_SENIORITY =1,ID_SEC_PROCESS=proceso_anterior.id)[0]

        seniority1= min((portfolio_adjusted_loss_balance-seniority3-seniority2),(t1_ant.CLASS_NOTIONAL  - t1_ant.AMORTISATION_AMOUNT) )  if t1_ant.CLASS_NOTIONAL!=None  and t1_ant.AMORTISATION_AMOUNT!=None else 0 #Initial Class Notional- Amortisation Amount
        print("Acción 2.9  adjusted_loss_balance TRANCHE_SENIORITY 1",seniority1)
        t1.LOSS_BALANCE=seniority1
        t1.save()
        respuesta="paso_1_proceso:" + str(proceso_actual.id) + " FechaCalculo:" + str(fecha_del_calculo) + "_ok"
        return respuesta


    def paso_3(process_id,fecha_del_calculo):
        proceso_actual = MOB_T_SEC_PROCESS.objects.get(id=process_id)
        proceso_anterior = MOB_T_SEC_PROCESS.objects.filter(MONTH=proceso_actual.MONTH - 1).filter(YEAR=proceso_actual.YEAR)[0]
        extrac_1 = MOB_T_OPERATION.objects.filter(ID_SEC_PROCESS=proceso_actual.id)    #mes actual (ma)
        for ma in extrac_1:
            mant=MOB_T_OPERATION.objects.filter(LOAN=ma.LOAN,ID_SEC_PROCESS=proceso_anterior.id)[0]  #Mes anterior (mant)
            fx_mesant = MOB_T_FX.objects.filter(COUNTERVALUE=ma.CCY,ID_SEC_PROCESS=proceso_anterior.id)[0]
            fx_mes = MOB_T_FX.objects.filter(COUNTERVALUE=ma.CCY,ID_SEC_PROCESS=proceso_actual.id)[0]

        #PASO 3
        # Acción 3.1  Importe retenido  

            temp1=0
            if ma.PROTECTION_TYPE!="SRT":
                temp1=(ps.verfloat(mant.RETENTION_REQUERIMENT)) * ps.verfloat(mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR) 
                
            
            temp2=0
            if mant.PROTECTION_TYPE!="SRT":    #cambiar
              temp2=(ps.verfloat(ma.RETENTION_REQUERIMENT) * ps.verfloat(ma.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR))

            ronacal=ps.verfloat(ma.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR) + ps.verfloat(mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR)

            retention_amount= ps.verfloat(mant.SAN_DRAWN_EUR) - ronacal - temp1 - temp2
            ma.STP_RETENTION_AMOUNT = retention_amount

            if ma.LOAN=='LO 0001':
                print(ma.LOAN,"SAN_DRAW", mant.SAN_DRAWN_EUR, "-rona:",ronacal, "temp1",temp1, "-temp2",temp2, " =retention_amount:",retention_amount)
            ma.save()
     
        # Acción 3.2  % retenido 


            retention_amount_perc= ps.verfloat(retention_amount) / ps.verfloat(mant.SAN_DRAWN_EUR) if ps.verfloat(mant.SAN_DRAWN_EUR)!=0 else 0
            ma.STP_RETENTION_PERC = retention_amount
 #           print(ma.LOAN," STP_RETENTION_PERC:",retention_amount_perc)
            ma.save()

        # Acción 3.3  Free_amount 

            free_amount= ps.verfloat(mant.SAN_DRAWN_EUR) - (ps.verfloat(mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR)  - ps.verfloat(ma.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR)) 
            ma.STP_FREE_AMOUNT = free_amount
#            print(ma.LOAN," free_amount:",free_amount)
            ma.save()
         # Acción 3.4  Internal Rating
        #    print(ma.PD)
            rating = MOB_T_RATING.objects.filter(PD_RATING=ma.PD)
            numero=0
            for ra in rating:
                numero=numero+1
                if numero<2:
                    print(numero,"LOAN:",ma.LOAN,"PD:",ma.PD,"rating pd:",ra.PD_RATING ,"rating",ra.INTERNAL_RATING)
                    ma.STP_INTERNAL_RATING=ra.INTERNAL_RATING
            ma.save()                




        respuesta="paso_3_proceso:" + str(proceso_actual.id) + " FechaCalculo:" + str(fecha_del_calculo) + "_ok"
        return respuesta





from app_api.models import  MOB_T_SEC_PROCESS, File, MOB_T_ALERT,MOB_T_OPERATION #  Account, Portfolio, Tramos, FX
from django.db.models import Avg, Max, Min, Sum, Count
import numpy as np
from app_api.data_process  import query_data_for_db

from django.db.models import Max, Min
import io, csv, pandas as pd
import numpy as np
import datetime
import numpy as np
import datetime as dt

# Acción 1.1:  SAN_DRAWN_CCY(t-1) mayor que SAN_DRAWN_CCY(t) y Protection Type= SRT
proceso_actual = MOB_T_SEC_PROCESS.objects.get(ID==xxx)
proceso_anterior = MOB_T_SEC_PROCESS.objects.filter(MOTNH=proceso_actual.MONTH - 1).filter(YEAR=proceso_actual.YEAR)[0]


        
        extrac_1 = MOB_T_OPERATION.objects.filter(PROTECTION_TYPE="SRT",ID_SEC_PROCESS=proceso_actual.ID)



# Acción 2.1:  Alertar al Portfolio Manager de que se ha detectado un evento de crédito    # *****************FALTA***********




mes = (MOB_T_OPERATION.objects.all().aggregate(Max('MONTH')))['MONTH__max']
mesant=mes-1

####  Defaulted amount '=MIN( drawn_eur de la operación con el credit_event="failure to pay"; RONA_eur de la operación con el credit_event="failure to pay")
# Defaulted_amount = np.array((MOB_T_OPERATION.objects.all().aggregate(Min('SAN_DRAWN_EUR')))['SAN_DRAWN_EUR__min'])

mes = (MOB_T_OPERATION.objects.all().aggregate(Max('MONTH')))['MONTH__max']
mesant=mes-1
# Acción 2.2: Cálculo de la perdida Inicial: Initial_Loss= LGD*Defaulted_amount
extrac_1 = MOB_T_OPERATION.objects.filter(PROTECTION_TYPE="SRT",MONTH=mes)
for i in extrac_1:
    j=MOB_T_OPERATION.objects.filter(LOAN=i.LOAN,MONTH=mesant)[0]




extrac_2 = MOB_T_OPERATION.objects.filter(PROTECTION_TYPE="SRT",MONTH=mes, CREDIT_EVENT="Failure to Pay")
for i in extrac_2:
    print(i)

print(mes)



    #Acción 1.1 RONA_ccy: (drawn_ccy (t-1)-drawn_ccy (t))/drawn_ccy(t-1)*RONA_ccy(t-1)
    RONA_ccy = np.array(i.SAN_DRAWN_CCY) / np.array(j.SAN_DRAWN_CCY) if np.array(j.SAN_DRAWN_CCY) != 0 and np.array(j.SAN_DRAWN_CCY) > np.array(i.SAN_DRAWN_CCY)   else 0
    RONA_ccy = RONA_ccy * np.array(j.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY)
    fx_mesant = MOB_T_FX.objects.filter(COUNTERVALUE=i.CCY,MONTH=mesant)[0]
    fx_mes = MOB_T_FX.objects.filter(COUNTERVALUE=i.CCY,MONTH=mes)[0]
#           print(np.array(fx_mesant.EUR))
    i.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY=RONA_ccy
    RONA_EUR = (RONA_ccy * np.array(fx_mesant.EUR)) / np.array(fx_mes.EUR)  if np.array(fx_mes.EUR) != 0 else 0  #Acción 1.2 RONA_ccy_FX_Corrected= RONA_ccy(t)*FX(t-1)/FX(t)
    i.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR= RONA_EUR
    i.save()
    #Acción 1.3
    if RONA_EUR==0:   #"Se generará una alerta al Portfolio Manager y indicando la operación amortizada en su totalidad"  
        alert =MOB_T_ALERT.objects.create(PP_ID=1, ID_MD=1, ID_SEC_PROCESS=1, ID_ENTITY=i.LOAN, COD_ALERT_TYPE="SPS_001",  
        NOTES="Operación amortizada en su totalidad", CREATED_BY ="testuser" ,  CREATED_ON=str(dt.datetime.now()),   
        UPDATED_BY="testuser",  UPDATED_ON=str(dt.datetime.now()), ACTIVE=1) 
        alert.save()
    else:    # "Se generará una alerta al Portfolio Manager y indicando la operación  ha sido parcialmente amortizada"
        alert =MOB_T_ALERT.objects.create(PP_ID=1, ID_MD=1, ID_SEC_PROCESS=1, ID_ENTITY=i.LOAN, COD_ALERT_TYPE="SPS_001",  
        NOTES="Operación  ha sido parcialmente amortizada", CREATED_BY ="testuser" ,  CREATED_ON=str(dt.datetime.now()),   
        UPDATED_BY="testuser",  UPDATED_ON=str(dt.datetime.now()), ACTIVE=1) 
        alert.save()
    respuesta="paso_0_accion1_ok"





        mes = (MOB_T_OPERATION.objects.all().aggregate(Max('MONTH')))['MONTH__max']
        mesant=mes-1
       extrac_1 = MOB_T_OPERATION.objects.filter(~Q(PROTECTION_TYPE = "SRT"),ID_SEC_PROCESS=proceso_actual.id)   
        for ma in extrac_1:
            fx_mes = MOB_T_FX.objects.filter(COUNTERVALUE=ma.CCY,ID_SEC_PROCESS=proceso_actual.id)[0]
            mant=MOB_T_OPERATION.objects.filter(LOAN=ma.LOAN,ID_SEC_PROCESS=proceso_anterior.id)[0]
            ma.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY= mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY    
            ma.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR= mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY  * np.array(fx_mes.EUR)   if mant.REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY!=None  else 0

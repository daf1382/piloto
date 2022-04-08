
from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import io, csv, pandas as pd
import numpy as np
import datetime as dt
import random

from app_api.models import  File, MOB_T_SEC_PROCESS, MOB_T_SEC_PROCESS_AUDIT, MOB_T_SEC_PROCESS_DOC,MOB_T_ALERT 
from app_api.models import MOB_T_OPERATION, MOB_T_PORTFOLIO, MOB_T_TRANCHE, MOB_T_FX, MOB_T_RATING

from app_api.data_process  import processing_data_for_db
from app_api.pasos  import processing_steps
def mid(s, offset, amount):
    return s[offset:offset+amount]



respuesta="None"

@csrf_exempt
def upload_file(request):
    file_from_request = request.FILES['file']
 #   prueba = request.POST['month']
 #   print(prueba)
    file = File()
    file_from_r=str(file_from_request)
    tipo_archivo=mid(file_from_r,0,file_from_r.find("_"))


    if tipo_archivo=="Operaciones":
        print("El archivo a subir es Operaciones")
        file.file_path.save('operacions_salida.csv', file_from_request)
        reader = pd.read_csv(file.file_path.name,sep=",", decimal=".",thousands=",")
        reader=reader.replace({np.nan: None})
        print("Procesando")        
        contract_list = [processing_data_for_db.get_operation_from_df_row(row) for row in reader.values]
        for i in contract_list:
            pass    
        print("Subiendo")
        MOB_T_OPERATION.objects.bulk_create(contract_list)
    
    if tipo_archivo=="Portfolio":
        print("El archivo subido es Portfolio")
        file.file_path.save('portfolio_salida.csv', file_from_request)
        reader = pd.read_csv(file.file_path.name,sep=",", decimal=".",thousands=",")
        reader=reader.replace({np.nan: None})
        contract_list = [processing_data_for_db.get_portfolio_from_df_row(row) for row in reader.values]
        MOB_T_PORTFOLIO.objects.bulk_create(contract_list)

    if tipo_archivo=="Tramos":
        print("El archivo subido es Tramos")
        file.file_path.save('tramos_salida.csv', file_from_request)
        reader = pd.read_csv(file.file_path.name,sep=",", decimal=".",thousands=",")
        reader=reader.replace({np.nan: None})
        contract_list = [processing_data_for_db.get_tranche_from_df_row(row) for row in reader.values]
        MOB_T_TRANCHE.objects.bulk_create(contract_list)

    if tipo_archivo=="FX":
        print("El archivo subido es FX")
        file.file_path.save('fx_salida.csv', file_from_request)
        reader = pd.read_csv(file.file_path.name,sep=",", decimal=".",thousands=",")
        reader=reader.replace({np.nan: None})
        contract_list = [processing_data_for_db.get_fx_from_df_row(row) for row in reader.values]
        MOB_T_FX.objects.bulk_create(contract_list)

    if tipo_archivo=="MOB":
        print("El archivo subido es MOB_T_SEC_PROCESS")
        file.file_path.save('MOB_T_SEC_PROCESS_salida.csv', file_from_request)
        reader = pd.read_csv(file.file_path.name,sep=";", decimal=".",thousands=",")
        reader=reader.replace({np.nan: None})
        contract_list = [processing_data_for_db.get_sec_process_from_df_row(row) for row in reader.values]
        MOB_T_SEC_PROCESS.objects.bulk_create(contract_list)

    if tipo_archivo=="RATING":
        print("El archivo subido es RATING_TABLA")
        file.file_path.save('RATING_TABLA_salida.csv', file_from_request)
        reader = pd.read_csv(file.file_path.name,sep=";") #, decimal=".",thousands=",")
        reader=reader.replace({np.nan: None})
        contract_list = [processing_data_for_db.get_rating_from_df_row(row) for row in reader.values]
        MOB_T_RATING.objects.bulk_create(contract_list)

    file_from_r="Archivo Subido: " + file_from_r
    return JsonResponse({"status1": file_from_r},safe=False)


@csrf_exempt   
def pasos(request):
    if request.method == 'POST':
        data= JSONParser().parse(request)
        msg = data['PASO']
        process_id = data['Process']
        print("proceso:", process_id)
        if msg==0:
            print("Arranca el paso 0")
            respuesta = processing_steps.paso_0(process_id)
        if msg==1 or msg==2:
            print("Arranca el paso 1 y 2")
            fecha_del_calculo=data['Fecha_del_calculo']
            respuesta = processing_steps.paso_1(process_id,fecha_del_calculo)        
        if msg==3:
            print("Arranca el paso 3")
            fecha_del_calculo=data['Fecha_del_calculo']
            respuesta = processing_steps.paso_3(process_id,fecha_del_calculo)
        if msg==4:
            print("Arranca el paso 4")
            fecha_del_calculo=data['Fecha_del_calculo']
            respuesta = processing_steps.paso_4(process_id,fecha_del_calculo)
        return JsonResponse({"status2": respuesta}, safe=False)           

#    msg = data['month']
#    print(msg)

    return JsonResponse({"status2": respuesta}, safe=False)




from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import ExtractMonth
from django.db.models import F
from rest_framework.parsers import JSONParser
import io, csv, pandas as pd
import numpy as np

from app_api.models import Contract, File

#from .models import Choice, Question

# Create your views here.

@csrf_exempt
def hello_world(request):
    if request.method == 'POST':
        data= JSONParser().parse(request)
        msg = data['test']
        respuesta= JsonResponse({'hello': msg}, safe= False)
 #       respuesta=processing_data.prueba1(data)
        return respuesta
    elif request.method == 'GET':
        return JsonResponse({'hello_world': 'GET'}, safe=False)



@csrf_exempt
def upload_file(request):
    if Contract.objects.exists():
        return JsonResponse({"status1": "alreadyupload"},safe=False)
    else: 
        file_from_request = request.FILES['file']
        file = File()
        file.file_path.save('operacions_salida.csv', file_from_request)
        reader = pd.read_csv(file.file_path.name,sep=";",decimal=",",thousands=".")
        reader=reader.replace({np.nan: None})
        contract_list = [get_contract_from_df_row(row) for row in reader.values]
        Contract.objects.bulk_create(contract_list)
        test_list = Contract.objects.filter(borrower_internal_rating=1.1)
        for c in test_list:
            print(c.contract)   
        return JsonResponse({"status1": "success1"},safe=False)

@csrf_exempt   
def month(request):
    if request.method == 'POST':
        Contract.objects.all().update(month=ExtractMonth('start'))
        data= JSONParser().parse(request)
        msg = data['month']
        test_list = Contract.objects.filter(month=msg)
        respuesta="ok"
        return JsonResponse({"status2": respuesta}, safe=False)



def get_contract_from_df_row(row):
    return Contract(
        borrower = row[0],
        guarantor = row[1],
        group = row[2],
        contract = row[3],
        loan_type = row[4],
        start = row[5],
        maturity = row[6],
        borrower_internal_rating = row[7],
        guarantor_internal_rating = row[8],
        rating_date = row[9],
        lgd = row[10],
        pd = row[11],
        scan = row[12],
        margin = row[13],
        industry = row[14],
        country = row[15],
        ccy = row[16],
        commit_ccy = row[17],
        commit_eur = row[18],
        drawn_ccy = row[19],
        drawn_eur = row[20],
        wal = row[21],
        classification = row[22],
        ifrs_9_provision_perc = row[23],
        rwa_perc = row[24],
        business = row[25],
        protection_start_date = row[26],
        rona_ccy = row[27],
        rona_eur = row[28],
        protection_type = row[29],
        retention_requirement = row[30],
        credit_event = row[31],
        credit_event_verification_report = row[32],
        date_credit_event_verification_report = row[33],
        initial_loss_verification_report_y_n_na = row[34],
        credit_protection_verification_report = row[35],
        recoveries = row[36],
        final_loss_perc = row[37],
        full_disposal = row[38],
        )



'''

    Contract.objects.bulk_create(contract_list)
    test_list = Contract.objects.filter(borrower_internal_rating=1.1)
    for c in test_list:
        print(c.contract)
'''
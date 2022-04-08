import datetime
from django.db import models
from django.utils import timezone




#########################   Tablas INPUT  #########################################

class File(models.Model):
    file_path = models.FileField(upload_to='./test')





#########################   Sec Process Tables  #########################################


class MOB_T_SEC_PROCESS(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    NUM_PROCESS = models.CharField(max_length=45,null=True)               #Number to identificate the securitization process SP/<YYYY><MM>/<ID>
    ID_FLOW_STEP = models.IntegerField(null=True)               #Workflow step for the process (to be defined in MOB_T_SEC_PROCESS_WF table)
    COD_STATUS = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with SEC_PROCESS_STATUS dimension
    YEAR = models.IntegerField(null=True)               #
    MONTH = models.IntegerField(null=True)               #
    CREATED_BY = models.CharField(max_length=255,null=True)               #
    CREATED_ON = models.CharField(max_length=45,null=True)               #
    UPDATED_BY = models.CharField(max_length=255,null=True)               #
    UPDATED_ON = models.CharField(max_length=45,null=True)               #
    ACTIVE = models.IntegerField(null=True)               #1/0 boolean value to identify active/deleteted rows in the database


class MOB_T_SEC_PROCESS_AUDIT(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    ID_SEC_PROCESS = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS
    NUM_SEC_PROCESS = models.CharField(max_length=45,null=True)               #Number NUM_PROCESS of the MOB_T_SEC_PROCESS
    ID_FLOW_STEP = models.IntegerField(null=True)               #Step at which was performed the action
    COD_STATUS = models.CharField(max_length=45,null=True)               #Status at which the action was performed
    COD_ACTIVITY = models.IntegerField(null=True)               #References elements of MOB_T_MASTERDATA with ACTIVITY_TYPE dimension
    COD_ACTION = models.IntegerField(null=True)               #References elements of MOB_T_MASTERDATA with ACTION dimension
    CREATED_BY = models.CharField(max_length=255,null=True)               #
    CREATED_ON = models.CharField(max_length=45,null=True)               #
    UPDATED_BY = models.CharField(max_length=255,null=True)               #
    UPDATED_ON = models.CharField(max_length=45,null=True)               #
    ACTIVE = models.CharField(max_length=45,null=True)               #1/0 boolean value to identify active/deleteted rows in the database


class MOB_T_SEC_PROCESS_DOC(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    ID_SEC_PROCESS = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS
    DOC_TYPE = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with DOC_TYPE dimension
    COD_STATUS = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with DOC_STATUS dimension
    APPIAN_ID_DOC = models.IntegerField(null=True)               #Appian identifier of the document
    NAME = models.CharField(max_length=255,null=True)               #
    EXTENSION = models.CharField(max_length=255,null=True)               #
    FILE_PATH = models.CharField(max_length=255,null=True)               #Path in the Python server where the file is stored
    CREATED_BY = models.CharField(max_length=255,null=True)               #
    CREATED_ON = models.CharField(max_length=45,null=True)               #
    UPDATED_BY = models.CharField(max_length=255,null=True)               #
    UPDATED_ON = models.CharField(max_length=45,null=True)               #
    ACTIVE = models.IntegerField(null=True)               #1/0 boolean value to identify active/deleteted rows in the database


class MOB_T_ALERT(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    ID_SEC_PROCESS = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS
    ID_ENTITY = models.CharField(max_length=45,null=True)               #Identifier of an entity, operations, tranches, … CONTRATO
    COD_ALERT_TYPE = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with ALERT_TYPE dimension   
    NOTES = models.CharField(max_length=45,null=True)               #
    CREATED_BY = models.CharField(max_length=255,null=True)               #
    CREATED_ON = models.CharField(max_length=45,null=True)               #
    UPDATED_BY = models.CharField(max_length=255,null=True)               #
    UPDATED_ON = models.CharField(max_length=45,null=True)               #
    ACTIVE = models.IntegerField(null=True)               #1/0 boolean value to identify active/deleteted rows in the database


class MOB_T_FX(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    ID_SEC_PROCESS = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS
    ID_SEC_PROCESS_DOC = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS_DOC
    COD_STATUS = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with OPERATION_SATUS dimension
    DATE = models.CharField(max_length=45,null=True)               #Input
    COUNTERVALUE = models.CharField(max_length=45,null=True)               #Input
    EUR =models.FloatField(null=True)               #Input
    CREATED_BY = models.CharField(max_length=255,null=True)               
    CREATED_ON = models.CharField(max_length=255,null=True)               
    UPDATED_BY = models.CharField(max_length=255,null=True)               
    UPDATED_ON = models.CharField(max_length=255,null=True)               
    ACTIVE = models.IntegerField(null=True)               #1/0 boolean value to identify active/deleteted rows in the database
    MONTH = models.IntegerField(null=True) 
    YEAR = models.IntegerField(null=True)


class MOB_T_OPERATION(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    ID_SEC_PROCESS = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS
    ID_SEC_PROCESS_DOC = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS_DOC
    COD_STATUS = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with OPERATION_SATUS dimension
    BORROWER = models.CharField(max_length=45,null=True)               #Input
    GUARANTOR = models.CharField(max_length=45,null=True)               #Input
    GROUP = models.CharField(max_length=45,null=True)               #Input
    LOAN = models.CharField(max_length=45,null=True)               #Input
    LOAN_TYPE = models.CharField(max_length=45,null=True)               #Input
    START = models.CharField(max_length=45,null=True)               #Input
    MATURITY = models.CharField(max_length=45,null=True)               #Input
    BORROWER_INTERNAL_RATING =  models.FloatField(null=True)             #Input
    GUARANTOR_INTERNAL_RATING = models.FloatField(null=True)              #Input
    RATING_DATE = models.CharField(max_length=45,null=True)               #Input
    LGD = models.FloatField(null=True)                #Input
    PD = models.FloatField(null=True)             #Input
    SCAN_STATUS = models.CharField(max_length=45,null=True)               #Input
    MARGIN = models.FloatField(null=True)                  #Input
    INDUSTRY = models.CharField(max_length=45,null=True)               #Input
    COUNTRY = models.CharField(max_length=45,null=True)               #Input
    CCY = models.CharField(max_length=45,null=True)               #Input
    COMMIT_CCY = models.FloatField(null=True)                  #Input
    COMMIT_EUR = models.FloatField(null=True)                 #Input
    SAN_DRAWN_CCY = models.FloatField(null=True)              #Input
    SAN_DRAWN_EUR = models.FloatField(null=True)                 #Input
    WAL_YEARS = models.FloatField(null=True)                  #Input
    CLASSIFICATION = models.CharField(max_length=45,null=True)               #Input
    IFRS_9_PROVISION =models.FloatField(null=True)               #Input
    RWA = models.FloatField(null=True)               #Input
    BUSINESS = models.CharField(max_length=45,null=True)               #Input
    PROTECTION_START_DATE = models.CharField(max_length=45,null=True)               #Input
    REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY = models.FloatField(null=True)              #Output
    REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR = models.FloatField(null=True)             #Output
    PROTECTION_TYPE = models.CharField(max_length=45,null=True)               #Input
    RETENTION_REQUERIMENT = models.FloatField(null=True)                 #Input
    CREDIT_EVENT = models.CharField(max_length=45,null=True)               #TODO_: Understand how to link to credit events
    CREDIT_EVENT_VERIF_REPORT = models.CharField(max_length=45,null=True)               #TODO_: Understand how to link to credit events
    DATE_CREDIT_EVENT_VERIF_REPORT = models.CharField(max_length=45,null=True)               #TODO_: Understand how to link to credit events
    INITIAL_LOSS_VERIF_REPORT_RESULT = models.CharField(max_length=45,null=True)               #TODO_: Understand how to link to credit events
    CREDIT_PROTECTION_VERIF_REPORT = models.CharField(max_length=45,null=True)               #TODO_: Understand how to link to credit events
    RECOVERIES =  models.FloatField(null=True)              #TODO_: Understand how to link to credit events
    FINAL_LOSS = models.FloatField(null=True)               #TODO_: Understand how to link to credit events
    FULL_DISPOSAL =  models.CharField(max_length=45,null=True)               #TODO_: Understand how to link to credit events
    STP_INICIAL_LOSS = models.FloatField(null=True)   
    STP_MAX_LOSS = models.FloatField(null=True)   
    STP_TOTAL_RECOVERIES = models.FloatField(null=True)   
    STP_CREDIT_PROTECTION_ADJUSTMENT_AMOUNT = models.FloatField(null=True)   
    STP_VERIFIED_ADJUSTMENT_AMOUNT = models.FloatField(null=True)   
    STP_RETENTION_PERC = models.FloatField(null=True)   
    STP_FREE_AMOUNT  = models.FloatField(null=True)  
    STP_RETENTION_AMOUNT  = models.FloatField(null=True)  
    STP_PROTECTIONTYPE_CAL  = models.FloatField(null=True)  
    STP_REMOVAL  = models.CharField(max_length=255,null=True)  
    STP_ELIGIBILITY  = models.CharField(max_length=255,null=True)
    STP_PROTECTION_TYPE_ELIGIBILITY   = models.CharField(max_length=255,null=True)
    STP_RONAS_EUR_SRT_ELIGIBILITY  = models.FloatField(null=True)  
    STP_INTERNAL_RATING  =  models.CharField(max_length=255,null=True)
    CREATED_BY = models.CharField(max_length=255,null=True)               #
    CREATED_ON = models.CharField(max_length=255,null=True)               #
    UPDATED_BY = models.CharField(max_length=255,null=True)               #
    UPDATED_ON = models.CharField(max_length=255,null=True)               #
    ACTIVE = models.IntegerField(null=True)               #1/0 boolean value to identify active/deleteted rows in the database



class MOB_T_PORTFOLIO(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    ID_SEC_PROCESS = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS
    ID_SEC_PROCESS_DOC = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS_DOC
    COD_STATUS = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with OPERATION_SATUS dimension
    CALC_DATE_INIT = models.CharField(max_length=45,null=True)               #Input
    CALC_DATE_END = models.CharField(max_length=45,null=True)               #Input
    PAYMENT_DATE_INI = models.CharField(max_length=45,null=True)               #Input
    PAYMENT_DATE_END = models.CharField(max_length=45,null=True)               #Input
    PORTFOLIO_NOTIONAL = models.CharField(max_length=45,null=True)               #Output
    REPLENISHMENT_INI = models.CharField(max_length=45,null=True)               #Input
    REPLENISHMENT_END = models.CharField(max_length=45,null=True)               #Input
    STP_DEFAULTED_AMOUNT_TOTAL = models.FloatField(null=True) 
    STP_RETENTION_AMOUNT_TOTAL = models.FloatField(null=True) 
    STP_RONAS_EUR_SRT_ELIGIBILITY =  models.FloatField(null=True)
    STP_CUMMULATIVE_UNMATURE_LOSSES = models.FloatField(null=True)
    CREATED_BY = models.CharField(max_length=255,null=True)               #
    CREATED_ON = models.CharField(max_length=255,null=True)               #
    UPDATED_BY = models.CharField(max_length=255,null=True)               #
    UPDATED_ON = models.CharField(max_length=255,null=True)               #
    ACTIVE = models.IntegerField(null=True)               #1/0 boolean value to identify active/deleteted rows in the database





class MOB_T_TRANCHE(models.Model):
    PP_ID = models.IntegerField(null=True)               #Track Appian process instances
    ID_MD = models.IntegerField(null=True)               #Refer to the MOB_T_MASTERDATA version (default 1)
    ID_SEC_PROCESS = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS
    ID_SEC_PROCESS_DOC = models.IntegerField(null=True)               #Identifier of the MOB_T_SEC_PROCESS_DOC
    COD_STATUS = models.CharField(max_length=45,null=True)               #References elements of MOB_T_MASTERDATA with OPERATION_SATUS dimension
    TRANCHE_TYPE = models.CharField(max_length=45,null=True)               #Input
    TRANCHE_SENIORITY = models.IntegerField(null=True)               #Input
    TRANCHE_THICKNESS =models.FloatField(null=True)                #Output?
    CLASS_NOTIONAL =models.FloatField(null=True)                #Output?
    AMORTISATION_AMOUNT =models.FloatField(null=True)                #Input
    LOSS_BALANCE =models.FloatField(null=True)                #Input
    PROTECTION_FEE_RATE =models.FloatField(null=True)                #Input
    PROTECTION_FEE_AMOUNT = models.CharField(max_length=45,null=True)               #Output?
    PROTECTION_SELLER_EXPENSES =models.FloatField(null=True)                #Input
    EURIBOR_FIXING =models.FloatField(null=True)                #Input
    COLLATERAL_INCOME =models.FloatField(null=True)                #Output?
    NOTE_INTEREST =models.FloatField(null=True)             
    STP_ADJUSTED_LOSS_BALANCE =models.FloatField(null=True) 
    CREATED_BY = models.CharField(max_length=255,null=True)               #
    CREATED_ON = models.CharField(max_length=255,null=True)               #
    UPDATED_BY = models.CharField(max_length=255,null=True)               #
    UPDATED_ON = models.CharField(max_length=255,null=True)               #
    ACTIVE = models.IntegerField(null=True)               #1/0 boolean value to identify active/deleteted rows in the database
 



class MOB_T_RATING(models.Model):
    PD_RATING = models.CharField(max_length=255,null=True)
    INTERNAL_RATING =  models.CharField(max_length=255,null=True)    





from django.http import HttpResponseRedirect, JsonResponse
from app_api.models import   MOB_T_SEC_PROCESS, MOB_T_SEC_PROCESS_AUDIT, MOB_T_SEC_PROCESS_DOC,MOB_T_ALERT, MOB_T_OPERATION, MOB_T_PORTFOLIO
from app_api.models import MOB_T_TRANCHE, MOB_T_FX, MOB_T_RATING

#queryset = Account.objects.all()

class processing_data_for_db:   
    def get_sec_process_from_df_row(row):
        return MOB_T_SEC_PROCESS(
            PP_ID  = row[0],
            ID_MD  = row[1],
            NUM_PROCESS  = row[2],
            ID_FLOW_STEP  = row[3],
            COD_STATUS  = row[4],
            YEAR  = row[5],
            MONTH  = row[6],
            CREATED_BY  = row[7],
            CREATED_ON  = row[8],
            UPDATED_BY  = row[9],
            UPDATED_ON  = row[10],
            ACTIVE  = row[11],
            )

    def get_sec_process_audit_from_df_row(row):
        return MOB_T_SEC_PROCESS_AUDIT(
            PP_ID  = row[0],
            ID_MD  = row[1],
            ID_SEC_PROCESS  = row[2],
            NUM_SEC_PROCESS  = row[3],
            ID_FLOW_STEP  = row[4],
            COD_STATUS  = row[5],
            COD_ACTIVITY  = row[6],
            COD_ACTION  = row[7],
            CREATED_BY  = row[8],
            CREATED_ON  = row[9],
            UPDATED_BY  = row[10],
            UPDATED_ON  = row[11],
            ACTIVE  = row[12],
            )

    def get_sec_process_doc_from_df_row(row):
        return MOB_T_SEC_PROCESS_DOC(
            PP_ID  = row[0],
            ID_MD  = row[1],
            ID_SEC_PROCESS  = row[2],
            DOC_TYPE  = row[3],
            COD_STATUS  = row[4],
            APPIAN_ID_DOC  = row[5],
            NAME  = row[6],
            EXTENSION  = row[7],
            FILE_PATH  = row[8],
            CREATED_BY  = row[9],
            CREATED_ON  = row[10],
            UPDATED_BY  = row[11],
            UPDATED_ON  = row[12],
            ACTIVE  = row[13],
            )

    def get_alert_from_df_row(row):
        return MOB_T_ALERT(
            PP_ID  = row[0],
            ID_MD  = row[1],
            ID_SEC_PROCESS  = row[2],
            ID_ENTITY  = row[3],
            COD_ALERT_TYPE  = row[4],
            NOTE  = row[5],
            CREATED_BY  = row[6],
            CREATED_ON  = row[7],
            UPDATED_BY  = row[8],
            UPDATED_ON  = row[9],
            ACTIVE  = row[10],
            )

    def get_operation_from_df_row(row):
        return MOB_T_OPERATION(
            PP_ID  = row[0],
            ID_MD  = row[1],
            ID_SEC_PROCESS  = row[2],
            ID_SEC_PROCESS_DOC  = row[3],
            COD_STATUS  = row[4],
            BORROWER  = row[5],
            GUARANTOR  = row[6],
            GROUP  = row[7],
            LOAN  = row[8],
            LOAN_TYPE  = row[9],
            START  = row[10],
            MATURITY  = row[11],
            BORROWER_INTERNAL_RATING  = row[12],
            GUARANTOR_INTERNAL_RATING  = row[13],
            RATING_DATE  = row[14],
            LGD  = row[15],
            PD  = row[16],
            SCAN_STATUS  = row[17],
            MARGIN  = row[18],
            INDUSTRY  = row[19],
            COUNTRY  = row[20],
            CCY  = row[21],
            COMMIT_CCY  = row[22],
            COMMIT_EUR  = row[23],
            SAN_DRAWN_CCY  = row[24],
            SAN_DRAWN_EUR  = row[25],
            WAL_YEARS  = row[26],
            CLASSIFICATION  = row[27],
            IFRS_9_PROVISION  = row[28],
            RWA  = row[29],
            BUSINESS  = row[30],
            PROTECTION_START_DATE  = row[31],
            REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY  = row[32],
            REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR  = row[33],
            PROTECTION_TYPE  = row[34],
            RETENTION_REQUERIMENT  = row[35],
            CREDIT_EVENT  = row[36],
            CREDIT_EVENT_VERIF_REPORT  = row[37],
            DATE_CREDIT_EVENT_VERIF_REPORT  = row[38],
            INITIAL_LOSS_VERIF_REPORT_RESULT  = row[39],
            CREDIT_PROTECTION_VERIF_REPORT  = row[40],
            RECOVERIES  = row[41],
            FINAL_LOSS  = row[42],
            FULL_DISPOSAL  = row[43],
            STP_INICIAL_LOSS  = row[44],
            STP_MAX_LOSS  = row[45],
            STP_TOTAL_RECOVERIES  = row[46],
            STP_CREDIT_PROTECTION_ADJUSTMENT_AMOUNT  = row[47],
            STP_VERIFIED_ADJUSTMENT_AMOUNT  = row[48],
            STP_RETENTION_PERC  = row[49],
            STP_FREE_AMOUNT  = row[50],
            STP_RETENTION_AMOUNT  = row[51],
            STP_PROTECTIONTYPE_CAL  = row[52],
            STP_REMOVAL  = row[53],
            STP_ELIGIBILITY  = row[54],
            STP_PROTECTION_TYPE_ELIGIBILITY   = row[55],
            STP_INTERNAL_RATING  = row[56],
            STP_RONAS_EUR_SRT_ELIGIBILITY  = row[57],
            CREATED_BY  = row[58],
            CREATED_ON  = row[59],
            UPDATED_BY  = row[60],
            UPDATED_ON  = row[61],
            ACTIVE  = row[62],   
            )




    def get_portfolio_from_df_row(row):
        return MOB_T_PORTFOLIO(
            PP_ID  = row[0],
            ID_MD  = row[1],
            ID_SEC_PROCESS  = row[2],
            ID_SEC_PROCESS_DOC  = row[3],
            COD_STATUS  = row[4],
            CALC_DATE_INIT  = row[5],
            CALC_DATE_END  = row[6],
            PAYMENT_DATE_INI  = row[7],
            PAYMENT_DATE_END  = row[8],
            PORTFOLIO_NOTIONAL  = row[9],
            REPLENISHMENT_INI  = row[10],
            REPLENISHMENT_END  = row[11],
            STP_DEFAULTED_AMOUNT_TOTAL = row[12],
            STP_RETENTION_AMOUNT_TOTAL = row[13],
            STP_RONAS_EUR_SRT_ELIGIBILITY = row[14],
            STP_CUMMULATIVE_UNMATURE_LOSSES = row[15],
            CREATED_BY  = row[16],
            CREATED_ON  = row[17],
            UPDATED_BY  = row[18],
            UPDATED_ON  = row[19],
            ACTIVE  = row[20],       
            )

    def get_tranche_from_df_row(row):
        return MOB_T_TRANCHE(
            PP_ID  = row[0],
            ID_MD  = row[1],
            ID_SEC_PROCESS  = row[2],
            ID_SEC_PROCESS_DOC  = row[3],
            COD_STATUS  = row[4],
            TRANCHE_TYPE  = row[5],
            TRANCHE_SENIORITY  = row[6],
            TRANCHE_THICKNESS  = row[7],
            CLASS_NOTIONAL  = row[8],
            AMORTISATION_AMOUNT  = row[9],
            LOSS_BALANCE  = row[10],
            PROTECTION_FEE_RATE  = row[11],
            PROTECTION_FEE_AMOUNT  = row[12],
            PROTECTION_SELLER_EXPENSES  = row[13],
            EURIBOR_FIXING  = row[14],
            COLLATERAL_INCOME  = row[15],
            NOTE_INTEREST  = row[16],
            STP_ADJUSTED_LOSS_BALANCE = row[17],
            CREATED_BY  = row[18],
            CREATED_ON  = row[19],
            UPDATED_BY  = row[20],
            UPDATED_ON  = row[21],
            ACTIVE  = row[22],
            )

    def get_fx_from_df_row(row):
        return MOB_T_FX(
            PP_ID  = row[0],
            ID_MD  = row[1],
            ID_SEC_PROCESS  = row[2],
            ID_SEC_PROCESS_DOC  = row[3],
            COD_STATUS  = row[4],
            DATE  = row[5],
            COUNTERVALUE  = row[6],
            EUR  = row[7],
            CREATED_BY  = row[8],
            CREATED_ON  = row[9],
            UPDATED_BY  = row[10],
            UPDATED_ON  = row[11],
            ACTIVE  = row[12],
            )
    def get_rating_from_df_row(row):
        return MOB_T_RATING(
            PD_RATING  = row[0],
            INTERNAL_RATING  = row[1],
        )
    
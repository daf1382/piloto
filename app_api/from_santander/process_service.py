import math
#from api.commprotocol.server_response import NON_EXISTENT_PROCESS, SUCCESS, WRONG_FILE, WRONG_JSON, ServerResponse
from app_api.models import FX, DocProcess, Operation, Portfolio, Process, Tranche
#from app_api.services import pandas_service, procedure_db_service, util_service
from app_api.utils.constants import BLOCK_SIZE, LOGGER, SYSTEM
#logger = LOGGER




def contracts_upload(process: Process, file: DocProcess):
    try:
        # Operations
        process_operations(process, file)
        # Portfolio
        process_portfolio(process, file)
        # Tranche
        process_tranche(process, file)
        # FX
        process_fx(process, file)
    except Exception as e:
        logger.error(str(e))
        return ServerResponse(status=WRONG_FILE)
    return ServerResponse(status=SUCCESS)



def process_operations(process: Process, file: DocProcess):
    logger.info('Reading operations from Excel file...')
    operations = pandas_service.read_excel(file.FILE_PATH.name, sheet=0)
    # We prepare data before insertion
    logger.info('Preparing data before insertion of operations in the DB')
    l = [op_from_dataframe(m, process, file) for m in operations.values]
    logger.info('Starting the insertion of operations in the DB')
    # A block is a set of BLOCK_SIZE contracts
    # We calculate the number of blocks rounding up
    total_blocks = math.ceil(len(l) / BLOCK_SIZE)
    for i in range(total_blocks):
        Operation.objects.bulk_create(l[i*BLOCK_SIZE:(i + 1)*BLOCK_SIZE])
    logger.info(
        'Completed insertion of operations in the DB. Uploaded blocks: {0}'.format(total_blocks))


def process_portfolio(process: Process, file: DocProcess):
    logger.info('Reading portfolio from Excel file...')
    portfolio = pandas_service.read_excel(file.FILE_PATH.name, sheet=1)
    # We prepare data before insertion
    logger.info('Preparing data before insertion of portfolio in the DB')
    l = [portfolio_from_dataframe(p, process, file) for p in portfolio.values]
    logger.info('Starting the insertion of portfolio in the DB')
    Portfolio.objects.bulk_create(l)
    logger.info(
        'Completed insertion of portfolio in the DB. Uploaded portfolio: {0}'.format(len(l)))
def process_tranche(process: Process, file: DocProcess):
    logger.info('Reading tranches from Excel file...')
    tranches = pandas_service.read_excel(file.FILE_PATH.name, sheet=2)
    # We prepare data before insertion
    logger.info('Preparing data before insertion of tranches in the DB')
    l = [tranche_from_dataframe(t, process, file) for t in tranches.values]
    logger.info('Starting the insertion of tranches in the DB')
    Tranche.objects.bulk_create(l)
    logger.info(
        'Completed insertion of tranches in the DB. Uploaded tranches: {0}'.format(len(l)))


def process_fx(process: Process, file: DocProcess):
    logger.info('Reading fx from Excel file...')
    fx = pandas_service.read_excel(file.FILE_PATH.name, sheet=3)
    # We prepare data before insertion
    logger.info('Preparing data before insertion of fx in the DB')
    l = [fx_from_dataframe(f, process, file) for f in fx.values]
    logger.info('Starting the insertion of fx in the DB')
    FX.objects.bulk_create(l)
    logger.info(
        'Completed insertion of fx in the DB. Uploaded fx: {0}'.format(len(l)))


        
def op_from_dataframe(op, process: Process, file: DocProcess):
    return Operation(
        PP_ID=file.PP_ID, ID_MD=process.ID_MD, ID_SEC_PROCESS=process.ID, ID_SEC_PROCESS_DOC=file.ID,
        BORROWER=op[0], GUARANTOR=op[1], GROUP=op[2],
        LOAN=op[3], LOAN_TYPE=op[4], START=op[5],
        MATURITY=op[6], BORROWER_INTERNAL_RATING=op[7], GUARANTOR_INTERNAL_RATING=op[8],
        RATING_DATE=op[9], LGD=op[10], PD=op[11],
        SCAN_STATUS=op[12], MARGIN=op[13], INDUSTRY=op[14],
        COUNTRY=op[15], CCY=op[16], COMMIT_CCY=op[17],
        COMMIT_EUR=op[18], SAN_DRAWN_CCY=op[19], SAN_DRAWN_EUR=op[20],
        WAL_YEARS=op[21], CLASSIFICATION=op[22], IFRS_9_PROVISION=op[23],
        RWA=op[24], BUSINESS=op[25], PROTECTION_START_DATE=op[26],
        PROTECTION_TYPE=op[27], RETENTION_REQUERIMENT=op[28], CREDIT_EVENT=op[29],
        CREDIT_EVENT_VERIF_REP=op[30], DATE_CREDIT_EVENT_VERIF_REP=op[
            31], INITIAL_LOSS_VERIF_REP_RES=op[32],
        CREDIT_PROTECTION_VERIF_REP=op[33], RECOVERIES=op[34],
        CREATED_BY=SYSTEM, UPDATED_BY=SYSTEM, ACTIVE=1
    )
def portfolio_from_dataframe(p, process: Process, file: DocProcess):
    return Portfolio(
        PP_ID=file.PP_ID, ID_MD=process.ID_MD, ID_SEC_PROCESS=process.ID, ID_SEC_PROCESS_DOC=file.ID,
        CALCULATION_DATE_INIT=p[0], CALCULATION_DATE_END=p[1], PAYMENT_DATE_INIT=p[2],
        PAYMENT_DATE_END=p[3], REPLENISHMENT_INIT=p[4], REPLENISHMENT_END=p[5],
        CREATED_BY=SYSTEM, UPDATED_BY=SYSTEM, ACTIVE=1
    )
def tranche_from_dataframe(t, process: Process, file: DocProcess):
    return Tranche(
        PP_ID=file.PP_ID, ID_MD=process.ID_MD, ID_SEC_PROCESS=process.ID, ID_SEC_PROCESS_DOC=file.ID,
        TRANCHE_TYPE=t[0], TRANCHE_SENIORITY=t[1], AMORTISATION_AMOUNT=t[2],
        LOSS_BALANCE=t[3], PROTECTION_FEE_RATE=t[4], PROTECTION_SELLER_EXPENSES=t[5],
        EURIBOR_FIXING=t[6],
        CREATED_BY=SYSTEM, UPDATED_BY=SYSTEM, ACTIVE=1
    )
def fx_from_dataframe(fx, process: Process, file: DocProcess):
    return FX(
        PP_ID=file.PP_ID, ID_MD=process.ID_MD, ID_SEC_PROCESS=process.ID, ID_SEC_PROCESS_DOC=file.ID,
        DATE=fx[0], COUNTERVALUE=fx[1], EUR=fx[2],
        CREATED_BY=SYSTEM, UPDATED_BY=SYSTEM, ACTIVE=1
    )
def pasocero(data: dict[str, any]):
    try:
        process_id = data['process_id']
        pp_id = data['pp_id']
    except:
        return ServerResponse(status=WRONG_JSON)
    try:
        current_process = Process.objects.get(ID=process_id)
    except:
        return ServerResponse(status=NON_EXISTENT_PROCESS)
    last_month, last_year = util_service.last_date(
        current_process.MONTH, current_process.YEAR)
    last_process = Process.objects.get(MONTH=last_month, YEAR=last_year)
    # Actions 1.1, 1.2
    procedure_db_service.call_rona_procedure(
        current_process.ID, last_process.ID)
    # Actions 1.3
    # ...
    rona_zero_list = Operation.objects.filter(
        ID_SEC_PROCESS=current_process.ID, RONA_CCY=0)
    for opearation in rona_zero_list:
        # INSERTAR ALERTA
        pass
    return ServerResponse(status=SUCCESS)

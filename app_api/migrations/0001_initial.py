# Generated by Django 2.2 on 2022-04-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.FileField(upload_to='./test')),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_ALERT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS', models.IntegerField(null=True)),
                ('ID_ENTITY', models.CharField(max_length=45, null=True)),
                ('COD_ALERT_TYPE', models.CharField(max_length=45, null=True)),
                ('NOTES', models.CharField(max_length=45, null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=45, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=45, null=True)),
                ('ACTIVE', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_FX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS_DOC', models.IntegerField(null=True)),
                ('COD_STATUS', models.CharField(max_length=45, null=True)),
                ('DATE', models.CharField(max_length=45, null=True)),
                ('COUNTERVALUE', models.CharField(max_length=45, null=True)),
                ('EUR', models.FloatField(null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=255, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=255, null=True)),
                ('ACTIVE', models.IntegerField(null=True)),
                ('MONTH', models.IntegerField(null=True)),
                ('YEAR', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_OPERATION',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS_DOC', models.IntegerField(null=True)),
                ('COD_STATUS', models.CharField(max_length=45, null=True)),
                ('BORROWER', models.CharField(max_length=45, null=True)),
                ('GUARANTOR', models.CharField(max_length=45, null=True)),
                ('GROUP', models.CharField(max_length=45, null=True)),
                ('LOAN', models.CharField(max_length=45, null=True)),
                ('LOAN_TYPE', models.CharField(max_length=45, null=True)),
                ('START', models.CharField(max_length=45, null=True)),
                ('MATURITY', models.CharField(max_length=45, null=True)),
                ('BORROWER_INTERNAL_RATING', models.FloatField(null=True)),
                ('GUARANTOR_INTERNAL_RATING', models.FloatField(null=True)),
                ('RATING_DATE', models.CharField(max_length=45, null=True)),
                ('LGD', models.FloatField(null=True)),
                ('PD', models.FloatField(null=True)),
                ('SCAN_STATUS', models.CharField(max_length=45, null=True)),
                ('MARGIN', models.FloatField(null=True)),
                ('INDUSTRY', models.CharField(max_length=45, null=True)),
                ('COUNTRY', models.CharField(max_length=45, null=True)),
                ('CCY', models.CharField(max_length=45, null=True)),
                ('COMMIT_CCY', models.FloatField(null=True)),
                ('COMMIT_EUR', models.FloatField(null=True)),
                ('SAN_DRAWN_CCY', models.FloatField(null=True)),
                ('SAN_DRAWN_EUR', models.FloatField(null=True)),
                ('WAL_YEARS', models.FloatField(null=True)),
                ('CLASSIFICATION', models.CharField(max_length=45, null=True)),
                ('IFRS_9_PROVISION', models.FloatField(null=True)),
                ('RWA', models.FloatField(null=True)),
                ('BUSINESS', models.CharField(max_length=45, null=True)),
                ('PROTECTION_START_DATE', models.CharField(max_length=45, null=True)),
                ('REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_CCY', models.FloatField(null=True)),
                ('REFERENCE_OBLIGATION_NOTIONAL_AMOUNT_EUR', models.FloatField(null=True)),
                ('PROTECTION_TYPE', models.CharField(max_length=45, null=True)),
                ('RETENTION_REQUERIMENT', models.FloatField(null=True)),
                ('CREDIT_EVENT', models.CharField(max_length=45, null=True)),
                ('CREDIT_EVENT_VERIF_REPORT', models.CharField(max_length=45, null=True)),
                ('DATE_CREDIT_EVENT_VERIF_REPORT', models.CharField(max_length=45, null=True)),
                ('INITIAL_LOSS_VERIF_REPORT_RESULT', models.CharField(max_length=45, null=True)),
                ('CREDIT_PROTECTION_VERIF_REPORT', models.CharField(max_length=45, null=True)),
                ('RECOVERIES', models.FloatField(null=True)),
                ('FINAL_LOSS', models.FloatField(null=True)),
                ('FULL_DISPOSAL', models.CharField(max_length=45, null=True)),
                ('STP_INICIAL_LOSS', models.FloatField(null=True)),
                ('STP_MAX_LOSS', models.FloatField(null=True)),
                ('STP_TOTAL_RECOVERIES', models.FloatField(null=True)),
                ('STP_CREDIT_PROTECTION_ADJUSTMENT_AMOUNT', models.FloatField(null=True)),
                ('STP_VERIFIED_ADJUSTMENT_AMOUNT', models.FloatField(null=True)),
                ('STP_RETENTION_PERC', models.FloatField(null=True)),
                ('STP_FREE_AMOUNT', models.FloatField(null=True)),
                ('STP_RETENTION_AMOUNT', models.FloatField(null=True)),
                ('STP_PROTECTIONTYPE_CAL', models.FloatField(null=True)),
                ('STP_REMOVAL', models.CharField(max_length=255, null=True)),
                ('STP_ELIGIBILITY', models.CharField(max_length=255, null=True)),
                ('STP_PROTECTION_TYPE_ELIGIBILITY', models.CharField(max_length=255, null=True)),
                ('STP_RONAS_EUR_SRT_ELIGIBILITY', models.FloatField(null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=255, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=255, null=True)),
                ('ACTIVE', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_PORTFOLIO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS_DOC', models.IntegerField(null=True)),
                ('COD_STATUS', models.CharField(max_length=45, null=True)),
                ('CALC_DATE_INIT', models.CharField(max_length=45, null=True)),
                ('CALC_DATE_END', models.CharField(max_length=45, null=True)),
                ('PAYMENT_DATE_INI', models.CharField(max_length=45, null=True)),
                ('PAYMENT_DATE_END', models.CharField(max_length=45, null=True)),
                ('PORTFOLIO_NOTIONAL', models.CharField(max_length=45, null=True)),
                ('REPLENISHMENT_INI', models.CharField(max_length=45, null=True)),
                ('REPLENISHMENT_END', models.CharField(max_length=45, null=True)),
                ('STP_DEFAULTED_AMOUNT_TOTAL', models.FloatField(null=True)),
                ('STP_RETENTION_AMOUNT_TOTAL', models.FloatField(null=True)),
                ('STP_RONAS_EUR_SRT_ELIGIBILITY', models.FloatField(null=True)),
                ('STP_CUMMULATIVE_UNMATURE_LOSSES', models.FloatField(null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=255, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=255, null=True)),
                ('ACTIVE', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_RATING',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PD_RATING', models.FloatField(null=True)),
                ('INTERNAL_RATING', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_SEC_PROCESS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('NUM_PROCESS', models.CharField(max_length=45, null=True)),
                ('ID_FLOW_STEP', models.IntegerField(null=True)),
                ('COD_STATUS', models.CharField(max_length=45, null=True)),
                ('YEAR', models.IntegerField(null=True)),
                ('MONTH', models.IntegerField(null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=45, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=45, null=True)),
                ('ACTIVE', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_SEC_PROCESS_AUDIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS', models.IntegerField(null=True)),
                ('NUM_SEC_PROCESS', models.CharField(max_length=45, null=True)),
                ('ID_FLOW_STEP', models.IntegerField(null=True)),
                ('COD_STATUS', models.CharField(max_length=45, null=True)),
                ('COD_ACTIVITY', models.IntegerField(null=True)),
                ('COD_ACTION', models.IntegerField(null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=45, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=45, null=True)),
                ('ACTIVE', models.CharField(max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_SEC_PROCESS_DOC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS', models.IntegerField(null=True)),
                ('DOC_TYPE', models.CharField(max_length=45, null=True)),
                ('COD_STATUS', models.CharField(max_length=45, null=True)),
                ('APPIAN_ID_DOC', models.IntegerField(null=True)),
                ('NAME', models.CharField(max_length=255, null=True)),
                ('EXTENSION', models.CharField(max_length=255, null=True)),
                ('FILE_PATH', models.CharField(max_length=255, null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=45, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=45, null=True)),
                ('ACTIVE', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MOB_T_TRANCHE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PP_ID', models.IntegerField(null=True)),
                ('ID_MD', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS', models.IntegerField(null=True)),
                ('ID_SEC_PROCESS_DOC', models.IntegerField(null=True)),
                ('COD_STATUS', models.CharField(max_length=45, null=True)),
                ('TRANCHE_TYPE', models.CharField(max_length=45, null=True)),
                ('TRANCHE_SENIORITY', models.IntegerField(null=True)),
                ('TRANCHE_THICKNESS', models.FloatField(null=True)),
                ('CLASS_NOTIONAL', models.FloatField(null=True)),
                ('AMORTISATION_AMOUNT', models.FloatField(null=True)),
                ('LOSS_BALANCE', models.FloatField(null=True)),
                ('PROTECTION_FEE_RATE', models.FloatField(null=True)),
                ('PROTECTION_FEE_AMOUNT', models.CharField(max_length=45, null=True)),
                ('PROTECTION_SELLER_EXPENSES', models.FloatField(null=True)),
                ('EURIBOR_FIXING', models.FloatField(null=True)),
                ('COLLATERAL_INCOME', models.FloatField(null=True)),
                ('NOTE_INTEREST', models.FloatField(null=True)),
                ('STP_ADJUSTED_LOSS_BALANCE', models.FloatField(null=True)),
                ('CREATED_BY', models.CharField(max_length=255, null=True)),
                ('CREATED_ON', models.CharField(max_length=255, null=True)),
                ('UPDATED_BY', models.CharField(max_length=255, null=True)),
                ('UPDATED_ON', models.CharField(max_length=255, null=True)),
                ('ACTIVE', models.IntegerField(null=True)),
            ],
        ),
    ]

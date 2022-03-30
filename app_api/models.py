import datetime
from django.db import models
from django.utils import timezone

class Contract(models.Model):
    borrower = models.CharField(max_length=20, null=True)
    guarantor = models.CharField(max_length=20, null=True)
    group = models.CharField(max_length=20, null=True)
    contract = models.CharField(max_length=20, null=True)
    loan_type = models.CharField(max_length=20, null=True)
    start = models.DateField(null=True)
    maturity = models.DateField(null=True)
    borrower_internal_rating = models.FloatField(null=True)
    guarantor_internal_rating = models.FloatField(null=True)
    rating_date = models.DateField(null=True)
    lgd = models.FloatField(null=True)
    pd = models.FloatField(null=True)
    scan = models.CharField(max_length=20, null=True)
    margin = models.FloatField(null=True)
    industry = models.IntegerField(null=True)
    country = models.CharField(max_length=20, null=True)
    ccy = models.CharField(max_length=20, null=True)
    commit_ccy = models.FloatField(null=True)
    commit_eur = models.FloatField(null=True)
    drawn_ccy = models.FloatField(null=True)
    drawn_eur = models.FloatField(null=True)
    wal = models.FloatField(null=True)
    classification = models.CharField(max_length=30, null=True)
    ifrs_9_provision_perc = models.FloatField(null=True)
    rwa_perc = models.FloatField(null=True)
    business = models.CharField(max_length=20, null=True)
    protection_start_date = models.DateField(null=True)
    rona_ccy = models.FloatField(null=True)
    rona_eur = models.FloatField(null=True)
    protection_type = models.CharField(max_length=20, null=True)
    retention_requirement = models.FloatField(null=True)
    credit_event = models.FloatField(null=True)
    credit_event_verification_report = models.FloatField(null=True)
    date_credit_event_verification_report = models.FloatField(null=True)
    initial_loss_verification_report_y_n_na = models.FloatField(null=True)
    credit_protection_verification_report = models.FloatField(null=True)
    recoveries = models.FloatField(null=True)
    final_loss_perc = models.FloatField(null=True)
    full_disposal = models.FloatField(null=True)
    month = models.IntegerField(null=True)

    def __str__(self):
        return self.contract




class File(models.Model):
    file_path = models.FileField(upload_to='./test')



 #   process = models.ForeignKey('Process', on_delete=models.DO_NOTHING,null=True)
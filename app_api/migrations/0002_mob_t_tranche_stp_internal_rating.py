# Generated by Django 2.2 on 2022-04-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mob_t_tranche',
            name='STP_INTERNAL_RATING',
            field=models.FloatField(null=True),
        ),
    ]

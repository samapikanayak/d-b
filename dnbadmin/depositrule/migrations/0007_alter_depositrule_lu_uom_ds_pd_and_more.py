# Generated by Django 4.0.4 on 2022-07-22 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depositrule', '0006_rename_unit_of_measure_code_depositrule_lu_uom_ds_pd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositrule',
            name='LU_UOM_DS_PD',
            field=models.CharField(max_length=40, verbose_name='DepositPaidOnUnitOfMeasureCode'),
        ),
        migrations.AlterField(
            model_name='depositrule',
            name='MO_UOM_DS_PD',
            field=models.DecimalField(decimal_places=2, max_digits=16, verbose_name='DepositPaidPerUnitOfMeasureAmount'),
        ),
    ]

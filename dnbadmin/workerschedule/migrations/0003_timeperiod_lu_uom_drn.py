# Generated by Django 4.0.4 on 2022-07-07 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unitofmeasure', '0003_unitofmeasure_created_at_unitofmeasure_status_uom'),
        ('workerschedule', '0002_remove_timeperiod_lu_uom_drn'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeperiod',
            name='LU_UOM_DRN',
            field=models.ForeignKey(blank=True, db_column='LU_UOM_DRN', null=True, on_delete=django.db.models.deletion.CASCADE, to='unitofmeasure.unitofmeasure', verbose_name='DurationUnitOfMeasureCode'),
        ),
    ]

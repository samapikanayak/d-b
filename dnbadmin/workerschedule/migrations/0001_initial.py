# Generated by Django 4.0.4 on 2022-06-06 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('worker', '0001_initial'),
        ('store', '0001_initial'),
        ('unitofmeasure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeGroup',
            fields=[
                ('ID_GP_TM', models.BigAutoField(primary_key=True, serialize=False, verbose_name='TimeGroupID')),
                ('DE_GP_TM', models.CharField(max_length=255, verbose_name='Description')),
            ],
            options={
                'db_table': 'CO_GP_TM',
            },
        ),
        migrations.CreateModel(
            name='WorkerAvailability',
            fields=[
                ('ID_WRKR_AVLB', models.BigAutoField(primary_key=True, serialize=False, verbose_name='WorkerAvailability')),
                ('DC_EF', models.DateTimeField(verbose_name='EffectiveDate')),
                ('DC_EP', models.DateTimeField(verbose_name='ExpirationDate')),
                ('ID_GP_TM', models.ForeignKey(db_column='ID_GP_TM', on_delete=django.db.models.deletion.CASCADE, to='workerschedule.timegroup', verbose_name='TimeGroupID')),
                ('ID_LCN', models.ForeignKey(db_column='ID_LCN', on_delete=django.db.models.deletion.CASCADE, to='store.worklocation', verbose_name='LocationID')),
                ('ID_WRKR', models.ForeignKey(db_column='ID_WRKR', on_delete=django.db.models.deletion.CASCADE, to='worker.worker', verbose_name='WorkerID')),
            ],
            options={
                'db_table': 'CO_WRKR_AVLB',
            },
        ),
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('ID_PD_TM', models.BigAutoField(primary_key=True, serialize=False, verbose_name='TimePeriodID')),
                ('NM_PD_TM', models.CharField(max_length=40, verbose_name='Name')),
                ('WD', models.CharField(max_length=1, verbose_name='DayOfWeek')),
                ('TM_SRT', models.TimeField(verbose_name='StartTime')),
                ('SI_DRN', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Duration')),
                ('LU_UOM_DRN', models.ForeignKey(db_column='LU_UOM_DRN', on_delete=django.db.models.deletion.CASCADE, to='unitofmeasure.unitofmeasure', verbose_name='DurationUnitOfMeasureCode')),
            ],
            options={
                'db_table': 'CO_PD_TM',
            },
        ),
        migrations.CreateModel(
            name='TimeGroupTimePeriod',
            fields=[
                ('ID_GP_PD_TM', models.BigAutoField(primary_key=True, serialize=False, verbose_name='TimeGroupTimePeriodID')),
                ('ID_GP_TM', models.ForeignKey(db_column='ID_GP_TM', on_delete=django.db.models.deletion.CASCADE, to='workerschedule.timegroup', verbose_name='TimeGroupID')),
                ('ID_PD_TM', models.ForeignKey(db_column='ID_PD_TM', on_delete=django.db.models.deletion.CASCADE, to='workerschedule.timeperiod', verbose_name='TimePeriodID')),
            ],
            options={
                'db_table': 'CO_GP_PD_TM',
            },
        ),
    ]
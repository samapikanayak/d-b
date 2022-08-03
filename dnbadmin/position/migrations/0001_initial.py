# Generated by Django 4.0.4 on 2022-06-06 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('worker', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('ID_PST', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ContractorID')),
                ('NM_TTL', models.CharField(max_length=40, verbose_name='Title')),
                ('DE_PST', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('FL_TM_FL', models.BooleanField(default=False, verbose_name='FullTimeFlag')),
                ('FL_SLRY', models.BooleanField(default=False, verbose_name='SalaryFlag')),
                ('FL_EXM_OVR_TM', models.BooleanField(default=False, verbose_name='OvertimeExemptFlag')),
                ('FL_RTE_PNL', models.BooleanField(default=False, verbose_name='PenalRateFlag')),
                ('CD_PRD_PY', models.CharField(choices=[('hr', 'Hour'), ('wk', 'Week'), ('mn', 'Month'), ('yr', 'Year')], default='mn', max_length=2, verbose_name='PayPeriodCode')),
                ('MO_RTE_PY', models.DecimalField(blank=True, decimal_places=5, max_digits=16, null=True, verbose_name='PayRate')),
                ('CRT_DT', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('MDF_DT', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('CRT_BY', models.ForeignKey(blank=True, db_column='CRT_BY', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PST_Createuser', to=settings.AUTH_USER_MODEL)),
                ('ID_JOB', models.ForeignKey(db_column='ID_JOB', on_delete=django.db.models.deletion.CASCADE, to='job.job', verbose_name='JobID')),
                ('ID_LCN', models.ForeignKey(db_column='ID_LCN', on_delete=django.db.models.deletion.CASCADE, to='store.worklocation', verbose_name='LocationID')),
                ('MDF_BY', models.ForeignKey(blank=True, db_column='MDF_BY', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PST_Modifiyuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CO_PST',
            },
        ),
        migrations.CreateModel(
            name='WorkerPositionAssignment',
            fields=[
                ('ID_ASGMT_WRKR_PSN', models.BigAutoField(primary_key=True, serialize=False, verbose_name='WorkerPositionAssignmentID')),
                ('DC_EF', models.DateTimeField(verbose_name='EffectiveDate')),
                ('SC_EM_ASGMT', models.CharField(choices=[('hr', 'Hour'), ('wk', 'Week'), ('mn', 'Month'), ('yr', 'Year')], default='mn', max_length=2, verbose_name='StatusCode')),
                ('DC_EP', models.DateTimeField(verbose_name='ExpirationDate')),
                ('NM_TTL', models.CharField(max_length=40, verbose_name='Title')),
                ('FL_TM_FL', models.BooleanField(default=False, verbose_name='FullTimeFlag')),
                ('FL_SLRY', models.BooleanField(default=False, verbose_name='SalaryFlag')),
                ('FL_EXM_OVR_TM', models.BooleanField(default=False, verbose_name='OvertimeExemptFlag')),
                ('FL_RTE_PNL', models.BooleanField(default=False, verbose_name='PenalRateFlag')),
                ('FL_CMN', models.BooleanField(default=False, verbose_name='CommissionFlag')),
                ('CD_PRD_PY', models.CharField(choices=[('hr', 'Hour'), ('wk', 'Week'), ('mn', 'Month'), ('yr', 'Year')], default='mn', max_length=2, verbose_name='PayPeriodCode')),
                ('MO_RTE_PY', models.DecimalField(blank=True, decimal_places=5, max_digits=16, null=True, verbose_name='PayRate')),
                ('ID_PST', models.ForeignKey(db_column='ID_PST', on_delete=django.db.models.deletion.CASCADE, to='position.position', verbose_name='PositionID')),
                ('ID_WRKR', models.ForeignKey(db_column='ID_WRKR', on_delete=django.db.models.deletion.CASCADE, to='worker.worker', verbose_name='WorkerID')),
            ],
            options={
                'db_table': 'CO_ASGMT_WRKR_PSN',
            },
        ),
        migrations.CreateModel(
            name='PositionWorkSchedule',
            fields=[
                ('ID_PST_WRK_SCH', models.BigAutoField(primary_key=True, serialize=False, verbose_name='PositionWorkScheduleID')),
                ('WD_PST_WRK_SCH', models.CharField(blank=True, max_length=1, null=True, verbose_name='PositionWorkScheduleWeekDay')),
                ('TM_STR', models.TimeField(blank=True, null=True, verbose_name='StartTime')),
                ('TM_FNS', models.TimeField(blank=True, null=True, verbose_name='Description')),
                ('HH_HR', models.DecimalField(blank=True, decimal_places=3, max_digits=9, null=True, verbose_name='Hours')),
                ('ID_PST', models.ForeignKey(db_column='ID_PST', on_delete=django.db.models.deletion.CASCADE, to='position.position', verbose_name='PositionID')),
            ],
            options={
                'db_table': 'CO_SCH_PST_WRK',
            },
        ),
        migrations.CreateModel(
            name='PositionHierarchy',
            fields=[
                ('ID_HRC_PST', models.BigAutoField(primary_key=True, serialize=False, verbose_name='PositionHierarchyID')),
                ('DC_EF', models.DateTimeField(verbose_name='EffectiveDate')),
                ('DC_EX', models.DateTimeField(verbose_name='ExpirationDate')),
                ('ID_PST_SPVR', models.ForeignKey(db_column='ID_PST_SPVR', on_delete=django.db.models.deletion.CASCADE, related_name='Sup_position', to='position.position', verbose_name='Supervisor')),
                ('ID_PST_SUB', models.ForeignKey(db_column='ID_PST_SUB', on_delete=django.db.models.deletion.CASCADE, related_name='Sub_position', to='position.position', verbose_name='Subordinate')),
            ],
            options={
                'db_table': 'ST_HRC_PST',
            },
        ),
    ]

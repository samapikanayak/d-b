# Generated by Django 4.0.4 on 2022-06-06 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementSystem',
            fields=[
                ('ID_MSRMT_SYS', models.BigAutoField(primary_key=True, serialize=False, verbose_name='MeasurementSystemID')),
                ('NM_MSRMT_SYS', models.CharField(max_length=40, verbose_name='Name')),
            ],
            options={
                'db_table': 'CO_MSRMT_SYS',
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('ID_UOM', models.BigAutoField(primary_key=True, serialize=False, verbose_name='UnitOfMeasureID')),
                ('FL_UOM_ENG_MC', models.BooleanField(default=False, verbose_name='EnglishMetricFlag')),
                ('CD_UOM', models.CharField(max_length=20, verbose_name='UnitOfMeasureCode')),
                ('TY_UOM', models.CharField(max_length=20, verbose_name='UnitOfMeasureTypeCode')),
                ('NM_UOM', models.CharField(max_length=40, verbose_name='Name')),
                ('DE_UOM', models.CharField(max_length=255, verbose_name='Description')),
                ('ID_MSRMT_SYS', models.ForeignKey(db_column='ID_MSRMT_SYS', on_delete=django.db.models.deletion.CASCADE, to='unitofmeasure.measurementsystem', verbose_name='MeasurementSystemID')),
            ],
            options={
                'db_table': 'CO_UOM',
            },
        ),
    ]

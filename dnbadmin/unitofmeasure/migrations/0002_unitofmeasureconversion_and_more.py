# Generated by Django 4.0.4 on 2022-07-06 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unitofmeasure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitOfMeasureConversion',
            fields=[
                ('ID_CVN_UOM', models.BigAutoField(primary_key=True, serialize=False, verbose_name='UnitOfMeasureConversionID')),
                ('MO_UOM_CVN', models.DecimalField(blank=True, decimal_places=3, max_digits=9, null=True, verbose_name='Quantity')),
                ('DE_CVN_RUL', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
            ],
            options={
                'db_table': 'CO_CVN_UOM',
            },
        ),
        migrations.RemoveField(
            model_name='unitofmeasure',
            name='ID_MSRMT_SYS',
        ),
        migrations.DeleteModel(
            name='MeasurementSystem',
        ),
        migrations.AddField(
            model_name='unitofmeasureconversion',
            name='ID_CVN_UOM_FM',
            field=models.ForeignKey(blank=True, db_column='CD_CVN_UOM_FM', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uom_conversion_fm', to='unitofmeasure.unitofmeasure'),
        ),
        migrations.AddField(
            model_name='unitofmeasureconversion',
            name='ID_CVN_UOM_TO',
            field=models.ForeignKey(blank=True, db_column='CD_CVN_UOM_TO', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uom_conversion_to', to='unitofmeasure.unitofmeasure'),
        ),
    ]

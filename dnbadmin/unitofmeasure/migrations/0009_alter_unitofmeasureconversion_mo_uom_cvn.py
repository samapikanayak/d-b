# Generated by Django 4.0.4 on 2022-07-25 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitofmeasure', '0008_alter_unitofmeasure_status_uom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitofmeasureconversion',
            name='MO_UOM_CVN',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Quantity'),
        ),
    ]
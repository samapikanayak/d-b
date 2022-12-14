# Generated by Django 4.0.4 on 2022-07-07 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitofmeasure', '0005_unitofmeasure_created_at_unitofmeasure_status_uom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitofmeasure',
            name='DE_UOM',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='unitofmeasure',
            name='NM_UOM',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='unitofmeasure',
            name='TY_UOM',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='UnitOfMeasureTypeCode'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-16 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('worker', '0003_manufacturer'),
        ('party', '0002_externalpartyidentificationprovider_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('NM_BRN', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='BrandName')),
                ('DE_BRN', models.CharField(max_length=255, verbose_name='Description')),
                ('CD_BRN_GRDG', models.CharField(max_length=20, verbose_name='BrandGrade')),
                ('ID_PRTY', models.ForeignKey(db_column='ID_PRTY', on_delete=django.db.models.deletion.CASCADE, to='party.party', verbose_name='Party ID')),
            ],
            options={
                'db_table': 'ID_BRN',
            },
        ),
        migrations.CreateModel(
            name='SubBrand',
            fields=[
                ('AI_SUB_BRN', models.BigAutoField(primary_key=True, serialize=False, verbose_name='SubBrandSequenceNumber')),
                ('NM_SUB_BRN', models.CharField(max_length=40, verbose_name='SubBrandName')),
                ('DE_SUB_BRN', models.CharField(max_length=255, verbose_name='Description')),
                ('NM_BRN', models.ForeignKey(db_column='NM_BRN', on_delete=django.db.models.deletion.CASCADE, to='brand.brand', verbose_name='BrandName')),
            ],
            options={
                'db_table': 'ID_SUB_BRN',
            },
        ),
        migrations.CreateModel(
            name='ManufacturerBrand',
            fields=[
                ('ID_ID_BRN_MF', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ManufacturerBrandID')),
                ('DC_EF', models.DateTimeField(verbose_name='EffectiveDate')),
                ('DC_EP', models.DateTimeField(verbose_name='ExpirationDate')),
                ('CD_STS', models.CharField(max_length=2, verbose_name='CurrentStatusCode')),
                ('ID_MF', models.ForeignKey(db_column='ID_MF', on_delete=django.db.models.deletion.CASCADE, to='worker.manufacturer', verbose_name='ManufacturerID')),
                ('NM_BRN', models.ForeignKey(db_column='NM_BRN', on_delete=django.db.models.deletion.CASCADE, to='brand.brand', verbose_name='BrandName')),
            ],
            options={
                'db_table': 'ID_BRN_MF',
            },
        ),
    ]

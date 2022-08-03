# Generated by Django 4.0.4 on 2022-06-06 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('party', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('ID_BSN_UN', models.BigAutoField(primary_key=True, serialize=False, verbose_name='BusinessUnitID')),
                ('TY_BSN_UN', models.CharField(choices=[], max_length=2, verbose_name='TypeCode')),
                ('NM_BSN_UN', models.CharField(max_length=40, verbose_name='Name')),
            ],
            options={
                'db_table': 'LO_BSN_UN',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('ID_CNY', models.BigAutoField(primary_key=True, serialize=False, verbose_name='CurrencyID')),
                ('DE_CNY', models.CharField(max_length=255, verbose_name='Description')),
                ('SY_CNY', models.CharField(max_length=40, verbose_name='Symbol')),
                ('CD_ISO4217_CNY', models.CharField(max_length=4, verbose_name='ISO4217CurrencyCode')),
            ],
            options={
                'db_table': 'CO_CNY',
            },
        ),
        migrations.CreateModel(
            name='WorkLocation',
            fields=[
                ('ID_LCN', models.BigAutoField(primary_key=True, serialize=False, verbose_name='LocationID')),
                ('ID_BSN_UN', models.ForeignKey(db_column='ID_BSN_UN', on_delete=django.db.models.deletion.CASCADE, to='store.businessunit', verbose_name='BusinessUnitID')),
            ],
            options={
                'db_table': 'LO_LCN_WRK',
            },
        ),
        migrations.CreateModel(
            name='ISO4217_CurrencyType',
            fields=[
                ('CD_CNY_ISO_4217', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='ISOCurrencyCode')),
                ('CD_CNY_ISO_4217_NBR', models.CharField(max_length=3, verbose_name='ISOCurrencyNumber')),
                ('NM_CNY', models.CharField(max_length=40, verbose_name='ISOCurrencyName')),
                ('CD_CY_RTLR_TYP', models.CharField(blank=True, max_length=20, null=True, verbose_name='RetailerAssignedCurrencyTypeCode')),
                ('SY_CNY', models.CharField(blank=True, max_length=40, null=True, verbose_name='Symbol')),
                ('CD_CY_ISO', models.ForeignKey(db_column='CD_CY_ISO', on_delete=django.db.models.deletion.CASCADE, to='party.iso3166_1country', verbose_name='ISOCountryCode')),
            ],
            options={
                'db_table': 'LU_CNY_ISO_4217',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnitGroup',
            fields=[
                ('ID_BSNGP', models.BigAutoField(primary_key=True, serialize=False, verbose_name='BusinessUnitGroupID')),
                ('NM_BSNGP', models.CharField(max_length=40, verbose_name='BusinessUnitGroupName')),
                ('ID_LGE', models.ForeignKey(db_column='ID_LGE', on_delete=django.db.models.deletion.CASCADE, to='party.language', verbose_name='LanguageID')),
            ],
            options={
                'db_table': 'CO_BSNGP',
            },
        ),
        migrations.AddField(
            model_name='businessunit',
            name='CD_CNY_ISO_4217',
            field=models.ForeignKey(db_column='CD_CNY_ISO_4217', on_delete=django.db.models.deletion.CASCADE, to='store.iso4217_currencytype', verbose_name='ISOCurrencyCode'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='ID_BSNGP',
            field=models.ForeignKey(db_column='ID_BSNGP', on_delete=django.db.models.deletion.CASCADE, to='store.businessunitgroup', verbose_name='BusinessUnitGroupID'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='ID_CNY_LCL',
            field=models.ForeignKey(db_column='ID_CNY_LCL', on_delete=django.db.models.deletion.CASCADE, to='store.currency', verbose_name='Local'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='ID_OPR_PRTY',
            field=models.ForeignKey(db_column='ID_OPR_PRTY', on_delete=django.db.models.deletion.CASCADE, to='party.operationalparty', verbose_name='OperationalPartyID'),
        ),
    ]

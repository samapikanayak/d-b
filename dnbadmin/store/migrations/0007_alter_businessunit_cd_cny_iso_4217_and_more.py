# Generated by Django 4.0.4 on 2022-06-30 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_alter_iso3166_1country_options_and_more'),
        ('store', '0006_alter_businessunitgrouplevel_id_bsngp_lv_prnt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessunit',
            name='CD_CNY_ISO_4217',
            field=models.ForeignKey(blank=True, db_column='CD_CNY_ISO_4217', null=True, on_delete=django.db.models.deletion.CASCADE, to='store.iso4217_currencytype', verbose_name='ISOCurrencyCode'),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='ID_CNY_LCL',
            field=models.ForeignKey(blank=True, db_column='ID_CNY_LCL', null=True, on_delete=django.db.models.deletion.CASCADE, to='store.currency', verbose_name='Local'),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='ID_OPR_PRTY',
            field=models.ForeignKey(blank=True, db_column='ID_OPR_PRTY', null=True, on_delete=django.db.models.deletion.CASCADE, to='party.operationalparty', verbose_name='OperationalPartyID'),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='TY_BSN_UN',
            field=models.CharField(max_length=2, verbose_name='TypeCode'),
        ),
    ]

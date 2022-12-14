# Generated by Django 4.0.4 on 2022-07-08 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depositrule', '0005_rename_mo_ds_depositrule_deposit_amount_and_more'),
        ('sellingrule', '0006_alter_itemsellingrule_item_tender_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsellingrule',
            name='deposit_rule',
            field=models.ForeignKey(db_column='ID_RU_DS', on_delete=django.db.models.deletion.CASCADE, to='depositrule.depositrule', verbose_name='DepositRuleID '),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='item_tender_group',
            field=models.ForeignKey(db_column='LU_GP_TND_RST', on_delete=django.db.models.deletion.CASCADE, to='sellingrule.itemtenderrestrictiongroup', verbose_name='ItemTenderRestrictionGroupCode'),
        ),
    ]

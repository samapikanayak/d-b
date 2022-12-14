# Generated by Django 4.0.4 on 2022-07-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellingrule', '0002_rename_de_gp_tnd_rst_itemtenderrestrictiongroup_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemsellingrule',
            old_name='ID_RU_DS',
            new_name='deposit_rule',
        ),
        migrations.RenameField(
            model_name='itemsellingrule',
            old_name='LU_GP_TND_RST',
            new_name='item_tender_group',
        ),
        migrations.RenameField(
            model_name='itemtenderrestrictiongroup',
            old_name='description',
            new_name='selling_rule_description',
        ),
        migrations.RenameField(
            model_name='itemtenderrestrictiongroup',
            old_name='name',
            new_name='selling_rule_name',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='DC_ITM_SLS',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='FL_CPN_ELTNC',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='FL_CPN_RST',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='FL_ENR_PRC_RQ',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='FL_ENT_WT_RQ',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='QU_MNM_SLS_UN',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='QU_UN_BLK_MXM',
        ),
        migrations.RemoveField(
            model_name='itemsellingrule',
            name='SC_ITM_SLS',
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='coupon',
            field=models.IntegerField(null=True, verbose_name='CouponRestrictedFlag'),
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='electronic_coupon',
            field=models.IntegerField(null=True, verbose_name='ElectronicCouponFlag'),
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='maximum_sale_unit',
            field=models.DecimalField(decimal_places=0, max_digits=3, null=True, verbose_name='MaximumSaleUnitCount'),
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='minimum_sale_unit',
            field=models.DecimalField(decimal_places=0, max_digits=3, null=True, verbose_name='MinimumSaleUnitCount'),
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='price_entry',
            field=models.IntegerField(null=True, verbose_name='PriceEntryRequiredFlag'),
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='selling_status_effective_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='SellingStatusCodeEffectiveDate'),
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='selling_status_expire_date',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='SellingStatusCodeEffectiveDate'),
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('I', 'Inactive')], default=1, max_length=2, verbose_name='Status Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemsellingrule',
            name='weight_entry',
            field=models.IntegerField(null=True, verbose_name='WeightEntryRequiredFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='CD_QTY_ACTN_KY',
            field=models.CharField(max_length=2, null=True, verbose_name='QuantityKeyActionCode'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_CPN_ALW_MULTY',
            field=models.IntegerField(null=True, verbose_name='AllowCouponMultiplyFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_DSC_EM_ALW',
            field=models.IntegerField(null=True, verbose_name='EmployeeDiscountAllowedFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_FD_STP_ALW',
            field=models.IntegerField(null=True, verbose_name='AllowFoodStampFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_ITM_GWY',
            field=models.IntegerField(null=True, verbose_name='GiveawayFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_ITM_WIC',
            field=models.IntegerField(null=True, verbose_name='WICFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_KY_PRH_RPT',
            field=models.IntegerField(null=True, verbose_name='ProhibitRepeatKeyFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_PNT_FQ_SHPR',
            field=models.IntegerField(null=True, verbose_name='FrequentShopperPointsEligibilityFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_PRC_VS_VR',
            field=models.IntegerField(null=True, verbose_name='VisualVerifyPriceFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_PRPPRTNL_RFD_EL',
            field=models.IntegerField(null=True, verbose_name='ProportionalRefundEligibleFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_RNCHK_EL',
            field=models.IntegerField(null=True, verbose_name='RaincheckEligibleFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='FL_RTN_PRH',
            field=models.IntegerField(null=True, verbose_name='ProhibitReturnFlag'),
        ),
        migrations.AlterField(
            model_name='itemsellingrule',
            name='QU_PNT_FQ_SHPR',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, verbose_name='FrequentShopperPointsCount'),
        ),
    ]

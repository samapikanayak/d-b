'''Selling rule Models'''
from datetime import datetime
from django.db import models
from depositrule.models import DepositRule


# Create your models here.

class ItemTenderRestrictionGroup(models.Model):
    '''Item Tender Model'''
    LU_GP_TND_RST = models.BigAutoField(
        "ItemTenderRestrictionGroupCode", primary_key=True)
    DE_GP_TND_RST = models.CharField("Description", max_length=255)
    NA_GP_TND_RST = models.CharField("Name", max_length=40)

    class Meta:
        '''Item Tender Meta class'''
        db_table = 'CO_RST_ITM_TND'


STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class ItemSellingRule(models.Model):
    '''Item Selling Rule'''
    ID_RU_ITM_SL = models.BigAutoField("ItemSellingRuleID", primary_key=True)
    # LU_GP_TND_RST = models.ForeignKey(ItemTenderRestrictionGroup, on_delete=models.CASCADE, verbose_name="ItemTenderRestrictionGroupCode",db_column="LU_GP_TND_RST")  # NOSONAR
    # FC_FMY_MF = models.ForeignKey(ManufacturerCouponFamily, on_delete=models.CASCADE, verbose_name="ManufacturerFamilyCode",db_column="FC_FMY_MF")  # NOSONAR
    NM_RU_ITM_SL = models.CharField("Title", max_length=40, null=True)
    DE_RU_ITM_SL = models.CharField("Description", max_length=255, null=True)
    ID_RU_DS = models.ForeignKey(
        DepositRule, on_delete=models.CASCADE, verbose_name="DepositRuleID ", db_column="ID_RU_DS")
    SC_ITM_SLS = models.CharField("Status Code", max_length=2, default="")
    DC_ITM_SLS = models.DateTimeField(
        "SellingStatusCodeEffectiveDate", null=True, blank=True)
    expired_date = models.DateTimeField(
        "ExpiredDate", null=True, blank=True)
    FL_CPN_RST = models.IntegerField("CouponRestrictedFlag", null=True)
    FL_CPN_ELTNC = models.IntegerField("ElectronicCouponFlag", null=True)
    FL_ENR_PRC_RQ = models.IntegerField("PriceEntryRequiredFlag", null=True)
    FL_ENT_WT_RQ = models.IntegerField("WeightEntryRequiredFlag", null=True)
    FL_DSC_EM_ALW = models.IntegerField(
        "EmployeeDiscountAllowedFlag", null=True)
    FL_FD_STP_ALW = models.IntegerField("AllowFoodStampFlag", null=True)
    FL_CPN_ALW_MULTY = models.IntegerField(
        "AllowCouponMultiplyFlag", null=True)
    QU_MNM_SLS_UN = models.DecimalField(
        "MinimumSaleUnitCount", max_digits=3, decimal_places=0, default=2)
    QU_UN_BLK_MXM = models.DecimalField(
        "MaximumSaleUnitCount", max_digits=3, decimal_places=0, default=2)
    FL_KY_PRH_RPT = models.IntegerField("ProhibitRepeatKeyFlag", null=True)
    FL_PRC_VS_VR = models.IntegerField("VisualVerifyPriceFlag", null=True)
    FL_PNT_FQ_SHPR = models.IntegerField(
        "FrequentShopperPointsEligibilityFlag", null=True)
    QU_PNT_FQ_SHPR = models.DecimalField(
        "FrequentShopperPointsCount", max_digits=9, decimal_places=3, null=True)
    CD_QTY_ACTN_KY = models.CharField(
        "QuantityKeyActionCode", max_length=2, null=True)
    FL_RTN_PRH = models.IntegerField("ProhibitReturnFlag", null=True)
    FL_ITM_WIC = models.IntegerField("WICFlag", null=True)
    FL_ITM_GWY = models.IntegerField("GiveawayFlag", null=True)
    # ID_MF = models.ForeignKey(ManufacturerCouponFamily, on_delete=models.CASCADE, verbose_name="ManufacturerID",related_name="ID_MFA",db_column="ID_MF")  # NOSONAR
    FL_RNCHK_EL = models.IntegerField("RaincheckEligibleFlag", null=True)
    FL_PRPPRTNL_RFD_EL = models.IntegerField(
        "ProportionalRefundEligibleFlag", null=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default="A")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        '''Item Selling meta class'''
        db_table = 'ID_RU_ITM_SL'

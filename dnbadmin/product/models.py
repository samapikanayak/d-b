'''product model'''
import uuid
from django.db import models
from sellingrule.models import ItemSellingRule
from store.models import BusinessUnitGroup
from taxonomy.models import MerchandiseHierarchyGroup
from brand.models import Brand, SubBrand


# Create your models here.

STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class ItemSellingPrices(models.Model):
    ID_ITM_SL_PRC = models.BigAutoField(
        "ItemSellingPricesID", primary_key=True)
    RP_PR_SLS = models.DecimalField(
        "PermanentSaleUnitRetailPriceAmount", max_digits=7, decimal_places=2, null=True, blank=True)
    FL_MKD_ORGL_PRC_PR = models.IntegerField(
        "PermanentSaleUnitRetailPriceOriginalMarkdownFlag", null=True, blank=True)
    QU_MKD_PR_PRC_PR = models.DecimalField(
        "PermanentRetailPricePermanentMarkdownCount", max_digits=7, decimal_places=0, null=True, blank=True)
    DC_PRC_EF_PRN_RT = models.DateTimeField(
        "PermanentRetailPriceEffectiveDate", null=True, blank=True)
    RP_SLS_CRT = models.DecimalField(
        "CurrentSaleUnitRetailPriceAmount", max_digits=7, decimal_places=2, null=True, blank=True)
    TY_PRC_RT = models.CharField(
        "CurrentSaleUnitRetailPriceTypeCode", max_length=2, null=True, blank=True)
    FL_PRC_RT_PNT_ALW = models.IntegerField(
        "CurrentSaleUnitRetailPricePointAllowedFlag", null=True, blank=True)
    DC_PRC_SLS_EF_CRT = models.DateTimeField(
        "CurrentSaleUnitRetailPriceEffectiveDate", null=True, blank=True)
    DC_PRC_SLS_EP_CRT = models.DateTimeField(
        "CurrentSaleUnitRetailPriceExpirationDate", null=True, blank=True)
    RP_PRC_MF_RCM_RT = models.DecimalField(
        "ManufacturerSaleUnitRecommendedRetailPriceAmount", max_digits=7, decimal_places=2, null=True, blank=True)
    DC_PRC_MF_RCM_RT = models.DateTimeField(
        "ManufacturerSaleUnitRecommendedRetailPriceEffectiveDate", null=True, blank=True)
    RP_PRC_CMPR_AT_SLS = models.DecimalField(
        "CompareAtSaleUnitRetailPriceAmount", max_digits=7, decimal_places=2, null=True, blank=True)
    FL_QTY_PRC = models.IntegerField(
        "QuantityPricingFlag", null=True, blank=True)
    QU_PCKG_PRC_CRT = models.DecimalField(
        "CurrentPackagePriceQuantity", max_digits=3, decimal_places=0, null=True, blank=True)
    RP_PCKG_PRC_CRT = models.DecimalField(
        "CurrentPackagePrice", max_digits=7, decimal_places=2, null=True, blank=True)
    QU_PCKG_PRC_PRN = models.DecimalField(
        "PermanentPackagePriceQuantity", max_digits=3, decimal_places=0, null=True, blank=True)
    RP_PCKG_PRC_PRN = models.DecimalField(
        "PermanentPackagePrice", max_digits=7, decimal_places=2, null=True, blank=True)
    RP_RTN_UN_PRN_SLS = models.DecimalField(
        "PermanentSaleUnitReturnPrice", max_digits=7, decimal_places=2, null=True, blank=True)
    RP_RTN_UN_CRT_SLS = models.DecimalField(
        "CurrentSaleUnitReturnPrice", max_digits=7, decimal_places=2, null=True, blank=True)
    FL_TX_INC = models.IntegerField(
        "IncludesSalesTaxFlag", null=True, blank=True)
    MO_AMT_TX_PRN = models.DecimalField(
        "PermanentSalesTaxAmount", max_digits=7, decimal_places=2, null=True, blank=True)
    MO_AMT_TX_CRT = models.DecimalField(
        "CurrentSalesTaxAmount", max_digits=7, decimal_places=2, null=True, blank=True)
    RP_MNM_ADVRTSD = models.DecimalField(
        "MinimumAdvertisedRetailUnitPrice", max_digits=7, decimal_places=2, null=True, blank=True)
    DC_EF_RP_MNM_ADVRTSD = models.DateTimeField(
        "MinimumAdvertisedRetailUnitPriceEffectiveDate")
    ITM_SL_PRC_STATUS = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="Item Selling Price Rule (Active/Inactive)",
    )
    ITM_SL_PRC_NAME = models.CharField("ItemSellingPriceRuleName",
                                       max_length=100,
                                       null=True,
                                       blank=True
                                       )

    class Meta:
        db_table = ' RU_ITM_SL_PRC'


class PriceLine(models.Model):
    ID_LN_PRC = models.BigAutoField("PriceLineID", primary_key=True)
    ID_MRHRC_GP = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                    verbose_name="MerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP")
    LL_LN_PRC = models.DecimalField(
        "LowAmount", max_digits=16, decimal_places=5)
    UL_LN_PRC = models.DecimalField(
        "HighAmount", max_digits=16, decimal_places=5)

    class Meta:
        db_table = 'AS_LN_PRC'


class POSDepartment(models.Model):
    ID_DPT_PS = models.BigAutoField("POSDepartmentID", primary_key=True)
    ID_RU_ITM_SL = models.ForeignKey(
        ItemSellingRule, on_delete=models.CASCADE, verbose_name="ItemSellingRuleID", db_column="ID_RU_ITM_SL", blank=True, null=True)
    ID_DPT_PS_PRNT = models.ForeignKey(
        'self', on_delete=models.CASCADE, verbose_name="ParentPOSDepartmentID", db_column="ID_DPT_PS_PRNT", null=True)
    NM_DPT_PS = models.CharField("Name", max_length=40)
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'ID_DPT_PS'


class Item(models.Model):
    ID_ITM = models.UUIDField(
        "ItemID", primary_key=True, default=uuid.uuid4, editable=False)
    ID_MRHRC_GP = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                    verbose_name="MerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP")
    ID_ITM_SL_PRC = models.ForeignKey(ItemSellingPrices, on_delete=models.CASCADE,
                                      verbose_name="ItemSellingPricesID", db_column="ID_ITM_SL_PRC")
    ID_RU_ITM_SL = models.ForeignKey(
        ItemSellingRule, on_delete=models.CASCADE, verbose_name="ItemSellingRuleID", db_column="ID_RU_ITM_SL")
    ID_DPT_PS = models.ForeignKey(
        POSDepartment, on_delete=models.CASCADE, verbose_name="POSDepartmentID", db_column="ID_DPT_PS")
    ID_LN_PRC = models.ForeignKey(
        PriceLine, on_delete=models.CASCADE, verbose_name="PriceLineID", db_column="ID_LN_PRC")
    NM_BRN = models.ForeignKey(Brand, on_delete=models.CASCADE,
                               verbose_name="BrandName", db_column="NM_BRN", null=True)
    FL_AZN_FR_SLS = models.IntegerField("AuthorizedForSaleFlag")
    FL_ITM_DSC = models.IntegerField("DiscountFlag")
    FL_ADT_ITM_PRC = models.IntegerField("PriceAuditFlag")
    LU_EXM_TX = models.CharField("TaxExemptCode", max_length=2)
    LU_ITM_USG = models.CharField("UsageCode", max_length=2)
    NM_ITM = models.CharField("Name", max_length=40)
    DE_ITM = models.CharField("Description", max_length=255)
    DE_ITM_LNG = models.TextField("LongDescription")
    TY_ITM = models.CharField("TypeCode", max_length=4)
    LU_KT_ST = models.CharField("KitSetCode", max_length=2)
    FL_ITM_SBST_IDN = models.IntegerField("SubstituteIdentifiedFlag")
    LU_CLN_ORD = models.CharField("OrderCollectionCode", max_length=2)
    FL_VLD_SRZ_ITM = models.IntegerField("SerializedIUnitValidationFlag")
    AI_SUB_BRN = models.ForeignKey(SubBrand, on_delete=models.CASCADE,
                                   verbose_name="SubBrand sequence number", db_column="AI_SUB_BRN", null=True)
    NM_BRN_SUB_BRN = models.CharField("SubBrand Name", max_length=40)

    class Meta:
        db_table = 'AS_ITM'


class BusinessUnitGroupItem(models.Model):
    ID_BSNGP_ITM = models.BigAutoField(
        "BusinessUnitGroupItemID", primary_key=True)
    ID_BSNGP = models.ForeignKey(BusinessUnitGroup, on_delete=models.CASCADE,
                                 verbose_name="BusinessUnitGroupID", db_column="ID_BSNGP")
    ID_ITM = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name="ItemID", db_column="ID_ITM")
    TS_EF = models.DateTimeField("EffectiveDateTime")
    TS_EP = models.DateTimeField("ExpirationDateTime")
    ID_ITM_SL_PRC = models.ForeignKey(ItemSellingPrices, on_delete=models.CASCADE,
                                      verbose_name="ItemSellingPricesID", db_column="ID_ITM_SL_PRC")
    ID_RU_ITM_SL = models.ForeignKey(
        ItemSellingRule, on_delete=models.CASCADE, verbose_name="ItemSellingRuleID", db_column="ID_RU_ITM_SL")
    SC_ITM_SLS = models.CharField("SellingStatusCode", max_length=2)
    SC_ITM = models.CharField("StatusCode", max_length=2)
    DC_ITM_SLS = models.DateTimeField(
        "SellingStatusCodeEffectiveDate", null=True)
    FL_STK_UPDT_ON_HD = models.IntegerField("UpdateStockOnHandFlag")

    class Meta:
        db_table = 'AS_BSNGP_ITM'

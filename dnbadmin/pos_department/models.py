'''pos model'''
from django.db import models
from product.models import POSDepartment, ItemSellingPrices
from sellingrule.models import ItemSellingRule
from store.models import BusinessUnitGroup

# Create your models here.


class BusinessUnitGroupPOSDepartment(models.Model):
    '''pos association with business unit group'''
    ID_BSNGP_DPT_PS = models.BigAutoField(
        "BusinessUnitGroupPOSDepartmentID", primary_key=True)
    ID_BSNGP = models.ForeignKey(BusinessUnitGroup, on_delete=models.CASCADE,
                                 verbose_name="BusinessUnitGroupID", db_column="ID_BSNGP")
    ID_DPT_PS = models.ForeignKey(
        POSDepartment, on_delete=models.CASCADE, verbose_name="POSDepartmentID", db_column="ID_DPT_PS")
    TS_EF = models.DateTimeField("EffectiveDateTime", null=True, blank=True)
    TS_EP = models.DateTimeField("ExpirationDateTime", null=True, blank=True)
    ID_RU_ITM_SL = models.ForeignKey(
        ItemSellingRule, on_delete=models.CASCADE, verbose_name="ItemSellingRuleID", db_column="ID_RU_ITM_SL", null=True, blank=True)
    ID_ITM_SL_PRC = models.ForeignKey(ItemSellingPrices, on_delete=models.CASCADE,
                                      verbose_name="ItemSellingPricesID", db_column="ID_ITM_SL_PRC", null=True, blank=True)
    NM_DPT_POS = models.CharField(
        "Name", max_length=40, help_text="The title or label given to a point-of-sale department.", null=True, blank=True)

    class Meta:
        db_table = 'CO_BSNGP_DPT_PS'

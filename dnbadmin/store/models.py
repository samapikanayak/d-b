from django.db import models
from party.models import Language, ISO3166_1Country, OperationalParty

STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)
# Create your models here.
TYPE_OF_BUSINESSUNIT = ()


class Currency(models.Model):
    ID_CNY = models.BigAutoField("CurrencyID", primary_key=True)
    DE_CNY = models.CharField("Description", max_length=255)
    SY_CNY = models.CharField("Symbol", max_length=40)
    CD_ISO4217_CNY = models.CharField("ISO4217CurrencyCode", max_length=4)

    class Meta:
        db_table = 'CO_CNY'

    def __unicode__(self):
        return self.CD_ISO4217_CNY


class ISO4217_CurrencyType(models.Model):
    CD_CNY_ISO_4217 = models.CharField(
        "ISOCurrencyCode", primary_key=True, max_length=3)
    CD_CNY_ISO_4217_NBR = models.CharField("ISOCurrencyNumber", max_length=3)
    NM_CNY = models.CharField("ISOCurrencyName", max_length=40)
    CD_CY_ISO = models.ForeignKey(ISO3166_1Country, on_delete=models.CASCADE,
                                  verbose_name="ISOCountryCode", db_column="CD_CY_ISO")
    CD_CY_RTLR_TYP = models.CharField(
        "RetailerAssignedCurrencyTypeCode", max_length=20, blank=True, null=True)
    SY_CNY = models.CharField("Symbol", max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'LU_CNY_ISO_4217'

    def __unicode__(self):
        return self.NM_CNY


class BusinessUnitGroup(models.Model):
    ID_BSNGP = models.BigAutoField("BusinessUnitGroupID", primary_key=True)
    ID_LGE = models.ForeignKey(
        Language, on_delete=models.CASCADE, verbose_name="LanguageID", db_column="ID_LGE")
    NM_BSNGP = models.CharField("BusinessUnitGroupName", max_length=40)

    class Meta:
        db_table = 'CO_BSNGP'

    def __unicode__(self):
        return self.NM_BSNGP


class BusinessUnit(models.Model):
    ID_BSN_UN = models.BigAutoField("BusinessUnitID", primary_key=True)
    ID_BSNGP = models.ForeignKey(BusinessUnitGroup, on_delete=models.CASCADE,
                                 verbose_name="BusinessUnitGroupID", db_column="ID_BSNGP")
    TY_BSN_UN = models.CharField(
        "TypeCode", max_length=2)
    NM_BSN_UN = models.CharField("Name", max_length=40)
    ID_CNY_LCL = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                   verbose_name="Local", db_column="ID_CNY_LCL", blank=True, null=True)
    CD_CNY_ISO_4217 = models.ForeignKey(ISO4217_CurrencyType, on_delete=models.CASCADE,
                                        verbose_name="ISOCurrencyCode", db_column="CD_CNY_ISO_4217", blank=True, null=True)
    ID_OPR_PRTY = models.ForeignKey(OperationalParty, on_delete=models.CASCADE,
                                    verbose_name="OperationalPartyID", db_column="ID_OPR_PRTY", blank=True, null=True)

    class Meta:
        db_table = 'LO_BSN_UN'

    def __unicode__(self):
        return self.TY_BSN_UN


class WorkLocation(models.Model):
    ID_LCN = models.BigAutoField("LocationID", primary_key=True)
    ID_BSN_UN = models.ForeignKey(
        BusinessUnit, on_delete=models.CASCADE, verbose_name="BusinessUnitID", db_column="ID_BSN_UN")

    class Meta:
        db_table = 'LO_LCN_WRK'

    def __unicode__(self):
        return self.ID_LCN


class BusinessUnitGroupFunction(models.Model):
    ID_BSNGP_FNC = models.BigAutoField(
        "BusinessUnitGroupFunctionID", primary_key=True)
    NM_BSNGP_FNC = models.CharField(
        "BusinessUnitGroupFunctionName", max_length=40)

    class Meta:
        db_table = 'CO_BSNGP_FNC'


class BusinessUnitGroupLevel(models.Model):
    ID_BSNGP_LV = models.BigAutoField(
        "BusinessUnitGroupLevelID", primary_key=True)
    # ID_BSNGP_FNC = models.ForeignKey('self', on_delete=models.CASCADE,verbose_name="BusinessUnitGroupFunctionID",related_name='BSNGP_FNC',db_column="ID_BSNGP_FNC")  # NOSONAR
    ID_BSNGP_FNC = models.ForeignKey(BusinessUnitGroupFunction, on_delete=models.CASCADE,
                                     verbose_name="BusinessUnitGroupFunctionID", db_column="ID_BSNGP_FNC")
    ID_BSNGP_LV_PRNT = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="BusinessUnitCenterGroupLevelID ",
                                         related_name='BSNGP_LV', db_column="ID_BSNGP_LV_PRNT", null=True)
    NM_BSNGP_LV = models.CharField("BusinessUnitGroupLevelName", max_length=40)

    class Meta:
        db_table = 'CO_BSNGP_LV'


class AssociatedBusinessUnitGroup(models.Model):
    ID_ASCTN_BSNGP = models.BigAutoField(
        "AssociatedBusinessUnitGroupID", primary_key=True)
    ID_BSNGP_FNC = models.ForeignKey(BusinessUnitGroupFunction, on_delete=models.CASCADE,
                                     verbose_name="BusinessUnitGroupFunctionID", db_column="ID_BSNGP_FNC")
    ID_BSNGP_LV = models.ForeignKey(BusinessUnitGroupLevel, on_delete=models.CASCADE,
                                    verbose_name="ParentBusinessUnitGroupLevelID", db_column="ID_BSNGP_LV")
    ID_BSNGP_PRNT = models.ForeignKey(BusinessUnitGroup, on_delete=models.CASCADE,
                                      verbose_name="ParentBusinessUnitGroupID", related_name='BSNGP_PRNT', db_column="ID_BSNGP_PRNT")
    ID_BSNGP_CHLD = models.ForeignKey(BusinessUnitGroup, on_delete=models.CASCADE,
                                      verbose_name="ChildBusinessUnitGroupID", related_name='BSNGP_CHLD', db_column="ID_BSNGP_CHLD")
    DC_EF = models.DateTimeField("EffectiveDate")
    DC_EP = models.DateTimeField("ExpirationDate")

    class Meta:
        db_table = 'ST_ASCTN_BSNGP'

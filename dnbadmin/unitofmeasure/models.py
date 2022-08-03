''' Unit Of Measure Model '''
from django.db import models

# Create your models here.
STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class UnitOfMeasure(models.Model):
    ''' Unit Of Measure Model Class '''
    ID_UOM = models.BigAutoField("UnitOfMeasureID", primary_key=True)
    FL_UOM_ENG_MC = models.BooleanField("EnglishMetricFlag", default=False)
    CD_UOM = models.CharField("UnitOfMeasureCode", max_length=20)
    TY_UOM = models.CharField("UnitOfMeasureTypeCode",
                              null=True, blank=True, max_length=20)
    NM_UOM = models.CharField("Name",  null=True, blank=True, max_length=40)
    DE_UOM = models.CharField(
        "Description",  null=True, blank=True, max_length=255)
    STATUS_UOM = models.CharField(
        "UnitOfMeasure Staus", max_length=2, choices=STATUS_CHOICES)
    CREATED_AT = models.DateTimeField(
        "UnitOfMeasure Created At", null=True, blank=True, auto_now_add=True)

    class Meta:
        ''' This is a Meta Class'''
        db_table = 'CO_UOM'

    def __unicode__(self):
        return self.CD_UOM


class UnitOfMeasureConversion(models.Model):
    ''' Unit Of Measure Conversion Model Class '''
    ID_CVN_UOM = models.BigAutoField(
        "UnitOfMeasureConversionID", primary_key=True)
    ID_CVN_UOM_FM = models.ForeignKey(
        UnitOfMeasure, on_delete=models.SET_NULL, blank=True, null=True, related_name="uom_conversion", db_column="CD_CVN_UOM_FM")
    ID_CVN_UOM_TO = models.ForeignKey(
        UnitOfMeasure, on_delete=models.SET_NULL, blank=True, null=True, related_name="uom_conversion_to", db_column="CD_CVN_UOM_TO")
    MO_UOM_CVN = models.DecimalField(
        "Quantity", max_digits=9, decimal_places=2, blank=True, null=True)
    DE_CVN_RUL = models.CharField(
        "Description", max_length=255, blank=True, null=True)

    class Meta:
        ''' This is a Meta Class'''
        db_table = 'CO_CVN_UOM'

    def __unicode__(self):
        return self.ID_CVN_UOM

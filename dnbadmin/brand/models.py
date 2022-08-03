from django.db import models
from worker.models import Manufacturer
from party.models import Party

# Create your models here.
class Brand(models.Model):
    NM_BRN = models.CharField("BrandName",max_length=40, primary_key=True)
    ID_PRTY = models.ForeignKey(Party, on_delete=models.CASCADE,verbose_name="Party ID",db_column="ID_PRTY")
    DE_BRN = models.CharField("Description", max_length=255)
    CD_BRN_GRDG  = models.CharField("BrandGrade", max_length=20)

    class Meta:
        db_table = 'ID_BRN'

class SubBrand(models.Model):
    AI_SUB_BRN = models.BigAutoField("SubBrandSequenceNumber", primary_key=True)
    NM_BRN   = models.ForeignKey(Brand,on_delete=models.CASCADE, verbose_name="BrandName",db_column="NM_BRN")
    NM_SUB_BRN = models.CharField("SubBrandName", max_length=40)
    DE_SUB_BRN = models.CharField("Description", max_length=255)

    class Meta:
        db_table = 'ID_SUB_BRN'

class ManufacturerBrand(models.Model):
    ID_ID_BRN_MF = models.BigAutoField("ManufacturerBrandID",primary_key=True)
    ID_MF = models.ForeignKey(Manufacturer,on_delete=models.CASCADE, verbose_name="ManufacturerID",db_column="ID_MF")
    NM_BRN = models.ForeignKey(Brand,on_delete=models.CASCADE, verbose_name="BrandName",db_column="NM_BRN")
    DC_EF = models.DateTimeField("EffectiveDate")
    DC_EP = models.DateTimeField("ExpirationDate")
    CD_STS = models.CharField("CurrentStatusCode", max_length=2)
    class Meta:
        db_table = 'ID_BRN_MF'
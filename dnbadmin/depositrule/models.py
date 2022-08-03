''' Deposit Rule Model File '''
from django.db import models

# Create your models here.
STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class DepositRule(models.Model):
    ''' Deposit Rule Model Class '''
    ID_RU_DS = models.BigAutoField("DepositRuleID", primary_key=True)
    MO_DS = models.DecimalField(
        "DepositAmount", max_digits=7, decimal_places=2)
    LU_UOM_DS_PD = models.CharField(
        "DepositPaidOnUnitOfMeasureCode", max_length=40)
    MO_UOM_DS_PD = models.DecimalField(
        "DepositPaidPerUnitOfMeasureAmount", max_digits=16, decimal_places=2)
    SC_RU_DS = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")

    class Meta:
        db_table = 'RU_DS'

    def __str__(self):
        return self.LU_UOM_DS_PD

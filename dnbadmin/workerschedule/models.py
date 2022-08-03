'''worker schedule model'''
from django.db import models
from worker.models import Worker
from store.models import WorkLocation
from unitofmeasure.models import UnitOfMeasure

# Create your models here.

STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class TimeGroup(models.Model):
    '''time group'''
    ID_GP_TM = models.BigAutoField("TimeGroupID", primary_key=True)
    NM_GP_TM = models.CharField("Title", max_length=40, default="")
    DE_GP_TM = models.CharField("Description", max_length=255)
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'CO_GP_TM'

    def __unicode__(self):
        return self.ID_GP_TM


class WorkerAvailability(models.Model):
    '''worker timegroup relation'''
    ID_WRKR_AVLB = models.BigAutoField("WorkerAvailability", primary_key=True)
    ID_WRKR = models.ForeignKey(
        Worker, on_delete=models.CASCADE, verbose_name="WorkerID", db_column="ID_WRKR")
    ID_GP_TM = models.ForeignKey(
        TimeGroup, on_delete=models.CASCADE, verbose_name="TimeGroupID", db_column="ID_GP_TM")
    ID_LCN = models.ForeignKey(
        WorkLocation, on_delete=models.CASCADE, verbose_name="LocationID", db_column="ID_LCN")
    DC_EF = models.DateTimeField("EffectiveDate")
    DC_EP = models.DateTimeField("ExpirationDate")

    class Meta:
        db_table = 'CO_WRKR_AVLB'

    def __unicode__(self):
        return self.ID_WRKR_AVLB


class TimePeriod(models.Model):
    '''time period'''
    ID_PD_TM = models.BigAutoField("TimePeriodID", primary_key=True)
    NM_PD_TM = models.CharField("Name", max_length=40)
    WD = models.CharField("DayOfWeek", max_length=1)
    TM_SRT = models.TimeField("StartTime")
    TM_END = models.TimeField("EndTime", null=True, blank=True)
    LU_UOM_DRN = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE,
                                   verbose_name="DurationUnitOfMeasureCode", null=True, blank=True, db_column="LU_UOM_DRN")
    SI_DRN = models.DecimalField("Duration", max_digits=4, decimal_places=2)
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")

    class Meta:
        db_table = 'CO_PD_TM'

    def __unicode__(self):
        return self.ID_PD_TM


class TimeGroupTimePeriod(models.Model):
    '''time group time period relation'''
    ID_GP_PD_TM = models.BigAutoField(
        "TimeGroupTimePeriodID", primary_key=True)
    ID_PD_TM = models.ForeignKey(
        TimePeriod, on_delete=models.CASCADE, verbose_name="TimePeriodID", db_column="ID_PD_TM")
    ID_GP_TM = models.ForeignKey(
        TimeGroup, on_delete=models.CASCADE, verbose_name="TimeGroupID", db_column="ID_GP_TM")

    class Meta:
        db_table = 'CO_GP_PD_TM'

    def __unicode__(self):
        return self.ID_GP_PD_TM

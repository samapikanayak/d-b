'''Position models'''
from django.db import models
from worker.models import Worker
from job.models import Job
from django.conf import settings
from store.models import WorkLocation
from department.models import Department

# Create your models here.
PAY_PERIOD_CHOICES =(
        ("hr", "Hour"),
        ("wk", "Week"),
        ("mn", "Month"),
        ("yr", "Year")
    )

STATUS_CHOICES = (
    ("A", "A"),
    ("I", "I"),
)
class Position(models.Model):
    '''Position models'''
    ID_PST = models.BigAutoField("ContractorID",primary_key=True)
    ID_LCN = models.ForeignKey(WorkLocation, on_delete=models.CASCADE,verbose_name="LocationID",db_column="ID_LCN", null=True)
    ID_JOB = models.ForeignKey(Job, on_delete=models.CASCADE,verbose_name="JobID",db_column="ID_JOB",null=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE,verbose_name="DepartmentID",db_column="department_id",null=True)
    NM_TTL = models.CharField("Title",max_length=40)
    DE_PST = models.CharField("Description",max_length=255,blank=True, null=True)
    FL_TM_FL = models.BooleanField("FullTimeFlag",default=False)
    FL_SLRY = models.BooleanField("SalaryFlag",default=False)
    FL_EXM_OVR_TM = models.BooleanField("OvertimeExemptFlag",default=False)
    FL_RTE_PNL = models.BooleanField("PenalRateFlag",default=False)
    CD_PRD_PY = models.CharField("PayPeriodCode",max_length=2,choices=PAY_PERIOD_CHOICES,default="mn")
    MO_RTE_PY = models.DecimalField("PayRate",max_digits=16, decimal_places=5, blank=True, null=True)
    CRT_DT = models.DateTimeField("Created Date",auto_now_add=True)
    CRT_BY = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True, null=True,related_name='PST_Createuser',db_column="CRT_BY")
    MDF_DT = models.DateTimeField("Modified Date",auto_now=True)
    MDF_BY = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True, null=True,related_name='PST_Modifiyuser',db_column="MDF_BY")
    createdby = models.IntegerField(null=True)
    updatedby = models.IntegerField(null=True)

    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default="A"
    )
    class Meta:
        '''meta class for position model'''
        db_table = 'CO_PST'
    def __unicode__(self):
        return self.NM_TTL

class PositionWorkSchedule(models.Model):
    '''PositionWorkSchedule model'''
    ID_PST_WRK_SCH = models.BigAutoField("PositionWorkScheduleID",primary_key=True)
    ID_PST = models.ForeignKey(Position, on_delete=models.CASCADE,verbose_name="PositionID",db_column="ID_PST")
    WD_PST_WRK_SCH = models.CharField("PositionWorkScheduleWeekDay",max_length=1,blank=True, null=True)
    TM_STR = models.TimeField("StartTime",blank=True, null=True)
    TM_FNS = models.TimeField("Description",blank=True, null=True)
    HH_HR = models.DecimalField("Hours",max_digits=9, decimal_places=3, blank=True, null=True)
    class Meta:
        '''Position work schedule meta class'''
        db_table = 'CO_SCH_PST_WRK'
    def __unicode__(self):
        return self.ID_PST_WRK_SCH

class PositionHierarchy(models.Model):
    '''PositionHierarchy model'''
    ID_HRC_PST = models.BigAutoField("PositionHierarchyID",primary_key=True)
    ID_PST_SUB = models.ForeignKey(Position, on_delete=models.CASCADE,verbose_name="Subordinate",related_name='Sub_position',db_column="ID_PST_SUB")
    ID_PST_SPVR = models.ForeignKey(Position, on_delete=models.CASCADE,verbose_name="Supervisor",related_name='Sup_position',db_column="ID_PST_SPVR")
    DC_EF = models.DateTimeField("EffectiveDate")
    DC_EX = models.DateTimeField("ExpirationDate")
    class Meta:
        '''PositionHierarchy meta class'''
        db_table = 'ST_HRC_PST'
    def __unicode__(self):
        return self.ID_HRC_PST

class WorkerPositionAssignment(models.Model):
    '''WorkerPositionAssignment model'''
    ID_ASGMT_WRKR_PSN = models.BigAutoField("WorkerPositionAssignmentID",primary_key=True)
    ID_PST = models.ForeignKey(Position, on_delete=models.CASCADE,verbose_name="PositionID",db_column="ID_PST")
    ID_WRKR = models.ForeignKey(Worker, on_delete=models.CASCADE,verbose_name="WorkerID",db_column="ID_WRKR")
    DC_EF = models.DateTimeField("EffectiveDate")
    SC_EM_ASGMT = models.CharField("StatusCode",max_length=2,choices=PAY_PERIOD_CHOICES,default="mn")
    DC_EP = models.DateTimeField("ExpirationDate")
    NM_TTL = models.CharField("Title",max_length=40)
    FL_TM_FL = models.BooleanField("FullTimeFlag",default=False)
    FL_SLRY = models.BooleanField("SalaryFlag",default=False)
    FL_EXM_OVR_TM = models.BooleanField("OvertimeExemptFlag",default=False)
    FL_RTE_PNL = models.BooleanField("PenalRateFlag",default=False)
    FL_CMN = models.BooleanField("CommissionFlag",default=False)
    CD_PRD_PY = models.CharField("PayPeriodCode",max_length=2,choices=PAY_PERIOD_CHOICES,default="mn")
    MO_RTE_PY = models.DecimalField("PayRate",max_digits=16, decimal_places=5, blank=True, null=True)
    class Meta:
        '''WorkerPositionAssignment meta class'''
        db_table = 'CO_ASGMT_WRKR_PSN'

    def __unicode__(self):
        return self.ID_ASGMT_WRKR_PSN

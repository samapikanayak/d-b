'''Access Control'''
from django.db import models
from store.models import BusinessUnit, WorkLocation
from worker.models import Worker
from job.models import Job

# Create your models here.
STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)
ACCESS_CHOICES = (
    ("NA", "No Access"),
    ("GA", "Group Access"),
    ("RA", "Resource Access")
)
TERMINL_STAT_CHOICES = (
    ("A", "Active"),
    ("C", "Closed"),
    ("O", "Off-Line")
)
TYPE_OF_WORKSTATION = ()

ACCESS_TYPE_CHOICES = (
    ("Backend", "Backend"),
    ("POS Terminal", "POS Terminal")
)


class Operator(models.Model):
    '''Operator Model'''
    ID_OPR = models.BigAutoField("OperatorID", primary_key=True)
    PW_ACS_OPR = models.CharField("AccessPassword", max_length=20)
    NM_USR = models.CharField("UserName", max_length=40)
    EMAIL_USR = models.EmailField(
        "Email", max_length=254, unique=True, null=True)
    RS_TYP_OPR = models.CharField(
        "Resource Type", max_length=2, choices=ACCESS_CHOICES, default="NA")
    ACCS_TYP_OPR = models.CharField(
        "Access Type", max_length=255, default="Backend", choices=ACCESS_TYPE_CHOICES)
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'PA_OPR'

    def __unicode__(self):
        return self.NM_USR


class AccessPassword(models.Model):
    ''' authenticate an Operator identification'''
    AI_ACS_PSWD = models.BigAutoField(
        "AccessPasswordSequenceNumber", primary_key=True)
    ID_OPR = models.ForeignKey(Operator, on_delete=models.SET_NULL,
                               verbose_name="OperatorID", blank=True, null=True, db_column="ID_OPR")
    PS_ACS_OPR = models.CharField("Password", max_length=20)
    TS_EP = models.DateTimeField("ExpirationDateTime", blank=True, null=True)

    class Meta:
        db_table = 'CO_ACS_PSWD'

    def __unicode__(self):
        return self.ID_OPR


class OperatorBusinessUnitAssignment(models.Model):
    '''assignment of an OperatorID to a particular BusinessUnit'''
    ID_ASGMT_OPR_LCN = models.BigAutoField(
        "OperatorBusinessUnitAssignmentID", primary_key=True)
    ID_OPR = models.ForeignKey(
        Operator, on_delete=models.CASCADE, verbose_name="OperatorID", db_column="ID_OPR")
    ID_BSN_UN = models.ForeignKey(
        BusinessUnit, on_delete=models.CASCADE, verbose_name="BusinessUnitID", db_column="ID_BSN_UN")
    TS_EF = models.DateTimeField("EffectiveDateTime", blank=True, null=True)
    TS_EP = models.DateTimeField("ExpirationDateTime", blank=True, null=True)
    NU_OPR = models.IntegerField("OperatorNumber", blank=True, null=True)

    class Meta:
        db_table = 'CO_ASGMT_OPR_LCN'

    def __unicode__(self):
        return self.ID_ASGMT_OPR_LCN


class WorkerOperatorAssignment(models.Model):
    '''Worker Operator Assignment'''
    ID_ASGMT_WRKR_OPR = models.BigAutoField(
        "WorkerOperatorAssignmentID", primary_key=True)
    ID_WRKR = models.ForeignKey(
        Worker, on_delete=models.CASCADE, verbose_name="WorkerID", db_column="ID_WRKR")
    ID_OPR = models.ForeignKey(
        Operator, on_delete=models.CASCADE, verbose_name="OperatorID", db_column="ID_OPR")
    TS_EF = models.DateTimeField("EffectiveDateTime")
    TS_EP = models.DateTimeField("ExpirationDateTime")
    SC_ASGMT = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")

    class Meta:
        db_table = 'CO_ASGMT_WRKR_OPR'

    def __unicode__(self):
        return self.ID_ASGMT_WRKR_OPR


class WorkGroup(models.Model):
    '''WorkGroup'''
    ID_GP_WRK = models.BigAutoField("WorkGroupID", primary_key=True)
    ID_GP_WRK_PRNT = models.ForeignKey(
        'self', on_delete=models.CASCADE, verbose_name="ParentWorkGroupID", blank=True, null=True, db_column="ID_GP_WRK_PRNT")
    DE_GP_WRK = models.CharField(
        "Description", max_length=255, null=True, blank=True, )
    NM_GP_WRK = models.CharField(
        "WorkGroupName", max_length=255, null=True, blank=True, unique=True)
    status = models.CharField(
        max_length=8,
        null=True, blank=True,
        choices=STATUS_CHOICES,
        help_text="Workgroup status (Active/Inactive)",
    )
    access_type = models.CharField(
        max_length=40,
        null=True, blank=True,
        default="Backend", choices=ACCESS_TYPE_CHOICES,
        help_text="Workgroup Access Type")
    welcome_screen = models.CharField(
        max_length=255,
        null=True, blank=True)
    createdby = models.IntegerField(null=True, help_text="Created By")
    createddate = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, help_text="Created date"
    )
    updatedby = models.IntegerField(null=True, help_text="Updated By")
    updateddate = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, help_text="Last update date"
    )

    class Meta:
        db_table = 'CO_GP_WRK'

    def __unicode__(self):
        return self.DE_GP_WRK


class OperatorGroup(models.Model):
    '''Operator Group'''
    ID_GP_OPR = models.BigAutoField("OperatorGroupID", primary_key=True)
    ID_GP_WRK = models.ForeignKey(
        WorkGroup, on_delete=models.CASCADE, verbose_name="WorkGroupID", db_column="ID_GP_WRK")
    ID_OPR = models.ForeignKey(
        Operator, on_delete=models.CASCADE, verbose_name="OperatorID", db_column="ID_OPR")

    class Meta:
        db_table = 'CO_GP_OPR'

    def __unicode__(self):
        return self.ID_GP_OPR


class Resource(models.Model):
    '''Resource'''
    ID_RS = models.BigAutoField("ResourceID", primary_key=True)
    ID_RS_PRNT = models.ForeignKey(
        'self', on_delete=models.CASCADE, verbose_name="ParentResourceID", blank=True, null=True, db_column="ID_RS_PRNT")
    DE_RS = models.CharField("Description", max_length=255)
    display_order = models.IntegerField(
        null=True, blank=True, help_text="Display order"
    )
    menu_url = models.CharField(
        max_length=255, null=True, blank=True, help_text="Menu Url"
    )
    is_visible_menu = models.BooleanField(
        null=True, blank=True, default=True, help_text="Is Visible in Menu?"
    )

    class Meta:
        db_table = 'PA_RS'

    def __str__(self):
        return self.DE_RS


class GroupResourceAccess(models.Model):
    '''GroupResourceAccess'''
    ID_ACS_GP_RS = models.BigAutoField(
        "GroupResourceAccessID", primary_key=True)
    ID_GP_WRK = models.ForeignKey(
        WorkGroup, on_delete=models.CASCADE, verbose_name="WorkGroupID", db_column="ID_GP_WRK")
    ID_RS = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name="ResourceID", db_column="ID_RS")
    FL_ACS_GP_RD = models.BooleanField(
        'GroupReadAccessLevelFlag', default=False)
    FL_ACS_GP_WR = models.BooleanField(
        'GroupWriteAccessLevelFlag', default=False)

    class Meta:
        db_table = 'CO_ACS_GP_RS'

    def __unicode__(self):
        return self.ID_ACS_GP_RS


class StoreWorkGroup(models.Model):
    ''' Store Work Group Assignment '''
    storeworkgroup_id = models.AutoField(
        primary_key=True, help_text="Storeworkgroup Identity"
    )
    ID_BSN_UN = models.ForeignKey(
        BusinessUnit, on_delete=models.CASCADE, help_text="Store Identity"
    )
    ID_GP_WRK = models.ForeignKey(
        WorkGroup, on_delete=models.CASCADE, help_text="Work Group Identity"
    )

    class Meta:
        db_table = 'store_workgroup'


class OperatorResourceAccess(models.Model):
    '''OperatorResourceAccess'''
    ID_ACS_OPR_RS = models.BigAutoField(
        "OperatorResourceAccessID", primary_key=True)
    ID_RS = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name="ResourceID", db_column="ID_RS")
    ID_OPR = models.ForeignKey(
        Operator, on_delete=models.CASCADE, verbose_name="OperatorID", db_column="ID_OPR")
    PS_ACS_RD = models.BooleanField("ReadAccessLevelCode", default=False)
    PR_ACS_WR = models.BooleanField("WriteAccessLevelCode", default=False)

    class Meta:
        db_table = 'CO_ACS_OPR_RS'

    def __unicode__(self):
        return self.ID_ACS_OPR_RS


class TaskSet(models.Model):
    '''TaskSet'''
    ID_ST_TSK = models.BigAutoField("TaskSetID", primary_key=True)
    NM_ST_TSK = models.CharField("Name", max_length=40)

    class Meta:
        db_table = 'CO_ST_TSK'

    def __unicode__(self):
        return self.ID_ST_TSK


class Task(models.Model):
    '''Task'''
    ID_TSK = models.BigAutoField("TaskID", primary_key=True)
    # ID_MRHRC_GP = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,verbose_name="MerchandiseHierarchyGroupID",db_column="ID_MRHRC_GP")  # NOSONAR
    NM_TSK = models.CharField("TaskName", max_length=40)
    DE_TSK = models.CharField("TaskDescription", max_length=255)
    ID_ST_TSK = models.ForeignKey(
        TaskSet, on_delete=models.CASCADE, verbose_name="TaskSetID", db_column="ID_ST_TSK")
    # ID_CTR_RVN_CST = models.ForeignKey(RevenueCostCenter, on_delete=models.CASCADE,verbose_name="RevenueCostCenterID",db_column="ID_CTR_RVN_CST")  # NOSONAR

    class Meta:
        db_table = 'CO_TSK'

    def __unicode__(self):
        return self.ID_TSK


class JobTaskSet(models.Model):
    '''JobTaskSet'''
    ID_JOB_ST_TSK = models.BigAutoField("JobTaskSetID", primary_key=True)
    ID_ST_TSK = models.ForeignKey(
        TaskSet, on_delete=models.CASCADE, verbose_name="TaskSetID", db_column="ID_ST_TSK")
    ID_JOB = models.ForeignKey(
        Job, on_delete=models.CASCADE, verbose_name="JobID")

    class Meta:
        db_table = 'ST_JOB_ST_TSK'

    def __unicode__(self):
        return self.ID_JOB_ST_TSK


class TaskResourceAccess(models.Model):
    '''TaskResourceAccess'''
    ID_ACS_TSK_RS = models.BigAutoField(
        "TaskResourceAccessID", primary_key=True)
    ID_TSK = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name="TaskID", db_column="ID_TSK")
    ID_RS = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name="ResourceID", db_column="ID_RS")

    class Meta:
        db_table = 'CO_ACS_TSK_RS'

    def __unicode__(self):
        return self.ID_ACS_TSK_RS


class WorkstationGroup(models.Model):
    '''WorkstationGroup'''
    ID_WSGP = models.BigAutoField("WorkstationGroupID", primary_key=True)
    ID_WSGP_PRNT = models.ForeignKey('self', on_delete=models.CASCADE,
                                     verbose_name="ParentWorkstationGroupID", db_column="ID_WSGP_PRNT", null=True)
    NM_WSGP = models.CharField("Name", max_length=255)

    class Meta:
        db_table = 'CO_WSGP'

    def __unicode__(self):
        return self.ID_WSGP


class Workstation(models.Model):
    '''Workstation'''
    ID_WS = models.BigAutoField("WorkstationID", primary_key=True)
    # ID_EQ = models.ForeignKey(Equipment, on_delete=models.CASCADE,verbose_name="EquipmentID",db_column="ID_EQ")  # NOSONAR
    NM_WS_MF = models.CharField("ManufacturerName", max_length=40)
    NM_MDL_WS_TML = models.CharField("TerminalModelNumber", max_length=40)
    SC_TML_WS = models.CharField(
        "TerminalStatusCode", max_length=2, choices=TERMINL_STAT_CHOICES, default="A")
    QU_TL_WS = models.DecimalField("TillCount", max_digits=3, decimal_places=0)
    TY_WS = models.CharField("TypeCode", max_length=4,
                             choices=TYPE_OF_WORKSTATION)
    FL_MOD_TRG = models.BooleanField('TrainingModeFlag', default=False)
    FL_WS_OTSD = models.BooleanField('OutsideFlag', default=False)
    NM_ADS_DVC = models.CharField("DeviceAddress", max_length=40)
    ID_WSGP = models.ForeignKey(WorkstationGroup, on_delete=models.CASCADE,
                                verbose_name="WorkstationGroupID", db_column="ID_WSGP")

    class Meta:
        db_table = 'AS_WS'

    def __unicode__(self):
        return self.ID_WS


class WorkstationResourceAccess(models.Model):
    '''WorkstationResourceAccess'''
    ID_ACS_WS_RS = models.BigAutoField(
        "WorkstationResourceAccessID", primary_key=True)
    ID_WS = models.ForeignKey(Workstation, on_delete=models.CASCADE,
                              verbose_name="WorkstationID", db_column="ID_WS")
    ID_RS = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name="ResourceID", db_column="ID_RS")
    PS_ACS_RD = models.CharField(
        "ReadAccessLevelCode", max_length=2, choices=ACCESS_CHOICES, default="NA")
    PS_ACS_WR = models.CharField(
        "WriteAccessLevelCode", max_length=2, choices=ACCESS_CHOICES, default="NA")

    class Meta:
        db_table = 'CO_ACS_WS_RS'

    def __unicode__(self):
        return self.ID_ACS_WS_RS


class WorkstationGroupResourceAccess(models.Model):
    '''WorkstationGroupResourceAccess'''
    ID_ACS_WSGP_RS = models.BigAutoField(
        "WorkstationGroupResourceAccessID", primary_key=True)
    ID_WSGP = models.ForeignKey(WorkstationGroup, on_delete=models.CASCADE,
                                verbose_name="WorkstationGroupID", db_column="ID_WSGP")
    ID_RS = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name="ResourceID", db_column="ID_RS")

    class Meta:
        db_table = 'CO_ACS_WSGP_RS'

    def __unicode__(self):
        return self.ID_ACS_WSGP_RS


class WorkGroupWorkstationGroupResourceAccess(models.Model):
    '''WorkGroupWorkstationGroupResourceAccess'''
    ID_ACS_WKGP_WSGP_RS = models.BigAutoField(
        "WorkGroupWorkstationGroupResourceAccessID", primary_key=True)
    ID_WSGP = models.ForeignKey(WorkstationGroup, on_delete=models.CASCADE,
                                verbose_name="WorkstationGroupID", db_column="ID_WSGP")
    ID_GP_WRK = models.ForeignKey(
        WorkGroup, on_delete=models.CASCADE, verbose_name="WorkGroupID", db_column="ID_GP_WRK")
    ID_RS = models.ForeignKey(
        Resource, on_delete=models.CASCADE, verbose_name="ResourceID", db_column="ID_RS")

    class Meta:
        db_table = 'CO_ACS_WKGP_WSGP_RS'

    def __unicode__(self):
        return self.ID_ACS_WKGP_WSGP_RS


class WorkstationLocationAssignment(models.Model):
    '''WorkstationLocationAssignment'''
    ID_ASGMT_WS_LCN = models.BigAutoField(
        "WorkstationLocationAssignmentID", primary_key=True)
    ID_WS = models.ForeignKey(Workstation, on_delete=models.CASCADE,
                              verbose_name="WorkstationID", db_column="ID_WS")
    ID_LCN = models.ForeignKey(
        WorkLocation, on_delete=models.CASCADE, verbose_name="LocationID", db_column="ID_LCN")
    DC_EF = models.DateTimeField("EffectiveDate")
    NU_WS = models.IntegerField("WorkstationNumber", unique=True)
    DC_EP = models.DateTimeField("ExpirationDate")

    class Meta:
        db_table = 'CO_ASGMT_WS_LCN'

    def __unicode__(self):
        return self.ID_ASGMT_WS_LCN


class WorkstationSiteAssignment(models.Model):
    '''WorkstationSiteAssignment'''
    ID_ASGMT_WS_STE = models.BigAutoField(
        "WorkstationSiteAssignmentID", primary_key=True)
    ID_WS = models.ForeignKey(Workstation, on_delete=models.CASCADE,
                              verbose_name="WorkstationID", db_column="ID_WS")
    DC_EF = models.DateTimeField("EffectiveDate")
    # ID_STE = models.ForeignKey(Site, on_delete=models.CASCADE,verbose_name="SiteID",db_column="ID_STE")  # NOSONAR
    NO_WS = models.IntegerField("WorkstationNumber", unique=True)
    DC_EP = models.DateTimeField("ExpirationDate")

    class Meta:
        db_table = 'CO_ASGMT_WS_STE'

    def __unicode__(self):
        return self.ID_ASGMT_WS_STE

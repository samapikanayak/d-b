from django.db import models
from party.models import PartyRoleAssignment
from django.conf import settings

# Create your models here.
WORKER_TYPE_CHOICES =(
    )
STATUS_CHOICES =(
    ("A", "Active"),
    ("I", "Inactive")
)
VENDOR_TYPE_CHOICES =(
        ("B2B", "B2B"),
        ("B2C", "B2C"),
        ("B2G", "B2G")
    )
class Worker(models.Model):
    ID_WRKR = models.BigAutoField("WorkerID",primary_key=True)
    TY_WRKR = models.CharField("WorkerType Code",max_length=2,choices=WORKER_TYPE_CHOICES,blank=True, null=True)
    BM_PGPH_WRKR = models.BinaryField("WorkerPhotograph",blank=True, null=True)
    DE_SPL_RQMT = models.TextField("SpecialRequirements",blank=True, null=True)
    ID_PRTY_RO_ASGMT = models.ForeignKey(PartyRoleAssignment, on_delete=models.CASCADE,verbose_name="PartyRoleAssignmentID",db_column="ID_PRTY_RO_ASGMT")
    WRKR_CRT_DT = models.DateTimeField("Created Date",auto_now_add=True)
    WRKR_CRT_BY = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True, null=True,related_name='WRKR_Createuser',db_column="WRKR_CRT_BY")
    WRKR_MDF_DT = models.DateTimeField("Modified Date",auto_now=True)
    WRKR_MDF_BY = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True, null=True,related_name='WRKR_Modifiyuser',db_column="WRKR_MDF_BY")
    class Meta:
        db_table = 'PA_WRKR'
    
    def __unicode__(self):
        return self.TY_WRKR

class Employee(models.Model):
    ID_EM = models.BigAutoField("EmployeeID",primary_key=True)
    ID_WRKR = models.ForeignKey(Worker, on_delete=models.CASCADE,verbose_name="WorkerID",db_column="ID_WRKR")
    SC_EM = models.CharField("StatusCode",max_length=2,choices=STATUS_CHOICES,default="A")
    class Meta:
        db_table = 'PA_EM'
    
    def __unicode__(self):
        return self.SC_EM

class Vendor(models.Model):
    ID_VN = models.BigAutoField("ContractorID",primary_key=True)
    TY_VN = models.CharField("VendorType",max_length=3,choices=VENDOR_TYPE_CHOICES)
    ID_PRTY_RO_ASGMT = models.ForeignKey(PartyRoleAssignment, on_delete=models.CASCADE,verbose_name="PartyRoleAssignmentID",db_column="ID_PRTY_RO_ASGMT")
    class Meta:
        db_table = 'TY_VN'
    
    def __unicode__(self):
        return self.TY_VN

class Contractor(models.Model):
    ID_CNTR = models.BigAutoField("ContractorID",primary_key=True)
    ID_WRKR = models.ForeignKey(Worker, on_delete=models.CASCADE,verbose_name="WorkerID",db_column="ID_WRKR")
    ID_VN = models.ForeignKey(Vendor, on_delete=models.CASCADE,verbose_name="VendorID",db_column="ID_VN")
    class Meta:
        db_table = 'PA_CNTR'
    
    def __unicode__(self):
        return self.ID_CNTR
class Manufacturer(models.Model):
    ID_MF = models.BigAutoField("ManufacturerID",primary_key=True)
    class Meta:
        db_table = 'PA_MF'

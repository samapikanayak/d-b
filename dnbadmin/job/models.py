from django.db import models

# Create your models here.
class Job(models.Model):
    ID_JOB = models.BigAutoField("JobID",primary_key=True)
    NM_JOB = models.CharField("Name",max_length=40) 
    DE_JOB = models.TextField("Description",blank=True, null=True)
    FL_SHR = models.BooleanField("ShareFlag",default=False)
    class Meta:
        db_table = 'CO_JOB'
    
    def __unicode__(self):
        return self.NM_JOB

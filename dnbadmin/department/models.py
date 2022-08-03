'''Department models'''
from django.db import models
from store.models import BusinessUnitGroup

STATUS_CHOICES = (
    ("A", "A"),
    ("I", "I"),
)

class Department(models.Model):
    '''Department model'''
    department_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="Department name")
    business_unit_group_code = models.ForeignKey(
        BusinessUnitGroup, on_delete=models.CASCADE,related_name="business_unit_group"
    )
    parent_department_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name="ParentDepartmentID", db_column="parent_department_id", null=True
    )
    description = models.TextField(
        null=True, blank=True, help_text="Department description"
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default="A",
        null=True,
        blank=True,
        help_text="Department status (Active/Inactive)",
    )
    isdeleted = models.BooleanField(
        null=True, blank=True, default=False, help_text="Is Deleted?"
    )
    createdby = models.IntegerField(null=True, help_text="Created By")
    createddate = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, help_text="Date Created"
    )
    updatedby = models.IntegerField(null=True, help_text="Updated By ")
    updateddate = models.DateTimeField(
        null=True, blank=True, auto_now=True, help_text="Last Updated Date"
    )

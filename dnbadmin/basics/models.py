"""
Basic common models
"""
from django.db import models

# Create your models here.
STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class DateFormat(models.Model):
    ''' Date Format Model '''
    ID_BA_DFMT = models.BigAutoField("DateFormatID", primary_key=True)
    name = models.CharField("Date Format", max_length=50)
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        """meta for model"""
        db_table = 'CO_BA_DFMT'

    def __str__(self):
        return self.name


class Timezone(models.Model):
    """Timezone model"""
    ID_BA_TZN = models.BigAutoField("TimezoneID", primary_key=True)
    gmt_offset = models.CharField("GMT Offset", max_length=100)
    country = models.CharField("Country", max_length=100)
    timezone = models.CharField("Timezone", max_length=100)
    code = models.CharField("Timezone Code", max_length=100)
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        """meta for model"""
        db_table = 'CO_BA_TZN'

    def __str__(self):
        return self.code


class BusinessUnitType(models.Model):
    """ Business Unit Type Model Class """
    name = models.CharField(
        max_length=255, unique=True, help_text="Business unit Type"
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="Businessunit status (Active/Inactive)",
    )
    createdby = models.IntegerField(null=True, help_text="Created By")
    createddate = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, help_text="Date Created"
    )
    updatedby = models.IntegerField(null=True, help_text="Updated By ")
    updateddate = models.DateTimeField(
        null=True, blank=True, auto_now=True, help_text="Last Updated Date"
    )

    class Meta:
        """meta for model"""
        db_table = 'LO_BSN_UN_TY'

    def __str__(self):
        return self.name


class CustomFormFieldType(models.Model):
    '''Custom Form Field Type'''
    ID_BA_CFF_TYP = models.BigAutoField(
        "CustomFormFieldType ID", primary_key=True)
    customformfieldtype_name = models.CharField(
        "Custom form field Type Name", max_length=255, unique=True, help_text="Custom form field Type Name")
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    isdeleted = models.BooleanField(
        "isdeleted", null=True, blank=True, default=False, help_text="Is Deleted?")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        """meta for model"""
        db_table = 'CO_BA_CFF_TYP'

    def __str__(self):
        return self.customformfieldtype_name


class CustomFormField(models.Model):
    '''Custom Form Field'''
    ID_BA_CFF = models.BigAutoField("CustomFormField ID", primary_key=True)
    customformfield_name = models.CharField(
        "Custom form field Name", max_length=40, unique=True, help_text="Custom form field Name")
    customformfield_description = models.TextField(
        "Custom form field Description", null=True, blank=True, help_text="Custom form field Description")
    ID_BA_CFF_TYP = models.ForeignKey(CustomFormFieldType, on_delete=models.PROTECT,
                                      verbose_name="Custom form field Type Id", db_column="ID_BA_CFF_TYP", help_text="Custom form field Type Id",)
    isfilterable = models.BooleanField(
        "Field is filterable?", null=True, blank=True, default=False, help_text="Field is filterable?")
    customformfield_label = models.CharField(
        "Custom form field Label", max_length=255, null=True, blank=True, help_text="Custom form field Label")
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    isdeleted = models.BooleanField(
        "isdeleted", null=True, blank=True, default=False, help_text="Is Deleted?")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        """meta for model"""
        db_table = 'CO_BA_CFF'


class CustomFormFieldValue(models.Model):
    '''Custom Form Field Value'''
    ID_BA_CFF_VAL = models.BigAutoField(
        "CustomFormFieldValue ID", primary_key=True)
    ID_BA_CFF = models.ForeignKey(CustomFormField, on_delete=models.CASCADE,
                                  verbose_name="Custom form field Id", db_column="ID_BA_CFF", help_text="Custom form field Id")
    customformfield_value = models.CharField(
        "Custom form field Value", max_length=255, blank=True, help_text="Custom form field Value")
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    isdefault = models.BooleanField(
        "isdefault", null=True, blank=True, default=False, help_text="Is it default?")
    isdeleted = models.BooleanField(
        "isdeleted", null=True, blank=True, default=False, help_text="Is Deleted?")

    class Meta:
        """meta for model"""
        db_table = 'CO_BA_CFF_VAL'


class ImageInformation(models.Model):
    ''' Image Information Class '''
    imageinformation_id = models.AutoField(
        primary_key=True, help_text="Image information Identity"
    )
    alt = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Alternative text for image",
    )
    title = models.CharField(
        max_length=255, null=True, blank=True, help_text="Title of the image"
    )
    image_info = models.CharField(
        max_length=255, null=True, blank=True, help_text="Image information"
    )
    image_license = models.CharField(
        max_length=255, null=True, blank=True, help_text="Image License"
    )
    acquire_license_page = models.CharField(
        max_length=255, null=True, blank=True, help_text="Acquire license page"
    )
    og_image_tag = models.CharField(
        max_length=255, null=True, blank=True, help_text="OG image tag"
    )
    image_slug = models.CharField(
        max_length=255, null=True, blank=True, help_text="Image slug"
    )
    modulename = models.CharField(
        max_length=255, null=True, blank=True, help_text="Module name"
    )
    imagename = models.CharField(
        max_length=255, null=True, blank=True, help_text="Image name"
    )
    imageurl = models.TextField(null=True, blank=True, help_text="Image url")
    image_type = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Image Type",
    )
    imagesize = models.CharField(max_length=255, help_text="Image size")
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        default="Active",
        help_text=" Image info status (Active/Inactive)",
    )
    isdeleted = models.BooleanField(
        null=True, blank=True, default=False, help_text="Is Deleted?"
    )
    createdby = models.IntegerField(
        null=True, blank=True, default=0, help_text="Created By"
    )
    createddate = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, help_text="Date Created"
    )
    updatedby = models.IntegerField(
        null=True, blank=True, default=0, help_text="Updated By"
    )
    updateddate = models.DateTimeField(
        null=True, blank=True, auto_now=True, help_text="Last Updated Date"
    )

    class Meta:
        """meta for model"""
        db_table = 'image_info'

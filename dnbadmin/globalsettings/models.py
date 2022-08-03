"""
Global Setting models
"""
from django.db import models
from basics.models import DateFormat, Timezone
from party.models import Language
from store.models import BusinessUnit

# Create your models here.
STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class GlobalSetting(models.Model):
    ''' Global Setting Model '''
    ID_GB_STNG = models.BigAutoField("GlobalSettingID", primary_key=True)
    name = models.CharField("Setting name", max_length=100, unique=True)
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    is_default = models.BooleanField(
        "Is Default Settings?", null=True, blank=True, default=False)
    ID_LGE = models.ForeignKey(Language, on_delete=models.SET_NULL,
                               verbose_name="LanguageID", blank=True, null=True, db_column="ID_LGE")
    ID_BA_DFMT = models.ForeignKey(DateFormat, on_delete=models.SET_NULL,
                                   verbose_name="DateFormatID", blank=True, null=True, db_column="ID_BA_DFMT")
    ID_BA_TZN = models.ForeignKey(Timezone, on_delete=models.SET_NULL,
                                  verbose_name="TimezoneID", blank=True, null=True, db_column="ID_BA_TZN")
    page_title = models.CharField(
        "Page title", max_length=100, null=True, blank=True, help_text="Page title")
    page_description = models.TextField(
        "Page description", null=True, blank=True, help_text="Page description")
    page_keyword = models.CharField(
        "Page keyword", max_length=100, null=True, blank=True, help_text="Page keyword")
    meta_locale = models.CharField(
        "Meta locale", max_length=255, null=True, blank=True, help_text="Meta location")
    meta_robots = models.CharField(
        "Meta robots", max_length=255, null=True, blank=True, help_text="Meta robots")
    meta_referral = models.CharField(
        "Meta referral", max_length=255, null=True, blank=True, help_text="Meta referral")
    meta_rights = models.CharField(
        "Meta rights", max_length=255, null=True, blank=True, help_text="Meta rights")
    og_type = models.CharField(
        "OG type", max_length=100, null=True, blank=True, help_text="OG type")
    og_url = models.CharField("OG url", max_length=255,
                              null=True, blank=True, help_text="OG url")
    og_title = models.CharField(
        "OG title", max_length=100, null=True, blank=True, help_text="OG title")
    og_description = models.TextField(
        "OG description", null=True, blank=True, help_text="OG description")
    og_image = models.CharField(
        "OG image", null=True, blank=True, max_length=255, help_text="OG image")
    og_locale = models.CharField(
        "OG locale", null=True, blank=True, max_length=255, help_text="OG locale")
    twitter_card = models.CharField(
        "Twitter card", null=True, blank=True, max_length=255, help_text="Twitter card")
    view_point = models.CharField(
        "View point", null=True, blank=True, max_length=255, help_text="View point")
    script = models.TextField(
        "Script", null=True, blank=True, help_text="Script")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'CO_GB_STNG'

    def __str__(self):
        return self.name


class BusinessUnitSetting(models.Model):
    ''' Global Setting Business unit relation '''
    ID_BSN_UN_STNG = models.BigAutoField(
        "BusinessUnitSettingID", primary_key=True)
    ID_BSN_UN = models.ForeignKey(
        BusinessUnit, on_delete=models.CASCADE, verbose_name="BusinessUnitID", db_column="ID_BSN_UN")
    ID_GB_STNG = models.ForeignKey(
        GlobalSetting, on_delete=models.CASCADE, verbose_name="GlobalSettingID", db_column="ID_GB_STNG")

    class Meta:
        db_table = 'CO_BSN_UN_STNG'

    def getid(self):
        '''get id of relation'''
        return self.ID_BSN_UN_STNG

'''taxonomy model'''
from django.db import models
from sellingrule.models import ItemSellingRule
from basics.models import CustomFormField, CustomFormFieldValue

# Create your models here.

STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)


class MerchandiseHierarchyFunction(models.Model):
    '''Merchandise Hierarchy Function'''
    ID_MRHRC_FNC = models.BigAutoField(
        "MerchandiseHierarchyFunctionID", primary_key=True)
    NM_MRHRC_FNC = models.CharField("Name", max_length=255)

    class Meta:
        db_table = 'CO_MRHRC_FNC'


class MerchandiseHierarchyLevel(models.Model):
    '''Merchandise Hierarchy Level'''
    ID_MRHRC_LV = models.BigAutoField(
        "MerchandiseHierarchyLevelID", primary_key=True)
    ID_MRHRC_FNC = models.ForeignKey(MerchandiseHierarchyFunction, on_delete=models.CASCADE,
                                     verbose_name="MerchandiseHierarchyFunctionID", db_column="ID_MRHRC_FNC")
    ID_MRHRC_LV_PRNT = models.ForeignKey(
        'self', on_delete=models.CASCADE, verbose_name="ParentMerchandiseHierarchyLevelID", db_column="ID_MRHRC_LV_PRNT", null=True)
    DE_MRHRC_LV = models.CharField("Name", max_length=40)

    class Meta:
        db_table = 'CO_MRHRC_LV'


class MerchandiseHierarchyGroup(models.Model):
    '''Merchandise Hierarchy Group'''
    ID_MRHRC_GP = models.BigAutoField(
        "MerchandiseHierarchyGroupID", primary_key=True)
    ID_RU_ITM_SL = models.ForeignKey(
        ItemSellingRule, on_delete=models.CASCADE, verbose_name="ItemSellingRuleID", db_column="ID_RU_ITM_SL")
    NM_MRHRC_GP = models.CharField("Name", max_length=255)
    DE_MRHRC_GP = models.CharField("Description", max_length=255)

    class Meta:
        db_table = 'CO_MRHRC_GP'


class AssociatedMerchandiseHierarchyGroup(models.Model):
    '''Associated Merchandise Hierarchy Group'''
    ID_ASCTN_MRHRC = models.BigAutoField(
        "AssociatedMerchandiseHierarchyGroupID", primary_key=True)
    ID_MRHRC_FNC = models.ForeignKey(MerchandiseHierarchyFunction, on_delete=models.CASCADE,
                                     verbose_name="MerchandiseHierarchyFunctionID", db_column="ID_MRHRC_FNC")
    ID_MRHRC_GP_PRNT = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                         verbose_name="ParentMerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP_PRNT", related_name='ASCTN_MRHRC_PRNT')
    ID_MRHRC_GP_CHLD = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                         verbose_name="ChildMerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP_CHLD", related_name='ASCTN_MRHRC_CHLD')
    ID_MRHRC_LV_PRNT = models.ForeignKey(MerchandiseHierarchyLevel, on_delete=models.CASCADE,
                                         verbose_name="ParentMerchandiseHierarchyLevelID", db_column="ID_MRHRC_LV_PRNT")
    DC_EF = models.DateTimeField("EffectiveDate")
    DC_EP = models.DateTimeField("ExpirationDate")

    class Meta:
        db_table = 'ST_ASCTN_MRHRC'


class Style(models.Model):
    '''Style'''
    LU_STYL = models.CharField("StyleCode", max_length=4, primary_key=True)
    DE_STYL = models.CharField("Description", max_length=255)
    NM_STYL = models.CharField("Name", max_length=40)

    class Meta:
        db_table = 'CO_STYL'


class MerchandiseHierarchyGroupStyle(models.Model):
    '''Merchandise Hierarchy Group Style'''
    ID_MRGP_STYL = models.BigAutoField(
        "MerchandiseHierarchyGroupStyleID", primary_key=True)
    ID_MRHRC_GP = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                    verbose_name="MerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP")
    LU_STYL = models.ForeignKey(
        Style, on_delete=models.CASCADE, verbose_name="StyleCode", db_column="LU_STYL")

    class Meta:
        db_table = 'CO_MRGP_STYL'


class ColorPalette(models.Model):
    '''Color Palette'''
    ID_PLTE_CLR = models.BigAutoField("ColorPaletteID", primary_key=True)
    NM_PLTE_CLR = models.CharField("Name", max_length=40)
    DE_PLTE_CLR = models.CharField("Description", max_length=255)

    class Meta:
        db_table = 'CO_PLTE_CLR'


class MerchandiseHierarchyGroupColorPalette(models.Model):
    '''Merchandise Hierarchy Group Color Palette'''
    ID_MRGP_PLTE_CLR = models.BigAutoField(
        "MerchandiseHierarchyGroupColorPaletteID", primary_key=True)
    ID_MRHRC_GP = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                    verbose_name="MerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP")
    ID_PLTE_CLR = models.ForeignKey(
        ColorPalette, on_delete=models.CASCADE, verbose_name="ColorPaletteID", db_column="ID_PLTE_CLR")

    class Meta:
        db_table = 'CO_MRGP_PLTE_CLR'


class ColorListAgency(models.Model):
    '''Color List Agency'''
    ID_AGY_CLR_LST = models.BigAutoField("ColorListAgencyID", primary_key=True)
    NM_AGY_CLR_LST = models.CharField("Name", max_length=40)

    class Meta:
        db_table = 'PA_AGY_CLR_LST'


class Color(models.Model):
    '''Color'''
    CD_CLR = models.CharField("ColorCode", max_length=4, primary_key=True)
    NM_CLR = models.CharField("Name", max_length=40)
    DE_CLR = models.CharField("Description", max_length=255)
    ID_PLTE_CLR = models.ForeignKey(
        ColorPalette, on_delete=models.CASCADE, verbose_name="ColorPaletteID", db_column="ID_PLTE_CLR")
    ID_AGY_CLR_LST = models.ForeignKey(
        ColorListAgency, on_delete=models.CASCADE, verbose_name="ColorListAgencyID", db_column="ID_AGY_CLR_LST")
    DE_MDFR = models.CharField("Modification", max_length=255)

    class Meta:
        db_table = 'CO_CLR'


class MerchandiseHierarchyGroupColor(models.Model):
    '''Merchandise Hierarchy Group Color'''
    ID_MRGP_CLR = models.BigAutoField(
        "MerchandiseHierarchyGroupColorID", primary_key=True)
    ID_MRHRC_GP = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                    verbose_name="MerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP")
    CD_CLR = models.ForeignKey(
        Color, on_delete=models.CASCADE, verbose_name="ColorCode", db_column="CD_CLR")

    class Meta:
        db_table = 'CO_MRGP_CLR'


class SizeFamily(models.Model):
    '''Size Family'''
    ID_SZ_FMY = models.BigAutoField("SizeFamilyID", primary_key=True)
    NM_SZ_FMY = models.CharField("SizeFamilyName", max_length=40)
    DE_SZ_FMY = models.CharField("SizeFamilyDescription", max_length=40)

    class Meta:
        db_table = 'CO_SZ_FMY'


class Size(models.Model):
    '''Size'''
    CD_SZ = models.CharField("SizeCode", max_length=4, primary_key=True)
    ID_SZ_FMY = models.ForeignKey(
        SizeFamily, on_delete=models.CASCADE, verbose_name="SizeFamilyID", db_column="ID_SZ_FMY")
    ED_TB_SZ = models.CharField("TableCode", max_length=2)
    NM_TB_SZ = models.CharField("TableName", max_length=40)
    DE_TB_SZ = models.CharField("Description", max_length=255)
    ED_SZ_ACT = models.CharField("ActualSizeCode", max_length=4)
    DE_TYP_ACT_SZ = models.CharField(
        "ActualSizeTypeDescription", max_length=40)
    DE_PRPTN_ACT_SZ = models.CharField(
        "ActualSizeProportionDescription", max_length=255)

    class Meta:
        db_table = 'CO_SZ'


class MerchandiseHierarchyGroupSize(models.Model):
    '''Merchandise Hierarchy Group Size'''
    ID_MRGP_SZ = models.BigAutoField(
        "MerchandiseHierarchyGroupSizeID", primary_key=True)
    ID_MRHRC_GP = models.ForeignKey(MerchandiseHierarchyGroup, on_delete=models.CASCADE,
                                    verbose_name="MerchandiseHierarchyGroupID", db_column="ID_MRHRC_GP")
    CD_SZ = models.ForeignKey(
        Size, on_delete=models.CASCADE, verbose_name="SizeCode", db_column="CD_SZ")
    ID_SZ_FMY = models.ForeignKey(
        SizeFamily, on_delete=models.CASCADE, verbose_name="SizeFamilyID", db_column="ID_SZ_FMY")

    class Meta:
        db_table = 'CO_MRGP_SZ'


class MerchandiseTemplateType(models.Model):
    '''Merchandise Template Type'''
    ID_MRHRC_TMP_TYP = models.BigAutoField(
        "Taxonomy Master Template Type Id", primary_key=True)
    merchandisetemplatetypename = models.CharField(
        "Master template type name", max_length=255, unique=True, help_text="Master template type name")
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
        db_table = 'CO_MRHRC_TMP_TYP'

    def __str__(self):
        return self.merchandisetemplatetypename


class MerchandiseTemplate(models.Model):
    '''Merchandise Template'''
    ID_MRHRC_TMP = models.BigAutoField(
        "Taxonomy Master Template Id", primary_key=True)
    merchandisetemplatename = models.CharField(
        "Name", max_length=255, unique=True, help_text="Name")
    description = models.TextField(
        "Description", null=True, blank=True, help_text="Description")
    ID_MRHRC_TMP_TYP = models.ForeignKey(MerchandiseTemplateType, on_delete=models.CASCADE, verbose_name="Taxonomy Master Template Type Id",
                                         db_column="ID_MRHRC_TMP_TYP", related_name="template_type", help_text="Master taxonomy template type Identity")
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    isdefault = models.BooleanField(
        "isdefault", null=True, blank=True, default=False, help_text="Is it default?")
    isdeleted = models.BooleanField(
        "isdeleted", null=True, blank=True, default=False, help_text="Is Deleted?")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'CO_MRHRC_TMP'


class MerchandiseTemplateControls(models.Model):
    '''Merchandise Template Controls'''
    ID_MRHRC_TMP_CNT = models.BigAutoField(
        "Template control Id", primary_key=True)
    ID_MRHRC_TMP = models.ForeignKey(MerchandiseTemplate, on_delete=models.CASCADE, verbose_name="Taxonomy Template Id",
                                     db_column="ID_MRHRC_TMP", related_name="taxonomy_template", help_text="Taxonomy Template Id")
    merchandisetemplatecontroldescription = models.TextField(
        "Description", null=True, blank=True, help_text="Description")
    ID_BA_CFF = models.ForeignKey(CustomFormField, on_delete=models.SET_NULL, null=True, blank=True, related_name="template_formfield",
                                  help_text="Custom form field Identity", verbose_name="Custom form field Id", db_column="ID_BA_CFF")
    ismandatory = models.BooleanField(
        "Is it mandatory?", null=True, blank=True, default=False, help_text="Is it mandatory?")
    ishidden = models.BooleanField(
        "Is hidden?", null=True, blank=True, default=False, help_text="Is hidden?")
    isfilterable = models.BooleanField(
        "Is filterable?", null=True, blank=True, default=False, help_text="Is filterable?")
    isvalidation = models.BooleanField(
        "Is validation required?", null=True, blank=True, default=False, help_text="Is validation required?")
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    isdefault = models.BooleanField(
        "isdefault", null=True, blank=True, default=False, help_text="Is it default?")
    isdeleted = models.BooleanField(
        "isdeleted", null=True, blank=True, default=False, help_text="Is Deleted?")
    createdby = models.IntegerField("Created By", null=True)
    createddate = models.DateTimeField(
        "Date Created", null=True, blank=True, auto_now_add=True)
    updatedby = models.IntegerField("Updated By", null=True)
    updateddate = models.DateTimeField(
        "Last Updated Date", null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'CO_MRHRC_TMP_CNT'


class MerchandiseTemplateControlValue(models.Model):
    '''Merchandise Template Control Value'''
    ID_MRHRC_TMP_CNT_VL = models.BigAutoField(
        "Template control value Id", primary_key=True)
    ID_MRHRC_TMP_CNT = models.ForeignKey(MerchandiseTemplateControls, on_delete=models.CASCADE, verbose_name="Taxonomy Template control Id",
                                         db_column="ID_MRHRC_TMP_CNT", related_name="taxonomy_template_control", help_text="Taxonomy Template control Id")
    ID_BA_CFF_VAL = models.ForeignKey(CustomFormFieldValue, null=True, blank=True, on_delete=models.CASCADE,
                                      help_text="Custom form field value Identity", verbose_name="Custom form field value Id", db_column="ID_BA_CFF_VAL")
    merchandisetemplatecontrol_value = models.TextField(
        "Template control value", null=True, blank=True, help_text="Template control value")
    status = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    isdefault = models.BooleanField(
        "isdefault", null=True, blank=True, default=False, help_text="Is it default?")
    isdeleted = models.BooleanField(
        "isdeleted", null=True, blank=True, default=False, help_text="Is Deleted?")

    class Meta:
        db_table = 'CO_MRHRC_TMP_CNT_VL'

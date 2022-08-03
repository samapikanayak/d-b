'''taxonomy model unit test'''
from random import randint
from django.test import TestCase
from django.utils.crypto import get_random_string as grs
from django.utils import timezone
from sellingrule.tests.test_models import ItemTenderRestrictionGroupTest, ItemSellingRuleTest
from basics.tests.test_models import CustomFormFieldModelTest, CustomFormFieldValueModelTest
from ..models import *


class MerchandiseHierarchyFunctionTest(TestCase):
    '''MerchandiseHierarchyFunctionTest'''

    def create_merchandise_hierarchy_function(self):
        '''create'''
        NM_MRHRC_FNC = 'nm_mrhrc_fnc'
        return MerchandiseHierarchyFunction.objects.create(NM_MRHRC_FNC=NM_MRHRC_FNC)

    def test_merchandise_hierarchy_function(self):
        '''test create'''
        obj = self.create_merchandise_hierarchy_function()
        self.assertTrue(isinstance(obj, MerchandiseHierarchyFunction))


class MerchandiseHierarchyLevelTest(TestCase):
    '''MerchandiseHierarchyLevelTest'''

    def craete_merchandise_heirarchy_level(self):
        '''create'''
        ID_MRHRC_FNC = MerchandiseHierarchyFunctionTest.create_merchandise_hierarchy_function(
            self)
        DE_MRHRC_LV = str("DE_MRHRC_LV").lower()
        return MerchandiseHierarchyLevel.objects.create(ID_MRHRC_FNC=ID_MRHRC_FNC, DE_MRHRC_LV=DE_MRHRC_LV)

    def test_merchandise_heirarchy_level(self):
        '''test create'''
        obj = self.craete_merchandise_heirarchy_level()
        self.assertTrue(isinstance(obj, MerchandiseHierarchyLevel))


class MerchandiseHierarchyGroupTest(TestCase):
    '''MerchandiseHierarchyGroupTest'''

    def create_merchandise_hierarchy_group(self):
        '''create'''
        return MerchandiseHierarchyGroup.objects.create(ID_RU_ITM_SL=ItemSellingRuleTest.create_item_selling_rule(self), NM_MRHRC_GP='nm_mrhrc_gp', DE_MRHRC_GP='description')

    def test_merchandise_hierarchy_group(self):
        '''test create'''
        obj = self.create_merchandise_hierarchy_group()
        self.assertTrue(isinstance(obj, MerchandiseHierarchyGroup))


class AssociatedMerchandiseHierarchyGroupTest(TestCase):
    '''AssociatedMerchandiseHierarchyGroupTest'''

    def create_associate_merchandise_heirarchy_group(self):
        '''create'''
        ID_MRHRC_FNC = MerchandiseHierarchyFunctionTest.create_merchandise_hierarchy_function(
            self)
        ID_MRHRC_GP_PRNT = MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(
            self)
        ID_MRHRC_GP_CHLD = MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(
            self)
        ID_MRHRC_LV_PRNT = MerchandiseHierarchyLevelTest.craete_merchandise_heirarchy_level(
            self)
        DC_EF = timezone.now()
        DC_EP = timezone.now()
        return AssociatedMerchandiseHierarchyGroup.objects.create(ID_MRHRC_FNC=ID_MRHRC_FNC, ID_MRHRC_GP_PRNT=ID_MRHRC_GP_PRNT, ID_MRHRC_GP_CHLD=ID_MRHRC_GP_CHLD,
                                                                  ID_MRHRC_LV_PRNT=ID_MRHRC_LV_PRNT, DC_EF=DC_EF, DC_EP=DC_EP)

    def test_associated_merchandise_heirarchy_group(self):
        '''test create'''
        obj = self.create_associate_merchandise_heirarchy_group()
        self.assertTrue(isinstance(obj, AssociatedMerchandiseHierarchyGroup))


class StyleTest(TestCase):
    '''StyleTest'''

    def create_style(self):
        '''create'''
        LU_STYL = str(randint(0, 1000))
        DE_STYL = str(randint(0, 10000000))
        NM_STYL = str(randint(0, 100000))
        return Style.objects.create(LU_STYL=LU_STYL, DE_STYL=DE_STYL, NM_STYL=NM_STYL)

    def test_style(self):
        '''test create'''
        obj = self.create_style()
        self.assertTrue(isinstance(obj, Style))


class MerchandiseHierarchyGroupStyleTest(TestCase):
    '''MerchandiseHierarchyGroupStyleTest'''

    def create_merchandise_hierarchyGroup_style(self):
        '''create'''
        return MerchandiseHierarchyGroupStyle.objects.create(ID_MRHRC_GP=MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(self), LU_STYL=StyleTest.create_style(self))

    def test_merchandise_hierarchyGroup_style(self):
        '''test create'''
        obj = self.create_merchandise_hierarchyGroup_style()
        self.assertTrue(isinstance(obj, MerchandiseHierarchyGroupStyle))


class ColorPaletteTest(TestCase):
    '''ColorPaletteTest'''

    def create_color_palette(self):
        '''create'''
        NM_PLTE_CLR = "Name Plate Colour"
        DE_PLTE_CLR = "Description Plate Colour"
        return ColorPalette.objects.create(NM_PLTE_CLR=NM_PLTE_CLR, DE_PLTE_CLR=DE_PLTE_CLR)

    def test_color_palette(self):
        '''test create'''
        obj = self.create_color_palette()
        self.assertTrue(isinstance(obj, ColorPalette))


class MerchandiseHierarchyGroupColorPaletteTest(TestCase):
    '''MerchandiseHierarchyGroupColorPaletteTest'''

    def create_merchandise_hierarchy_group_color_palette(self):
        '''create'''
        ID_MRHRC_GP = MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(
            self)
        ID_PLTE_CLR = ColorPaletteTest.create_color_palette(self)
        return MerchandiseHierarchyGroupColorPalette.objects.create(ID_MRHRC_GP=ID_MRHRC_GP, ID_PLTE_CLR=ID_PLTE_CLR)

    def test_merchandise_hierarchy_groupColor_palette(self):
        '''test create'''
        obj = self.create_merchandise_hierarchy_group_color_palette()
        self.assertTrue(isinstance(obj, MerchandiseHierarchyGroupColorPalette))


class ColorListAgencyTest(TestCase):
    '''ColorListAgencyTest'''

    def create_color_list_agency(self):
        '''create'''
        return ColorListAgency.objects.create(NM_AGY_CLR_LST="NM_AGY_CLR_LST")

    def test_color_list_agency(self):
        '''test create'''
        obj = self.create_color_list_agency()
        self.assertTrue(isinstance(obj, ColorListAgency))


class ColorTest(TestCase):
    '''ColorTest'''

    def craete_color(self):
        '''create'''
        CD_CLR = grs(4, '0123456789ABCDEF')
        NM_CLR = "Name of clor"
        DE_CLR = "Desc of color"
        ID_PLTE_CLR = ColorPaletteTest.create_color_palette(self)
        ID_AGY_CLR_LST = ColorListAgencyTest.create_color_list_agency(self)
        DE_MDFR = "Modification"
        return Color.objects.create(CD_CLR=CD_CLR, NM_CLR=NM_CLR, DE_CLR=DE_CLR, ID_PLTE_CLR=ID_PLTE_CLR, ID_AGY_CLR_LST=ID_AGY_CLR_LST, DE_MDFR=DE_MDFR)

    def test_color(self):
        '''test create'''
        obj = self.craete_color()
        self.assertTrue(isinstance(obj, Color))


class MerchandiseHierarchyGroupColorTest(TestCase):
    '''MerchandiseHierarchyGroupColorTest'''

    def create_merchandise_hierarchy_group_color(self):
        '''create'''
        ID_MRHRC_GP = MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(
            self)
        CD_CLR = ColorTest.craete_color(self)
        return MerchandiseHierarchyGroupColor.objects.create(ID_MRHRC_GP=ID_MRHRC_GP, CD_CLR=CD_CLR)

    def test_merchandise_hierarchy_group_color(self):
        '''test create'''
        obj = self.create_merchandise_hierarchy_group_color()
        self.assertTrue(isinstance(obj, MerchandiseHierarchyGroupColor))


class SizeFamilyTest(TestCase):
    '''SizeFamilyTest'''

    def create_size_family(self):
        '''create'''
        return SizeFamily.objects.create(NM_SZ_FMY="SizeFamilyName", DE_SZ_FMY="SizeFamilyDescription")

    def test_size_family(self):
        '''test create'''
        obj = self.create_size_family()
        self.assertTrue(isinstance(obj, SizeFamily))


class SizeTest(TestCase):
    '''SizeTest'''

    def create_size(self):
        '''create'''
        CD_SZ = grs(4, '0123456789ABCDEF')
        ID_SZ_FMY = SizeFamilyTest.create_size_family(self)
        ED_TB_SZ = grs(2, '0123456789ABCD')
        NM_TB_SZ = "Table name"
        DE_TB_SZ = "Description"
        ED_SZ_ACT = grs(4, "0123456789ABCDEF")
        DE_TYP_ACT_SZ = "Actual Size Type Description"
        DE_PRPTN_ACT_SZ = "Actual Size Proportion Description"
        return Size.objects.create(CD_SZ=CD_SZ, ID_SZ_FMY=ID_SZ_FMY, ED_TB_SZ=ED_TB_SZ,
                                   NM_TB_SZ=NM_TB_SZ, DE_TB_SZ=DE_TB_SZ, ED_SZ_ACT=ED_SZ_ACT, DE_TYP_ACT_SZ=DE_TYP_ACT_SZ,
                                   DE_PRPTN_ACT_SZ=DE_PRPTN_ACT_SZ)

    def test_size(self):
        '''test create'''
        obj = self.create_size()
        self.assertTrue(isinstance(obj, Size))


class MerchandiseHierarchyGroupSizeTest(TestCase):
    '''MerchandiseHierarchyGroupSizeTest'''

    def creat_merchandise_hierarchy_group_size(self):
        '''create'''
        ID_MRHRC_GP = MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(
            self)
        CD_SZ = SizeTest.create_size(self)
        ID_SZ_FMY = SizeFamilyTest.create_size_family(self)

        return MerchandiseHierarchyGroupSize.objects.create(ID_MRHRC_GP=ID_MRHRC_GP, CD_SZ=CD_SZ, ID_SZ_FMY=ID_SZ_FMY)

    def test_merchandise_hierarchy_group_size(self):
        '''test create'''
        obj = self.creat_merchandise_hierarchy_group_size()
        self.assertTrue(isinstance(obj, MerchandiseHierarchyGroupSize))


class MerchandiseTemplateTypeModelTest(TestCase):
    """Merchandise Template Type Model Test"""

    def create_merchandisetemplatetype(self):
        """create test model"""
        return MerchandiseTemplateType.objects.create(merchandisetemplatetypename=str(randint(0, 1000))+'Product')

    def test_merchandisetemplatetype(self):
        """test model creation"""
        obj = self.create_merchandisetemplatetype()
        self.assertTrue(isinstance(obj, MerchandiseTemplateType))


class MerchandiseTemplateModelTest(TestCase):
    """Merchandise Template Model Test"""

    def create_merchandisetemplate(self):
        """create test model"""
        template_type = MerchandiseTemplateTypeModelTest.create_merchandisetemplatetype(
            self)
        return MerchandiseTemplate.objects.create(merchandisetemplatename=str(randint(0, 1000))+'Template',
                                                  ID_MRHRC_TMP_TYP=template_type)

    def test_merchandisetemplate(self):
        """test model creation"""
        obj = self.create_merchandisetemplate()
        self.assertTrue(isinstance(obj, MerchandiseTemplate))


class MerchandiseTemplateControlsModelTest(TestCase):
    """Merchandise Template Controls Model Test"""

    def create_merchandisetemplatecontrols(self):
        """create test model"""
        template = MerchandiseTemplateModelTest.create_merchandisetemplate(
            self)
        form_field = CustomFormFieldModelTest.create_custom_form_field(self)
        return MerchandiseTemplateControls.objects.create(ID_MRHRC_TMP=template, ID_BA_CFF=form_field, merchandisetemplatecontroldescription='Description')

    def test_merchandisetemplatecontrols(self):
        """test model creation"""
        obj = self.create_merchandisetemplatecontrols()
        self.assertTrue(isinstance(obj, MerchandiseTemplateControls))


class MerchandiseTemplateControlValueModelTest(TestCase):
    """Merchandise Template Control Value Model Test"""

    def create_merchandisetemplatecontrolvalue(self):
        """create test model"""
        template_control = MerchandiseTemplateControlsModelTest.create_merchandisetemplatecontrols(
            self)
        form_field_val = CustomFormFieldValueModelTest.create_custom_form_field_value(
            self)
        return MerchandiseTemplateControlValue.objects.create(ID_MRHRC_TMP_CNT=template_control, ID_BA_CFF_VAL=form_field_val, merchandisetemplatecontrol_value="Red")

    def test_merchandisetemplatecontrolvalue(self):
        """test model creation"""
        obj = self.create_merchandisetemplatecontrolvalue()
        self.assertTrue(isinstance(obj, MerchandiseTemplateControlValue))

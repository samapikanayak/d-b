from django.test import TestCase
from store.models import Currency, ISO4217_CurrencyType, BusinessUnitGroup, BusinessUnit, WorkLocation, BusinessUnitGroupFunction, BusinessUnitGroupLevel
from django.utils.crypto import get_random_string as grs
from party.tests.test_models import ISO3166CountryModelTest, LanguageModelTest, OperationalPartyModelTest


class CurrencyModelTest(TestCase):
    '''
    Currency Model Test
    '''

    def create_currency(self, DE_CNY="Inidan Currency", SY_CNY = "", CD_ISO4217_CNY = "INR"):
        return Currency.objects.create(DE_CNY = DE_CNY, SY_CNY = SY_CNY, CD_ISO4217_CNY = CD_ISO4217_CNY)

    def test_create_currency(self):
        w = self.create_currency()
        self.assertTrue(isinstance(w, Currency))
        self.assertEqual(w.__unicode__(), w.CD_ISO4217_CNY)


class ISO4217CurrencyTypeModelTest(TestCase):

    def create_currency_type(self, CD_CNY_ISO_4217_NBR="100", NM_CNY = "Rupee"):
        iso_country = ISO3166CountryModelTest.create_iso03166_country(self)
        return ISO4217_CurrencyType.objects.create(CD_CNY_ISO_4217_NBR = CD_CNY_ISO_4217_NBR, NM_CNY = NM_CNY, CD_CY_ISO = iso_country)

    def test_create_currency_type(self):
        w = self.create_currency_type()
        self.assertTrue(isinstance(w, ISO4217_CurrencyType))
        self.assertEqual(w.__unicode__(), w.NM_CNY)


class BusinessUnitGroupModelTest(TestCase):

    def create_business_unit_grp(self, NM_BSNGP = "Business Unit Group Name"):
        lang_instance = LanguageModelTest.create_language(self)
        return BusinessUnitGroup.objects.create(ID_LGE = lang_instance, NM_BSNGP =NM_BSNGP)

    def test_business_unit_grp(self):
        w = self.create_business_unit_grp()
        self.assertTrue(isinstance(w, BusinessUnitGroup))
        self.assertEqual(w.__unicode__(), w.NM_BSNGP)



class BusinessUnitModelTest(BusinessUnitGroupModelTest, CurrencyModelTest, ISO4217CurrencyTypeModelTest, TestCase):

    def create_business_unit(self, TY_BSN_UN = "BU", NM_BSN_UN = "Business Unit"):
        bsns_grp_unit = BusinessUnitGroupModelTest.create_business_unit_grp(self)
        cur_instance = CurrencyModelTest.create_currency(self)
        iso_cur_instance = ISO4217CurrencyTypeModelTest.create_currency_type(self)
        opr_prty_instance = OperationalPartyModelTest.create_opr_prty(self)
        return BusinessUnit.objects.create(TY_BSN_UN = TY_BSN_UN, NM_BSN_UN=  NM_BSN_UN, ID_BSNGP = bsns_grp_unit, ID_CNY_LCL = cur_instance, CD_CNY_ISO_4217 = iso_cur_instance, ID_OPR_PRTY = opr_prty_instance)

    def test_business_unit(self):
        w = self.create_business_unit()
        self.assertTrue(isinstance(w, BusinessUnit))
        self.assertEqual(w.__unicode__(), w.TY_BSN_UN)


class WorkLocationModelTest(BusinessUnitModelTest, TestCase):

    def create_work_location(self):
        bu_instance = BusinessUnitModelTest.create_business_unit(self)
        return WorkLocation.objects.create(ID_BSN_UN = bu_instance)

    def test_create_work_location(self):
        w = self.create_work_location()
        self.assertTrue(isinstance(w, WorkLocation))
        self.assertEqual(w.__unicode__(), w.ID_LCN)

class BusinessUnitGroupFunctionModelTest(TestCase):
    def create_business_unit_group_function(self):
        NM_BSNGP_FNC = grs(40)
        return BusinessUnitGroupFunction.objects.create(NM_BSNGP_FNC=NM_BSNGP_FNC)
    
    def test_business_unit_group_function(self):
        w = self.create_business_unit_group_function()
        self.assertTrue(isinstance(w, BusinessUnitGroupFunction))

class BusinessUnitGroupLevelModelTest(TestCase):
    def create_business_unit_group_level(self):
        ID_BSNGP_FNC = BusinessUnitGroupFunctionModelTest.create_business_unit_group_function(self)
        NM_BSNGP_LV = grs(40)
        return BusinessUnitGroupLevel.objects.create(ID_BSNGP_FNC=ID_BSNGP_FNC, NM_BSNGP_LV=NM_BSNGP_LV)

    def test_business_unit_group_level(self):
        w = self.create_business_unit_group_level()
        self.assertTrue(isinstance(w, BusinessUnitGroupLevel))


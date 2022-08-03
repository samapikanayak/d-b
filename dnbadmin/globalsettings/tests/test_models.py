"""
Global Setting models test cases
"""
from random import randint
from globalsettings.models import GlobalSetting, BusinessUnitSetting
from basics.tests.test_models import DateFormatModelTest, TimezoneModelTest
from party.tests.test_models import LanguageModelTest
from store.tests.test_models import BusinessUnitModelTest
from django.test import TestCase


class GlobalSettingModelTest(TestCase):
    """GlobalSetting Model Test"""

    def create_globalsetting(self):
        """create test model"""
        name = str(randint(1000000, 9999999))+'- Setting Name'
        status = "A"
        language_instance = LanguageModelTest.create_language(
            self, str(randint(1, 9))+"ENG", "ENGLISH")
        dateformat_instance = DateFormatModelTest.create_dateformat(self)
        tzone_instance = TimezoneModelTest.create_timezone(self)
        instance = GlobalSetting.objects.create(
            name=name, status=status, ID_LGE=language_instance, ID_BA_DFMT=dateformat_instance, ID_BA_TZN=tzone_instance)
        return instance

    def test_globalsetting_creation(self):
        """test model creation"""
        obj = self.create_globalsetting()
        self.assertTrue(isinstance(obj, GlobalSetting))
        self.assertEqual(str(obj), obj.name)


class BusinessUnitSettingModelTest(TestCase):
    """BusinessUnitSetting Model Test"""

    def create_bsn_unit_setting(self):
        """create test model"""
        bunit_instance = BusinessUnitModelTest.create_business_unit(self)
        gsetting_instance = GlobalSettingModelTest.create_globalsetting(self)
        instance = BusinessUnitSetting.objects.create(
            ID_BSN_UN=bunit_instance, ID_GB_STNG=gsetting_instance)
        return instance

    def test_bsn_unit_setting_creation(self):
        """test model creation"""
        obj = self.create_bsn_unit_setting()
        self.assertTrue(isinstance(obj, BusinessUnitSetting))
        self.assertEqual(obj.getid(), obj.ID_BSN_UN_STNG)

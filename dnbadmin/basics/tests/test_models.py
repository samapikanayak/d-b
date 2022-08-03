"""
Basic common models test cases
"""
from random import randint
from basics.models import (BusinessUnitType, CustomFormField,
                           CustomFormFieldType, CustomFormFieldValue,
                           DateFormat, Timezone)
from django.test import TestCase

# models test


class DateFormatModelTest(TestCase):
    """Date Format Model Test"""

    def create_dateformat(self, name="d-m-Y"):
        """create test model"""
        instance = DateFormat.objects.create(name=name)
        return instance

    def test_dateformat_creation(self):
        """test model creation"""
        obj = self.create_dateformat()
        self.assertTrue(isinstance(obj, DateFormat))
        self.assertEqual(str(obj), obj.name)


class TimezoneModelTest(TestCase):
    """Timezone Model Test"""

    def create_timezone(self, gmt_offset="+05:30", country='India', timezone='Indian Standard Time', code='IST'):
        """create test model"""
        return Timezone.objects.create(gmt_offset=gmt_offset, country=country, timezone=timezone, code=code)

    def test_timezone_creation(self):
        """test model creation"""
        obj = self.create_timezone()
        self.assertTrue(isinstance(obj, Timezone))
        self.assertEqual(str(obj), obj.code)


class BusinessUnitTypeModelTest(TestCase):
    """Business Unit Type Model Test"""

    def create_business_unit_type(self, name="kg", status='A'):
        """create test model"""
        return BusinessUnitType.objects.create(name=name, status=status)

    def test_timezone_creation(self):
        """test model creation"""
        obj = self.create_business_unit_type()
        self.assertTrue(isinstance(obj, BusinessUnitType))
        self.assertEqual(str(obj), obj.name)


class CustomFormFieldTypeModelTest(TestCase):
    """Custom Form Field Type Model Test"""

    def create_custom_form_field_type(self):
        """create test model"""
        return CustomFormFieldType.objects.create(customformfieldtype_name=str(randint(0, 1000))+'Text Area')

    def test_custom_form_field_type(self):
        """test model creation"""
        obj = self.create_custom_form_field_type()
        self.assertTrue(isinstance(obj, CustomFormFieldType))


class CustomFormFieldModelTest(TestCase):
    """Custom Form Field Model Test"""

    def create_custom_form_field(self):
        """create test model"""
        field_type = CustomFormFieldTypeModelTest.create_custom_form_field_type(
            self)
        return CustomFormField.objects.create(customformfield_name=str(randint(0, 1000))+'Colours',
                                              ID_BA_CFF_TYP=field_type)

    def test_custom_form_field(self):
        """test model creation"""
        obj = self.create_custom_form_field()
        self.assertTrue(isinstance(obj, CustomFormField))


class CustomFormFieldValueModelTest(TestCase):
    """Custom Form Field Value Model Test"""

    def create_custom_form_field_value(self):
        """create test model"""
        form_field = CustomFormFieldModelTest.create_custom_form_field(
            self)
        return CustomFormFieldValue.objects.create(ID_BA_CFF=form_field, customformfield_value="Red")

    def test_custom_form_field_value(self):
        """test model creation"""
        obj = self.create_custom_form_field_value()
        self.assertTrue(isinstance(obj, CustomFormFieldValue))

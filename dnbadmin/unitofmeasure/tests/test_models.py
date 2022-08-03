''' Unit of Measure Model Unit Test '''
from django.test import TestCase
from unitofmeasure.models import UnitOfMeasure, UnitOfMeasureConversion

#! models test


class UnitOfMeasureModelTest(TestCase):
    ''' Unit of Measure Test Class'''

    def create_unit_measure(self, cd_uom="Kg", ty_uom="Kg", nm_uom="Kilogram", de_uom="Unit Description"):
        ''' Create unit of measure function '''
        return UnitOfMeasure.objects.create(CD_UOM=cd_uom, TY_UOM=ty_uom, NM_UOM=nm_uom, DE_UOM=de_uom)

    def test_create_unit_measure(self):
        ''' Create unit of measure test function '''
        w = self.create_unit_measure()
        self.assertTrue(isinstance(w, UnitOfMeasure))
        self.assertEqual(w.__unicode__(), w.CD_UOM)


class UnitOfMeasureConversionModelTest(UnitOfMeasureModelTest, TestCase):
    ''' Unit of Measure Conversion Unit Test '''

    def create_unit_measure_covn(self):
        ''' Create unit of measure conversion function '''
        return UnitOfMeasureConversion.objects.create()

    def test_create_unit_measure_conv(self):
        ''' Create unit of measure conversion test function '''
        w = self.create_unit_measure_covn()
        self.assertTrue(isinstance(w, UnitOfMeasureConversion))
        self.assertEqual(w.__unicode__(), w.ID_CVN_UOM)

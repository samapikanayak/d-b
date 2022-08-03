from django.test import TestCase
from ..models import *
from django.utils.crypto import get_random_string as grs
from party.tests.test_models import PartyModelTest
from worker.tests.test_models import ManufacturerModelTest, Manufacturer
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string as grs


class BrandModelTest(TestCase):
    def create_brand(self):
        NM_BRN = grs(4)
        ID_PRTY = PartyModelTest.create_party(self)
        DE_BRN = grs(40)
        CD_BRN_GRDG = grs(10)

        return Brand.objects.create(NM_BRN=NM_BRN, ID_PRTY=ID_PRTY, DE_BRN=DE_BRN, CD_BRN_GRDG=CD_BRN_GRDG)

    def test_brand(self):
        w = self.create_brand()
        self.assertTrue(isinstance(w, Brand))

class SubBrandModelTest(TestCase):
    def create_sub_brand(self):
        return SubBrand.objects.create(NM_BRN=BrandModelTest.create_brand(self), NM_SUB_BRN=grs(40), DE_SUB_BRN=grs(250))
        
    def test_sub_brand(self):
        w = self.create_sub_brand()
        self.assertTrue(isinstance(w, SubBrand))

class ManufacturerBrandModelTest(TestCase):
    def create_manufacture_brand(self):
        m = Manufacturer.objects.create()
        ID_MF = m
        NM_BRN = BrandModelTest.create_brand(self)
        DC_EF = timezone.now()
        DC_EP = timezone.now() + timedelta(seconds=0, minutes=0, hours=0, days=365)
        CD_STS = grs(2)

        return ManufacturerBrand.objects.create(ID_MF=ID_MF, NM_BRN=NM_BRN, DC_EF=DC_EF, DC_EP=DC_EP,CD_STS=CD_STS)

    def test_manufacture_brand(self):
        w = self.create_manufacture_brand()
        self.assertTrue(isinstance(w, ManufacturerBrand))

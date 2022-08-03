'''pos model test'''
from django.test import TestCase
from pos_department.models import POSDepartment, BusinessUnitGroupPOSDepartment
from sellingrule.tests.test_models import ItemSellingRuleTest
from store.tests.test_models import BusinessUnitGroupModelTest


class POSDepartmentModelTest(ItemSellingRuleTest, TestCase):
    '''pos create test model'''

    def create_pos(self):
        '''create obj'''
        selling_rule_instance = ItemSellingRuleTest.create_item_selling_rule(
            self)
        return POSDepartment.objects.create(ID_RU_ITM_SL=selling_rule_instance, NM_DPT_PS="POS Name", status="A")

    def test_create_pos(self):
        '''create obj test'''
        obj = self.create_pos()
        self.assertTrue(isinstance(obj, POSDepartment))


class BusinessUnitGroupPOSDepartmentModelTest(POSDepartmentModelTest, BusinessUnitGroupModelTest, TestCase):
    '''pos business unit group model test'''

    def create_pos_bngp(self):
        '''create obj'''
        pos_instance = POSDepartmentModelTest.create_pos(self)
        bsngp_instance = BusinessUnitGroupModelTest.create_business_unit_grp(
            self)
        return BusinessUnitGroupPOSDepartment.objects.create(ID_BSNGP=bsngp_instance, ID_DPT_PS=pos_instance)

    def test_create_pos_bngp(self):
        '''create obj test'''
        obj = self.create_pos_bngp()
        self.assertTrue(isinstance(obj, BusinessUnitGroupPOSDepartment))

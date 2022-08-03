'''Deposit Rule model Tests'''
from django.test import TestCase
from depositrule.models import DepositRule


class DepositRuleModelTest(TestCase):
    '''Deposit Rule Model Test'''

    def create_deposit_rule(self):
        '''Deposit rule craete'''
        deposit_amount = 12.05
        unit_of_measure_code = "lu"
        measure_amount = 12.05
        return DepositRule.objects.create(MO_DS=deposit_amount, LU_UOM_DS_PD=unit_of_measure_code, MO_UOM_DS_PD=measure_amount)

    def test_deposit_rule(self):
        '''deposit rule model test'''
        w = self.create_deposit_rule()
        self.assertTrue(isinstance(w, DepositRule))

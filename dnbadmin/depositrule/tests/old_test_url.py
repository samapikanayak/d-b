'''deposit rule url test cases'''
from django.test import TestCase
from django.urls import reverse, resolve
from depositrule.views import DepositRuleListCreate, DepositRuleRetriveUpdate

class DepositRuleUrlCreateListTest(TestCase):
    '''test cases for deposit rule urls'''
    def test_depositrule_url(self) -> None:
        '''test cases for deposit rule urls'''
        url = reverse("depositrule")
        self.assertEqual(resolve(url).func.view_class, DepositRuleListCreate)

    def test_detail_depositrule_url(self):
        '''deposit rule url test case'''
        url = reverse("detaildepositrule", args=["1"])
        self.assertEqual(resolve(url).func.view_class, DepositRuleRetriveUpdate)

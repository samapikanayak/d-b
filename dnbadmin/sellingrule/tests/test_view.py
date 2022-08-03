"""
selling rule api test view
"""
from rest_framework import status
from sellingrule.models import ItemSellingRule
from depositrule.tests.test_models import DepositRuleModelTest
from django.urls import reverse
from .test_setup import TestSetUp


class TestItemSellingRule(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_rule(self):
        '''selling rule create post'''
        dprule_instance = DepositRuleModelTest.create_deposit_rule(self)
        self.setting_data['ID_RU_DS'] = dprule_instance.ID_RU_DS
        response = self.client.post(
            reverse('sellingrule'), self.setting_data, format="json")
        return response


class TestListCreateItemSellingRule(TestItemSellingRule):
    ''' Test create  and list selling rule '''

    def test_should_not_create_wa_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_rule()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_wa_auth(self):
        '''create with auth test'''
        prev_count = ItemSellingRule.objects.all().count()
        self.authenticate()
        res = self.create_rule()
        self.assertEqual(ItemSellingRule.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['NM_RU_ITM_SL'], 'Test selling rule')

    def test_retrive_wa_list(self):
        '''retrive rule list'''
        self.authenticate()
        res = self.client.get(reverse('sellingrule'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)


class TestItemSellingRuleRetrieveUpdate(TestItemSellingRule):
    '''test retrive update rule'''

    def test_update_one_item(self):
        '''update one item'''
        self.authenticate()
        response = self.create_rule()
        self.setting_data['NM_RU_ITM_SL'] = "New one"
        self.setting_data['DE_RU_ITM_SL'] = "new title"
        res = self.client.put(reverse("sellingruledetail", kwargs={
                              'itemselling_id': response.data['ID_RU_ITM_SL']}), self.setting_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_wa = ItemSellingRule.objects.get(
            ID_RU_ITM_SL=response.data['ID_RU_ITM_SL'])
        self.assertEqual(updated_wa.NM_RU_ITM_SL, 'New one')
        self.assertEqual(updated_wa.DE_RU_ITM_SL, 'new title')

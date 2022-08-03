from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetUp
from product.models import ItemSellingPrices


class TestItemPriceRule(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_item_price_rule(self):
        '''global setting create post'''
        response = self.client.post(
            self.item_price_rule_get_create, self.setting_data, format="json")
        return response


class TestListCreateItemPriceRule(TestItemPriceRule):
    ''' Test create  and list item price rule '''

    def test_should_not_create_itempricerule_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_item_price_rule()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_itempricerule_auth(self):
        '''create with auth test'''
        prev_count = ItemSellingPrices.objects.all().count()
        self.authenticate()
        res = self.create_item_price_rule()
        self.assertEqual(ItemSellingPrices.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['ITM_SL_PRC_STATUS'], 'A')
        self.assertEqual(res.data['ITM_SL_PRC_NAME'],
                         'Item Selling Price Rule Name')

    def test_retrive_gsetting_list(self):
        '''retrive item_price_rule list'''
        self.authenticate()
        res = self.client.get(self.item_price_rule_get_create)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)

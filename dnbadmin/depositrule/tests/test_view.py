'''test views'''
from django.urls import reverse
from rest_framework import status
from ..models import DepositRule
from .test_setup import TestSetUp


class TestItemDepositRule(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_depositrule(self):
        '''deposit rule create post'''
        response = self.client.post(
            reverse('depositrule'), self.setting_data, format="json")
        return response


class TestListCreateDepositRule(TestItemDepositRule):
    ''' Test create  and list selling rule '''

    def test_should_not_create_wa_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_depositrule()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_wa_auth(self):
        '''create with auth test'''
        prev_count = DepositRule.objects.all().count()
        self.authenticate()
        res = self.create_depositrule()
        self.assertEqual(DepositRule.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['LU_UOM_DS_PD'], 'kg')

    def test_retrive_wa_list(self):
        '''retrive rule list'''
        self.authenticate()
        res = self.client.get(reverse('depositrule'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)

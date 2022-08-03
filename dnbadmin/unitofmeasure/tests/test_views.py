""" Unit of Measure Views Test """
from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetUp
from ..models import UnitOfMeasure, UnitOfMeasureConversion


class TestUnitOfMeasure(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_unit_of_measure(self):
        '''unit of measure create post'''
        response = self.client.post(
            self.uom_createlist_url, self.setting_data, format="json")
        return response

    def test_shouldnot_fetch_butype_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.uom_createlist_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_butype_list(self):
        '''retrive unit of measure list'''
        self.authenticate()
        res = self.client.get(self.uom_createlist_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_create_uom_auth(self):
        '''create with auth test'''
        prev_count = UnitOfMeasure.objects.all().count()
        self.authenticate()
        res = self.create_unit_of_measure()
        self.assertEqual(UnitOfMeasure.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # def test_update_one_item(self):
    #     '''update one item'''
    #     self.authenticate()
    #     response = self.create_unit_of_measure()
    #     res = self.client.get(reverse("Update Unit of Measure", kwargs={
    #                           'gsettingId': response.data['ID_GB_STNG']}))
    #     self.setting_data['ID_LGE'] = response.data['ID_LGE']
    #     self.setting_data['ID_BA_DFMT'] = response.data['ID_BA_DFMT']
    #     self.setting_data['ID_BA_TZN'] = response.data['ID_BA_TZN']
    #     self.setting_data['b_unit'] = res.data['b_unit_added']
    #     self.setting_data['name'] = "New one"
    #     self.setting_data['og_title'] = "new title"
    #     res = self.client.put(reverse("global_setting_update_del_view", kwargs={
    #                           'gsettingId': response.data['ID_GB_STNG']}), self.setting_data, format="json")
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     updated_gsetting = UnitOfMeasure.objects.get(
    #         ID_GB_STNG=response.data['ID_GB_STNG'])
    #     self.assertEqual(updated_gsetting.og_title, 'new title')
    #     self.assertEqual(updated_gsetting.name, 'New one')

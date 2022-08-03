"""
Global Setting api test view
"""
from random import randint
from rest_framework import status
from basics.tests.test_models import DateFormatModelTest, TimezoneModelTest
from party.tests.test_models import LanguageModelTest
from store.tests.test_models import BusinessUnitModelTest
from globalsettings.models import GlobalSetting
from django.urls import reverse
from .test_setup import TestSetUp


class TestGlobalSetting(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_gsetting(self):
        '''global setting create post'''
        language_instance = LanguageModelTest.create_language(
            self, str(randint(1, 9))+"ENG", "ENGLISH")
        dateformat_instance = DateFormatModelTest.create_dateformat(self)
        tzone_instance = TimezoneModelTest.create_timezone(self)
        bunit_instance = BusinessUnitModelTest.create_business_unit(self)
        self.setting_data['ID_LGE'] = language_instance.ID_LGE
        self.setting_data['ID_BA_DFMT'] = dateformat_instance.ID_BA_DFMT
        self.setting_data['ID_BA_TZN'] = tzone_instance.ID_BA_TZN
        self.setting_data['b_unit'] = str(bunit_instance.ID_BSN_UN)
        response = self.client.post(
            self.global_setting_createlist_url, self.setting_data, format="json")
        return response


class TestListCreateGlobalSetting(TestGlobalSetting):
    ''' Test create  and list globalsetting '''

    def test_should_not_create_gsetting_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_gsetting()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_gsetting_auth(self):
        '''create with auth test'''
        prev_count = GlobalSetting.objects.all().count()
        self.authenticate()
        res = self.create_gsetting()
        self.assertEqual(GlobalSetting.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'Baker City setting')
        self.assertEqual(res.data['meta_referral'], 'Baker City mref')

    def test_retrive_gsetting_list(self):
        '''retrive gsetting list'''
        self.authenticate()
        res = self.client.get(self.global_setting_createlist_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)


class TestGlobalSettingRetrieveUpdate(TestGlobalSetting):
    '''test retrive update delete global setting'''

    def test_retrive_one_item(self):
        '''retrive one item by pk'''
        self.authenticate()
        response = self.create_gsetting()
        res = self.client.get(reverse("global_setting_update_del_view", kwargs={
                              'gsettingId': response.data['ID_GB_STNG']}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        todo = GlobalSetting.objects.get(
            ID_GB_STNG=response.data['ID_GB_STNG'])
        self.assertEqual(todo.name, res.data['name'])
        self.assertEqual(todo.meta_referral, res.data['meta_referral'])

    def test_update_one_item(self):
        '''update one item'''
        self.authenticate()
        response = self.create_gsetting()
        res = self.client.get(reverse("global_setting_update_del_view", kwargs={
                              'gsettingId': response.data['ID_GB_STNG']}))
        self.setting_data['ID_LGE'] = response.data['ID_LGE']
        self.setting_data['ID_BA_DFMT'] = response.data['ID_BA_DFMT']
        self.setting_data['ID_BA_TZN'] = response.data['ID_BA_TZN']
        self.setting_data['b_unit'] = res.data['b_unit_added']
        self.setting_data['name'] = "New one"
        self.setting_data['og_title'] = "new title"
        res = self.client.put(reverse("global_setting_update_del_view", kwargs={
                              'gsettingId': response.data['ID_GB_STNG']}), self.setting_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_gsetting = GlobalSetting.objects.get(
            ID_GB_STNG=response.data['ID_GB_STNG'])
        self.assertEqual(updated_gsetting.og_title, 'new title')
        self.assertEqual(updated_gsetting.name, 'New one')


class TestGlobalSettingMultiplestatUpdate(TestGlobalSetting):
    '''test multiple status update'''

    def test_stat_updates_multiple_item(self):
        '''status update test'''
        self.authenticate()
        response = self.create_gsetting()
        res = self.client.put(
            reverse("global_setting_multiplestatusupdate"), {
                "ids": [
                    response.data['ID_GB_STNG']
                ],
                "status": "I"
            })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_gsetting = GlobalSetting.objects.get(
            ID_GB_STNG=response.data['ID_GB_STNG'])
        self.assertEqual(updated_gsetting.status, 'I')


class TestGlobalSettingDeleteMultiple(TestGlobalSetting):
    '''multiple delete test'''

    def test_delete_one_item(self):
        '''del one item'''
        self.authenticate()
        response = self.create_gsetting()
        prev_db_count = GlobalSetting.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)
        response = self.client.delete(reverse("global_setting_multipledelete"), {
            "ids": [
                response.data['ID_GB_STNG']
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GlobalSetting.objects.all().count(), 0)

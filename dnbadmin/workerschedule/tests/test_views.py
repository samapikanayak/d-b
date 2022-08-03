"""
Work Availability api test view
"""
from rest_framework import status
from workerschedule.models import TimeGroup
from unitofmeasure.tests.test_models import UnitOfMeasureModelTest
from django.urls import reverse
from .test_setup import TestSetUp


class TestWorkSchedule(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_wavailability(self):
        '''Work Availability create post'''
        uom_instance = UnitOfMeasureModelTest.create_unit_measure(self)
        self.setting_data['uom'] = uom_instance.ID_UOM
        response = self.client.post(
            reverse('work_schedule_createlist'), self.setting_data, format="json")
        return response


class TestListCreateWorkSchedule(TestWorkSchedule):
    ''' Test create  and list Work Availability '''

    def test_should_not_create_wa_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_wavailability()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_wa_auth(self):
        '''create with auth test'''
        prev_count = TimeGroup.objects.all().count()
        self.authenticate()
        res = self.create_wavailability()
        self.assertEqual(TimeGroup.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['NM_GP_TM'], 'Time Group 1')
        self.assertEqual(res.data['DE_GP_TM'], 'Time Group 1 Description')

    def test_retrive_wa_list(self):
        '''retrive wa list'''
        self.authenticate()
        res = self.client.get(reverse('work_schedule_createlist'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)


class TestWorkScheduleRetrieveUpdate(TestWorkSchedule):
    '''test retrive update Work Availability'''

    def test_update_one_item(self):
        '''update one item'''
        self.authenticate()
        response = self.create_wavailability()
        res = self.client.get(reverse("work_schedule_update_del_view", kwargs={
                              'bhourId': response.data['ID_GP_TM']}))
        self.setting_data['NM_GP_TM'] = "New one"
        self.setting_data['DE_GP_TM'] = "new title"
        res = self.client.put(reverse("work_schedule_update_del_view", kwargs={
                              'bhourId': response.data['ID_GP_TM']}), self.setting_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_wa = TimeGroup.objects.get(
            ID_GP_TM=response.data['ID_GP_TM'])
        self.assertEqual(updated_wa.NM_GP_TM, 'New one')
        self.assertEqual(updated_wa.DE_GP_TM, 'new title')


class TestWorkScheduleMultiplestatUpdate(TestWorkSchedule):
    '''test multiple status update'''

    def test_stat_updates_multiple_item(self):
        '''status update test'''
        self.authenticate()
        response = self.create_wavailability()
        res = self.client.put(
            reverse("work_schedule_multiplestatusupdate"), {
                "ids": [
                    response.data['ID_GP_TM']
                ],
                "status": "I"
            })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_gsetting = TimeGroup.objects.get(
            ID_GP_TM=response.data['ID_GP_TM'])
        self.assertEqual(updated_gsetting.status, 'I')


class TestWorkScheduleDeleteMultiple(TestWorkSchedule):
    '''multiple delete test'''

    def test_delete_one_item(self):
        '''del one item'''
        self.authenticate()
        response = self.create_wavailability()
        prev_db_count = TimeGroup.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)
        response = self.client.delete(reverse("work_schedule_multipledelete"), {
            "ids": [
                response.data['ID_GP_TM']
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TimeGroup.objects.all().count(), 0)

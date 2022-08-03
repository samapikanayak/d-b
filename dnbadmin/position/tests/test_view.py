'''Position views test'''
from rest_framework import status
from ..models import Position
from department.tests.test_models import DepartmentModelTest
from django.urls import reverse
from .test_setup import TestSetUp

class TestPosition(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_position(self):
        '''position create post'''
        department = DepartmentModelTest.create_department(self)
        self.setting_data['department_id'] = department.department_id
        response = self.client.post(
            reverse('position'), self.setting_data, format="json")
        return response


class TestListCreatePosition(TestPosition):
    ''' Test create  and list position '''

    def test_should_not_create_wa_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_position()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_wa_auth(self):
        '''create with auth test'''
        prev_count = Position.objects.all().count()
        self.authenticate()
        res = self.create_position()
        self.assertEqual(Position.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrive_pos_list(self):
        '''retrive pos list'''
        self.authenticate()
        res = self.client.get(reverse('position'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)

class TestPositionUpdate(TestPosition):
    '''test retrive update position '''

    def test_update_one_item(self):
        '''update one item'''
        self.authenticate()
        response = self.create_position()
        self.setting_data['NM_TTL'] = "New one"
        self.setting_data['status'] = "I"
        res = self.client.put(reverse("position-detail", kwargs={
                              'positionId': response.data['ID_PST']}), self.setting_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_wa = Position.objects.get(
            ID_PST=response.data['ID_PST'])
        self.assertEqual(updated_wa.NM_TTL, 'New one')
        self.assertEqual(updated_wa.status, 'I')

class TestPositionMultiplestatUpdate(TestPosition):
    '''test multiple status update'''

    def test_stat_updates_multiple_item(self):
        '''status update test'''
        self.authenticate()
        response = self.create_position()
        res = self.client.put(
            reverse("position-status-update"), {
                "ids": [
                    response.data['ID_PST']
                ],
                "status": "I"
            })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_gsetting = Position.objects.get(
            ID_PST=response.data['ID_PST'])
        self.assertEqual(updated_gsetting.status, 'I')

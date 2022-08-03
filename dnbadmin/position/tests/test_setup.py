"""
Position api test cases setup
"""
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    ''' Test Setup '''

    def setUp(self):
        ''' Here we setup data for unit test '''
        self.position_createlist_url = reverse('position')
        self.register_url = reverse('signup')
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        self.setting_data = {
            "NM_TTL": "position title",
            "status": "A",
            "DE_PST": "Position Description",
            "start_date": "2022-01-01",
            "end_date": "2022-01-01"
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

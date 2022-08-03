"""
deposit rule api test cases setup
"""
from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    ''' Test Setup '''

    def setUp(self):
        ''' Here we setup data for unit test '''
        self.register_url = reverse('signup')
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        self.setting_data = {
            "MO_DS": '7.9',
            "LU_UOM_DS_PD": "kg",
            "MO_UOM_DS_PD": "5.6",
            "SC_RU_DS": "A"
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

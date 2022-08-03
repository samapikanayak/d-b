"""
pos api test cases setup
"""
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
            "NM_DPT_PS": "Test Pos",
            "status": "A"
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

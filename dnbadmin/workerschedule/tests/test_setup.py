"""
Work Availability api test cases setup
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
            "NM_GP_TM": "Time Group 1",
            "DE_GP_TM": "Time Group 1 Description",
            "time_period": [
                {
                    "status": "A",
                    "NM_PD_TM": "Monday",
                    "WD": "1",
                    "TM_SRT": "09:00:00",
                    "TM_END": "19:00:00",
                    "SI_DRN": 9
                },
                {
                    "status": "A",
                    "NM_PD_TM": "Tuesday",
                    "WD": "2",
                    "TM_SRT": "09:00:00",
                    "TM_END": "19:00:00",
                    "SI_DRN": 9
                },
                {
                    "status": "A",
                    "NM_PD_TM": "Wednesday",
                    "WD": "3",
                    "TM_SRT": "09:00:00",
                    "TM_END": "19:00:00",
                    "SI_DRN": 9
                }
            ]
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

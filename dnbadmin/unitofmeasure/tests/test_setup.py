"""
Unit of measure test cases setup
"""
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    ''' Unit of Measure Test Setup '''

    def setUp(self):
        ''' Here we setup data for unit test '''
        self.uom_createlist_url = reverse(
            'Get Umit of Measure List')
        self.register_url = reverse('signup')
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        self.setting_data = {
            "uom_conversion": [
            ],
            "CD_UOM": "kg",
            "TY_UOM": "weight",
            "NM_UOM": "Kilogram",
            "DE_UOM": "Decsription",
            "STATUS_UOM": "A"
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

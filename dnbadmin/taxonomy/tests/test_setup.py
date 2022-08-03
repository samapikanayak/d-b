"""
taxonomy api test cases setup
"""
from random import randint
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
        self.setting_data_custom_form_field = {
            "customformfield_name": str(randint(0, 1000))+'Colours',
            "customformfield_description": "Lorem Ipsum",
            "customformfield_label": "Colours",
            "customformfield_values": [
                {
                    "customformfield_value": "Test",
                    "isdefault": 1
                }
            ]
        }
        self.setting_data_custom_form_field_value = {
            "customformfield_values": [
                {
                    "customformfield_value": "Test1",
                    "isdefault": 0
                }
            ]
        }
        self.setting_data_taxonomy_template = {
            "merchandisetemplatename": "Template 1",
            "description": "Lorem Ipsum",
            "status": "A",
            "customfields": [
                {
                    "merchandisetemplatecontroldescription": "Lorem Ipsum",
                    "customfield_values": [
                        {
                            "merchandisetemplatecontrol_value": "Test",
                            "isdefault": 1
                        }
                    ]
                }
            ]
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

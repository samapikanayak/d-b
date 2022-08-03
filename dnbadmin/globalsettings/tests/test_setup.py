"""
Global Setting api test cases setup
"""
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    ''' Test Setup '''

    def setUp(self):
        ''' Here we setup data for unit test '''
        self.global_setting_createlist_url = reverse(
            'global_setting_createlist')
        self.register_url = reverse('signup')
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        self.setting_data = {
            "name": "Baker City setting",
            "status": "A",
            "page_title": "Baker City Title",
            "page_description": "Baker City Descrp",
            "page_keyword": "Baker City kwd",
            "meta_locale": "Baker City ml",
            "meta_robots": "Baker City mr",
            "meta_referral": "Baker City mref",
            "meta_rights": "",
            "og_type": "",
            "og_url": "",
            "og_title": "",
            "og_description": "",
            "og_image": "",
            "og_locale": "",
            "twitter_card": "",
            "view_point": "",
            "script": ""
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

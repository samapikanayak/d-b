"""
Basic api test cases setup
"""
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    ''' Test Setup '''

    def setUp(self):
        ''' Here we setup data for unit test '''
        self.language_list_url = reverse(
            'language_list')
        self.dateformat_list_url = reverse(
            'dateformat_list')
        self.timezone_list_url = reverse(
            'timezone_list')
        self.bu_type_list_create_url = reverse(
            'Business Unit Type Get & Create')
        self.legalorg_type_list_create_url = reverse(
            'Legal Organization Type Get & Create')
        self.imageinfo_create_url = reverse(
            'imageinfo_create')
        self.register_url = reverse('signup')
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        self.bu_type_data = {
            'name': 'kg',
            'status': 'A'
        }
        self.legalorg_type_data = {
            'CD_LGL_ORGN_TYP': 'lglorg',
            'DE_LGL_ORGN_TYP': 'Description',
            'status': 'A'
        }
        self.imageinfo_data = [{
            'imagename': 'tedshirt.jpg',
            'imageurl': 'imageurl',
            'imagesize': '1234',
            'status': 'A'
        }]
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

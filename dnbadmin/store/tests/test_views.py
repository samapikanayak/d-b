"""
Basic api test view
"""
from rest_framework import status
from .test_setup import TestSetUp


class TestBasic(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")


class TestBusinessUnitList(TestBasic):
    ''' Test list BusinessUnit '''

    def test_shouldnot_fetch_businessunitlist_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.businessunitlist_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_businessunit_list(self):
        '''retrive businessunit list'''
        self.authenticate()
        res = self.client.get(self.businessunitlist_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

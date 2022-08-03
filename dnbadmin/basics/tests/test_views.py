"""
Basic api test view
"""
from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetUp
from ..models import BusinessUnitType, ImageInformation
from party.models import LegalOrganizationType


class TestBasic(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")


class TestLanguageList(TestBasic):
    ''' Test list language '''

    def test_shouldnot_fetch_languagelist_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.language_list_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_language_list(self):
        '''retrive language list'''
        self.authenticate()
        res = self.client.get(self.language_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestDateFormatList(TestBasic):
    ''' Test list DateFormat '''

    def test_shouldnot_fetch_dategormatlist_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.dateformat_list_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_dategormat_list(self):
        '''retrive dateformat list'''
        self.authenticate()
        res = self.client.get(self.dateformat_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestTimezoneList(TestBasic):
    ''' Test list Timezone '''

    def test_shouldnot_fetch_timezonelist_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.timezone_list_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_timezone_list(self):
        '''retrive dateformat list'''
        self.authenticate()
        res = self.client.get(self.timezone_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestBusinessUnitType(TestBasic):
    ''' Test Business Unit Type '''

    def create_businessunit_type(self):
        '''business unit type create post'''
        response = self.client.post(
            self.bu_type_list_create_url, self.bu_type_data, format="json")
        return response

    def test_shouldnot_fetch_butype_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.bu_type_list_create_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_butype_list(self):
        '''retrive business unit type list'''
        self.authenticate()
        res = self.client.get(self.bu_type_list_create_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_create_butype_auth(self):
        '''create with auth test'''
        prev_count = BusinessUnitType.objects.all().count()
        self.authenticate()
        res = self.create_businessunit_type()
        self.assertEqual(BusinessUnitType.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'kg')
        self.assertEqual(res.data['status'], 'A')

    def test_stat_updates_multiple_item(self):
        '''status update test'''
        self.authenticate()
        response = self.create_businessunit_type()
        res = self.client.put(
            reverse("Business Unit Type Multiple Status Update & Delete"), {
                "ids": [
                    response.data['id']
                ],
                "status": "I"
            })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_butype = BusinessUnitType.objects.get(
            id=response.data['id'])
        self.assertEqual(updated_butype.status, 'I')


class TestLegalOrgType(TestBasic):
    ''' Test Legal Organization Type '''

    def create_legalorg_type(self):
        '''legal org type create post'''
        response = self.client.post(
            self.legalorg_type_list_create_url, self.legalorg_type_data, format="json")
        return response

    def test_not_fetch_legalorg_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.legalorg_type_list_create_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_legalorg_list(self):
        '''retrive legal organization type list'''
        self.authenticate()
        res = self.client.get(self.legalorg_type_list_create_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_create_legalorg_auth(self):
        '''create with auth test'''
        prev_count = LegalOrganizationType.objects.all().count()
        self.authenticate()
        res = self.create_legalorg_type()
        self.assertEqual(
            LegalOrganizationType.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['CD_LGL_ORGN_TYP'], 'lglorg')
        self.assertEqual(res.data['status'], 'A')


class TestImageInfo(TestBasic):
    ''' Test Image Information '''

    def create_imageinfo(self):
        '''image info create post'''
        response = self.client.post(
            self.imageinfo_create_url, self.imageinfo_data, format="json")
        return response

    def test_not_fetch_imageinfo_with_no_auth(self):
        '''create with no auth test'''
        res = self.client.get(self.imageinfo_create_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_imageinfo_list(self):
        '''retrive image info list'''
        self.authenticate()
        res = self.client.get(self.imageinfo_create_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_create_imageinfo_auth(self):
        '''create with auth test'''
        prev_count = ImageInformation.objects.all().count()
        self.authenticate()
        res = self.create_imageinfo()
        self.assertEqual(
            ImageInformation.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

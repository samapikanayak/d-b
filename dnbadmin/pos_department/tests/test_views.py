"""
POS api test view
"""
from rest_framework import status
from pos_department.models import POSDepartment
from sellingrule.tests.test_models import ItemSellingRuleTest
from store.tests.test_models import BusinessUnitGroupModelTest
from django.urls import reverse
from .test_setup import TestSetUp


class TestPOSDepartment(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_pos(self):
        '''pos create post'''
        selling_rule_instance = ItemSellingRuleTest.create_item_selling_rule(
            self)
        bsngp_instance = BusinessUnitGroupModelTest.create_business_unit_grp(
            self)
        self.setting_data['ID_RU_ITM_SL'] = selling_rule_instance.ID_RU_ITM_SL
        self.setting_data['ID_BSNGP'] = bsngp_instance.ID_BSNGP
        response = self.client.post(
            reverse('pos_dept_createlist'), self.setting_data, format="json")
        return response


class TestListCreatePOSDepartment(TestPOSDepartment):
    ''' Test create  and list pos '''

    def test_should_not_create_wa_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_pos()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_wa_auth(self):
        '''create with auth test'''
        prev_count = POSDepartment.objects.all().count()
        self.authenticate()
        res = self.create_pos()
        self.assertEqual(POSDepartment.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['NM_DPT_PS'], 'Test Pos')

    def test_retrive_pos_list(self):
        '''retrive pos list'''
        self.authenticate()
        res = self.client.get(reverse('pos_dept_createlist'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)


class TestPOSDepartmentRetrieveUpdate(TestPOSDepartment):
    '''test retrive update pos'''

    def test_update_one_item(self):
        '''update one item'''
        self.authenticate()
        response = self.create_pos()
        self.setting_data['NM_DPT_PS'] = "New one"
        self.setting_data['status'] = "I"
        res = self.client.put(reverse("pos_dept_update_del_view", kwargs={
                              'posId': response.data['ID_DPT_PS']}), self.setting_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_wa = POSDepartment.objects.get(
            ID_DPT_PS=response.data['ID_DPT_PS'])
        self.assertEqual(updated_wa.NM_DPT_PS, 'New one')
        self.assertEqual(updated_wa.status, 'I')


class TestPOSDepartmentMultiplestatUpdate(TestPOSDepartment):
    '''test multiple status update'''

    def test_stat_updates_multiple_item(self):
        '''status update test'''
        self.authenticate()
        response = self.create_pos()
        res = self.client.put(
            reverse("pos_dept_multiplestatusupdate"), {
                "ids": [
                    response.data['ID_DPT_PS']
                ],
                "status": "I"
            })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_gsetting = POSDepartment.objects.get(
            ID_DPT_PS=response.data['ID_DPT_PS'])
        self.assertEqual(updated_gsetting.status, 'I')


class TestPOSDepartmentDeleteMultiple(TestPOSDepartment):
    '''multiple delete test'''

    def test_delete_one_item(self):
        '''del one item'''
        self.authenticate()
        response = self.create_pos()
        prev_db_count = POSDepartment.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)
        response = self.client.delete(reverse("pos_dept_multipledelete"), {
            "ids": [
                response.data['ID_DPT_PS']
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(POSDepartment.objects.all().count(), 0)

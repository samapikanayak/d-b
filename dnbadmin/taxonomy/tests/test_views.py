"""
taxonomy api test view
"""
from rest_framework import status
from basics.models import CustomFormField, CustomFormFieldValue
from basics.tests.test_models import CustomFormFieldTypeModelTest, CustomFormFieldModelTest, CustomFormFieldValueModelTest
from taxonomy.models import MerchandiseTemplate
from taxonomy.tests.test_models import MerchandiseTemplateTypeModelTest
from django.urls import reverse
from .test_setup import TestSetUp


class TestTaxonomyTemplate(TestSetUp):
    '''common test case functions'''

    def authenticate(self):
        '''user authentication'''
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def create_custom_form_field(self):
        '''cff create post'''
        field_type_instance = CustomFormFieldTypeModelTest.create_custom_form_field_type(
            self)
        self.setting_data_custom_form_field['ID_BA_CFF_TYP'] = field_type_instance.ID_BA_CFF_TYP
        response = self.client.post(
            reverse('custom_field_createlist'), self.setting_data_custom_form_field, format="json")
        return response

    def create_taxonomy_template(self):
        '''taxonomy template create post'''
        template_type_instance = MerchandiseTemplateTypeModelTest.create_merchandisetemplatetype(
            self)
        custom_form_field_instance = CustomFormFieldModelTest.create_custom_form_field(
            self)
        custom_form_field_value_instance = CustomFormFieldValueModelTest.create_custom_form_field_value(
            self)
        self.setting_data_taxonomy_template['ID_MRHRC_TMP_TYP'] = template_type_instance.ID_MRHRC_TMP_TYP
        self.setting_data_taxonomy_template['customfields'][0]['ID_BA_CFF'] = custom_form_field_instance.ID_BA_CFF
        self.setting_data_taxonomy_template['customfields'][0]['customfield_values'][
            0]['ID_BA_CFF_VAL'] = custom_form_field_value_instance.ID_BA_CFF_VAL
        response = self.client.post(
            reverse('taxonomy_template_createlist'), self.setting_data_taxonomy_template, format="json")
        return response


class TestMerchandiseTemplate(TestTaxonomyTemplate):
    '''Template related test'''

    def test_taxonomy_template_type_list(self):
        '''retrive template type list'''
        self.authenticate()
        res = self.client.get(reverse('taxonomy_template_type_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_not_create_taxonomy_template_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_taxonomy_template()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_taxonomy_template_auth(self):
        '''create with auth test'''
        prev_count = MerchandiseTemplate.objects.all().count()
        self.authenticate()
        res = self.create_taxonomy_template()
        self.assertEqual(
            MerchandiseTemplate.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['merchandisetemplatename'], 'Template 1')

    def test_retrive_taxonomy_template_list(self):
        '''retrive taxonomy template list'''
        self.authenticate()
        res = self.client.get(reverse('taxonomy_template_createlist'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)

    def test_update_one_item(self):
        '''update one item'''
        self.authenticate()
        response = self.create_taxonomy_template()
        self.setting_data_taxonomy_template['merchandisetemplatename'] = "New one"
        self.setting_data_taxonomy_template['status'] = "I"
        res = self.client.put(reverse("taxonomy_template_update_del_view", kwargs={
                              'taxtempId': response.data['ID_MRHRC_TMP']}), self.setting_data_taxonomy_template, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_wa = MerchandiseTemplate.objects.get(
            ID_MRHRC_TMP=response.data['ID_MRHRC_TMP'])
        self.assertEqual(updated_wa.merchandisetemplatename, 'New one')
        self.assertEqual(updated_wa.status, 'I')

    def test_stat_updates_multiple_item(self):
        '''status update test'''
        self.authenticate()
        response = self.create_taxonomy_template()
        res = self.client.put(
            reverse("taxonomy_template_multiplestatusupdate"), {
                "ids": [
                    response.data['ID_MRHRC_TMP']
                ],
                "status": "I"
            })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_gsetting = MerchandiseTemplate.objects.get(
            ID_MRHRC_TMP=response.data['ID_MRHRC_TMP'])
        self.assertEqual(updated_gsetting.status, 'I')

    def test_delete_one_item(self):
        '''del one item'''
        self.authenticate()
        response = self.create_taxonomy_template()
        prev_db_count = MerchandiseTemplate.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)
        response = self.client.delete(reverse("taxonomy_template_multipledelete"), {
            "ids": [
                response.data['ID_MRHRC_TMP']
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MerchandiseTemplate.objects.all().count(), 0)


class TestCustomFormField(TestTaxonomyTemplate):

    def test_custom_form_field_type_list(self):
        '''retrive custom field type list'''
        self.authenticate()
        res = self.client.get(reverse('custom_form_field_type_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_not_create_cff_with_no_auth(self):
        '''create with no auth test'''
        res = self.create_custom_form_field()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_cff_auth(self):
        '''create with auth test'''
        prev_count = CustomFormField.objects.all().count()
        self.authenticate()
        res = self.create_custom_form_field()
        self.assertEqual(CustomFormField.objects.all().count(), prev_count+1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['customformfield_label'], 'Colours')

    def test_retrive_cff_list(self):
        '''retrive cff list'''
        self.authenticate()
        res = self.client.get(reverse('custom_field_createlist'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data['results'], list)

    def test_should_create_cff_value(self):
        '''create with auth test'''
        self.authenticate()
        response = self.create_custom_form_field()
        self.setting_data_custom_form_field_value['customformfield_values'][
            0]['ID_BA_CFF'] = response.data['ID_BA_CFF']
        res = self.client.post(
            reverse('custom_field_value_createlist'), self.setting_data_custom_form_field_value, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_custom_field_value_multipledelete(self):
        '''del one item'''
        self.authenticate()
        self.create_custom_form_field()
        response = self.client.get(reverse('custom_field_createlist'))
        prev_db_count = CustomFormFieldValue.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)
        response = self.client.delete(reverse("custom_field_value_multipledelete"), {
            "ids": [
                response.data['results'][0]['customformfield_values'][0]['ID_BA_CFF_VAL']
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomFormFieldValue.objects.all().count(), 0)

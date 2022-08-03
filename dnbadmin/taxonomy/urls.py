'''global setting url'''
from django.urls import path

from taxonomy.views import (CustomFormFieldCreate, CustomFormFieldTypeList,
                            CustomFormFieldValueCreate,
                            CustomFormFieldValueDeleteMultipleView,
                            MerchandiseTemplateControlsDeleteMultipleView,
                            MerchandiseTemplateControlsRetrieveUpdate,
                            MerchandiseTemplateCreate,
                            MerchandiseTemplateRetrieveUpdate,
                            MerchandiseTemplateTypeList,
                            MerchandiseTemplatestatusUpdateMultipleView,
                            MerchandiseTemplateDeleteMultipleView)

urlpatterns = [
    path('templatetype/', MerchandiseTemplateTypeList.as_view(),
         name='taxonomy_template_type_list'),
    path('customformfieldtype/', CustomFormFieldTypeList.as_view(),
         name='custom_form_field_type_list'),
    path('customformfield/', CustomFormFieldCreate.as_view(),
         name='custom_field_createlist'),
    path('customformfieldvalue/', CustomFormFieldValueCreate.as_view(),
         name='custom_field_value_createlist'),
    path('customformfieldvalue/delete/',
         CustomFormFieldValueDeleteMultipleView.as_view(), name='custom_field_value_multipledelete'),
    path('template/', MerchandiseTemplateCreate.as_view(),
         name='taxonomy_template_createlist'),
    path('template/<int:taxtempId>/', MerchandiseTemplateRetrieveUpdate.as_view(),
         name='taxonomy_template_update_del_view'),
    path('template/statusupdate/',
         MerchandiseTemplatestatusUpdateMultipleView.as_view(), name='taxonomy_template_multiplestatusupdate'),
    path('template/delete/',
         MerchandiseTemplateDeleteMultipleView.as_view(), name='taxonomy_template_multipledelete'),
    path('customfield/<int:cfield_Id>/', MerchandiseTemplateControlsRetrieveUpdate.as_view(),
         name='taxonomy_template_control_update_del_view'),
    path('customfield/delete/',
         MerchandiseTemplateControlsDeleteMultipleView.as_view(), name='taxonomy_template_control_multipledelete'),
]

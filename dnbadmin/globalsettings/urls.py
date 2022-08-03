'''global setting url'''
from django.urls import path
from .views import ChangePassword, GlobalSettingCreate, GlobalSettingRetrieveUpdate, GlobalSettingstatusUpdateMultipleView, GlobalSettingDeleteMultipleView

urlpatterns = [
    path('setting/', GlobalSettingCreate.as_view(),
         name='global_setting_createlist'),
    path('setting/<int:gsettingId>/', GlobalSettingRetrieveUpdate.as_view(),
         name='global_setting_update_del_view'),
    path('setting/statusupdate/',
         GlobalSettingstatusUpdateMultipleView.as_view(), name='global_setting_multiplestatusupdate'),
    path('setting/delete/',
         GlobalSettingDeleteMultipleView.as_view(), name='global_setting_multipledelete'),
    path("changepassword", ChangePassword.as_view())
]

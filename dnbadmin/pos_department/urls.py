'''global setting url'''
from django.urls import path
from .views import POSDepartmentCreate, POSDepartmentRetrieveUpdate, POSDepartmentstatusUpdateMultipleView, POSDepartmentDeleteMultipleView

urlpatterns = [
    path('', POSDepartmentCreate.as_view(),
         name='pos_dept_createlist'),
    path('<int:posId>/', POSDepartmentRetrieveUpdate.as_view(),
         name='pos_dept_update_del_view'),
    path('statusupdate/',
         POSDepartmentstatusUpdateMultipleView.as_view(), name='pos_dept_multiplestatusupdate'),
    path('delete/',
         POSDepartmentDeleteMultipleView.as_view(), name='pos_dept_multipledelete'),
]

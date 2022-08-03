'''urls for department'''
from django.urls import path
from .views import DepartmentListCreateView, DepartmentRetriveUpdate, DepartmentstatusUpdateMultipleView, DepartmentDeleteMultipleView

urlpatterns = [
    path("",DepartmentListCreateView.as_view(), name="department"),
    path("<int:departmentId>/",DepartmentRetriveUpdate.as_view(), name="department-detail"),
    path("statusupdate/",DepartmentstatusUpdateMultipleView.as_view(), name="department-status-update"),
    path("delete/",DepartmentDeleteMultipleView.as_view(), name="department-delete"),
]

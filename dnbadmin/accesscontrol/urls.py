''' Accesscontrol Urls File '''
from django.urls import path
from .views import PermissionResource, WorkGroupResource, WorkGroupUpdate

urlpatterns = [
    path('resourcelist/', PermissionResource.as_view(), name='resource_list'),
    path('<workgroupId>/', WorkGroupUpdate.as_view(),
         name='workergroup_resource_update'),
    path('', WorkGroupResource.as_view(), name='workergroup_resource_create'),
]

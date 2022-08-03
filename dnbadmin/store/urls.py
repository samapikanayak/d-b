'''global setting url'''
from django.urls import path
from .views import BusinessUnitList, BusinessUnitGroupList

urlpatterns = [
    path('businessunitlist/', BusinessUnitList.as_view(),
         name='businessunit_list'),
    path('businessunitgrouplist/', BusinessUnitGroupList.as_view(),
         name='businessunit_group_list'),
]

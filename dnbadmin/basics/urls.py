'''global setting url'''
from django.urls import path
from .views import LanguageList, DateFormatList, TimezoneList, BusinessUnitTypeCreateViews, BusinessUnitTypeUpdateViews, BusinessUnitTypeMultipleStatusUpdate, LegalOrgTypeCreateViews, LegalOrgTypeMultipleStatusUpdate, LegalOrgTypeUpdateViews, ImageInfoCreateViews, ImageInfoUpdateViews, ImageOnfoMultipleStatusUpdate

urlpatterns = [
    path('language/', LanguageList.as_view(),
         name='language_list'),
    path('dateformat/', DateFormatList.as_view(),
         name='dateformat_list'),
    path('timezone/', TimezoneList.as_view(),
         name='timezone_list'),
    path('businessunittype/multiple/', BusinessUnitTypeMultipleStatusUpdate.as_view(),
         name='Business Unit Type Multiple Status Update & Delete'),
    path('businessunittype/', BusinessUnitTypeCreateViews.as_view(),
         name='Business Unit Type Get & Create'),
    path('businessunittype/<butypId>/', BusinessUnitTypeUpdateViews.as_view(),
         name='Business Unit Type Update & Retrive'),
    path('legalorgtype/multiple/', LegalOrgTypeMultipleStatusUpdate.as_view(),
         name='Legal Organization Type Multiple Status Update & Delete'),
    path('legalorgtype/', LegalOrgTypeCreateViews.as_view(),
         name='Legal Organization Type Get & Create'),
    path('legalorgtype/<legalorgtypCd>/', LegalOrgTypeUpdateViews.as_view(),
         name='Legal Organization Type Update & Retrive'),
    path('imageinfo/', ImageInfoCreateViews.as_view(),
         name='imageinfo_create'),
    path('imageinfo/<imageinfoId>', ImageInfoUpdateViews.as_view(),
         name='imageinfo_update'),
    path('imageinfo/multiple/', ImageOnfoMultipleStatusUpdate.as_view(),
         name='imageinfo_multiple_status_update_delete'),
]

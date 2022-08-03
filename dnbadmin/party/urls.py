'''party urls'''
from django.urls import path
from .views import TestClass, ContactPurposeTypeList, ContactMethodTypeList, CountryList, StateList

urlpatterns = [
    path('allparty/', TestClass.as_view()),
    #######Party contact method start########
    path('contactpurpose/', ContactPurposeTypeList.as_view()),
    path('contactmethod/', ContactMethodTypeList.as_view()),
    path('country/', CountryList.as_view()),
    path('state/', StateList.as_view()),
    #######Party contact method end########
]

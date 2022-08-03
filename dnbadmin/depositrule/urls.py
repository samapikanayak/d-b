'''deposit rule urls'''
from django.urls import path
from .views import DepositRuleListCreate, DepositRuleRetriveUpdate, DepositRuleMultipleDelete, DepositRulestatusUpdateMultipleView

urlpatterns = [
    path("", DepositRuleListCreate.as_view(), name="depositrule"),
    path("<int:depositrule_id>/", DepositRuleRetriveUpdate.as_view(),
         name="detaildepositrule"),
    path("delete/", DepositRuleMultipleDelete.as_view(),
         name="depositrulemultipledelete"),
    path("statusupdate/", DepositRulestatusUpdateMultipleView.as_view(),
         name="depositrulemultiplestatusupdate"),
]

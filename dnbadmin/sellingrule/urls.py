'''selling rule urls'''
from django.urls import path
from .views import ItemSellingRuleRetriveUpdate, ItemSellingRuleListCreate, ItemTenderRestrictionGroupListCreate, ItemTenderRestrictionGroupRetriveUpdate, SellingRuleMultipleDelete, SellingRulestatusUpdateMultipleView

urlpatterns = [
    path("itemtendergroup", ItemTenderRestrictionGroupListCreate.as_view(),
         name="itemtendergroup"),
    path("itemtendergroup/<int:itemtender_id>",
         ItemTenderRestrictionGroupRetriveUpdate.as_view(), name="itemtendergroupdetail"),
    path("itemselling/", ItemSellingRuleListCreate.as_view(), name="sellingrule"),
    path("itemselling/<itemselling_id>/",
         ItemSellingRuleRetriveUpdate.as_view(), name="sellingruledetail"),
    path("delete/", SellingRuleMultipleDelete.as_view(),
         name="sellingrulemultipledelete"),
    path("sellingrule/statusupdate/", SellingRulestatusUpdateMultipleView.as_view(),
         name="sellingrulemultiplestatusupdate"),
]

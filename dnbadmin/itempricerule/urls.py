''' Item Price Rule url'''
from django.urls import path
from .views import ItemPriceRuleViews, ItemPriceRuleUpdateViews, ItemPriceRuleMultipleStatusUpdate

urlpatterns = [
    path('multiple/', ItemPriceRuleMultipleStatusUpdate.as_view(),
         name='item_price_rule_multiple_status_update_delete'),
    path('<itemPriceRuleID>/', ItemPriceRuleUpdateViews.as_view(),
         name='item_price_rule_updtae'),
    path('', ItemPriceRuleViews.as_view(),
         name='item_price_rule_get_create'),

]

'''operator url'''
from django.urls import path

from .views import (OperatorCreate, OperatorDeleteMultipleView,
                    OperatorRetrieveUpdate, OperatorstatusUpdateMultipleView)

urlpatterns = [
    path('', OperatorCreate.as_view(),
         name='operator_createlist'),
    path('<int:oprId>/', OperatorRetrieveUpdate.as_view(),
         name='operator_update_del_view'),
    path('statusupdate/',
         OperatorstatusUpdateMultipleView.as_view(), name='operator_multiplestatusupdate'),
    path('delete/',
         OperatorDeleteMultipleView.as_view(), name='operator_multipledelete'),
]

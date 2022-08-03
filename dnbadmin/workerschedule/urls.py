'''global setting url'''
from django.urls import path
from .views import WorkScheduleCreate, WorkScheduleRetrieveUpdate, WorkSchedulestatusUpdateMultipleView, WorkScheduleDeleteMultipleView

urlpatterns = [
    path('', WorkScheduleCreate.as_view(),
         name='work_schedule_createlist'),
    path('<int:bhourId>/', WorkScheduleRetrieveUpdate.as_view(),
         name='work_schedule_update_del_view'),
    path('statusupdate/',
         WorkSchedulestatusUpdateMultipleView.as_view(), name='work_schedule_multiplestatusupdate'),
    path('delete/',
         WorkScheduleDeleteMultipleView.as_view(), name='work_schedule_multipledelete'),
]

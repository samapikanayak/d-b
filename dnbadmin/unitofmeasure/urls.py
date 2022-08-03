''' Unit Of Measure Url's '''
from django.urls import path
from .views import UnitOfMeasureGet, UnitOfMeasureUpdate, UnitOfMeasureMultipleStatusUpdate

urlpatterns = [
    path('', UnitOfMeasureGet.as_view(), name='Get Umit of Measure List'),
    path('<int:unitofmeasureId>/', UnitOfMeasureUpdate.as_view(),
         name='Update Unit of Measure'),
    path('multiple/', UnitOfMeasureMultipleStatusUpdate.as_view(),
         name='Update Unit of Measure Status'),

]

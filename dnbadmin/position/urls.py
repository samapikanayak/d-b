'''Position urls'''
from django.urls import path
from .views import PositionListCreateView, PositionRetriveUpdate, PositionStatusUpdate, PositionMultipleDelete

urlpatterns = [
    path("", PositionListCreateView.as_view(), name="position"),
    path("statusupdate/", PositionStatusUpdate.as_view(), name="position-status-update"),
    path("delete/", PositionMultipleDelete.as_view(), name="position-delete"),
    path("<positionId>/", PositionRetriveUpdate.as_view(), name="position-detail"),
]

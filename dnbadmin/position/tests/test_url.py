'''url test for position'''
from django.urls import reverse, resolve
from django.test import TestCase
from ..views import PositionListCreateView, PositionRetriveUpdate, PositionStatusUpdate, PositionMultipleDelete


class PositionUrlTest(TestCase):
    '''Position URL test'''
    def test_position_list_create(self):
        '''position listcreate url'''
        self.url = reverse("position")
        self.assertEqual(resolve(self.url).func.view_class, PositionListCreateView)
    def test_position_update(self):
        '''position update url'''
        self.url = reverse("position-detail", args=[1])
        self.assertEqual(resolve(self.url).func.view_class, PositionRetriveUpdate)
    def test_position_status_update(self):
        '''position status update url'''
        self.url = reverse("position-status-update")
        self.assertEqual(resolve(self.url).func.view_class, PositionStatusUpdate)
    def test_position_multiple_delete(self):
        '''position multiple delete url'''
        self.url = reverse("position-delete")
        self.assertEqual(resolve(self.url).func.view_class, PositionMultipleDelete)


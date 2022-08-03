from django.test import TestCase
from django.urls import reverse, resolve
from ..views import DepartmentListCreateView, DepartmentRetriveUpdate, DepartmentstatusUpdateMultipleView, DepartmentDeleteMultipleView

class DepartmentUrlTest(TestCase):
    def test_department_get_create(self):
        self.url = reverse("department")
        self.assertEqual(resolve(self.url).func.view_class, DepartmentListCreateView)
    def test_department_retrive_update(self):
        self.url = reverse("department-detail", args=[2])
        self.assertEqual(resolve(self.url).func.view_class, DepartmentRetriveUpdate)
    def test_department_status_update(self):
        self.url = reverse("department-status-update")
        self.assertEqual(resolve(self.url).func.view_class, DepartmentstatusUpdateMultipleView)
    def test_department_multi_delete(self):
        self.url = reverse("department-delete")
        self.assertEqual(resolve(self.url).func.view_class, DepartmentDeleteMultipleView)
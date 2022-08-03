from datetime import datetime
from django.test import TestCase
from party.models import PartyRole, PartyType, Party, PartyRoleAssignment
from worker.models import *
from django.utils import timezone
from random import randrange
from party.tests.test_models import PartyRoleAssgnModelTest


class WorkerModelTest(TestCase):

    def create_worker(self, TY_WRKR = "WT"):
        prty_ro_asgmt_inst = PartyRoleAssgnModelTest.create_prty_role_assign(self)
        return Worker.objects.create(TY_WRKR=TY_WRKR, ID_PRTY_RO_ASGMT = prty_ro_asgmt_inst)

    def test_create_worker(self):
        w = self.create_worker()
        self.assertTrue(isinstance(w, Worker))
        self.assertEqual(w.__unicode__(), w.TY_WRKR)


class EmployeeModelTest(WorkerModelTest, TestCase):

    def create_employee(self, SC_EM = "WT"):
        worker_instance = WorkerModelTest.create_worker(self)
        return Employee.objects.create(SC_EM=SC_EM, ID_WRKR = worker_instance)

    def test_create_employee(self):
        w = self.create_employee()
        self.assertTrue(isinstance(w, Employee))
        self.assertEqual(w.__unicode__(), w.SC_EM)

class VendorModelTest(TestCase):

    def create_vendor(self, TY_VN = "B2B"):
        prty_ro_asgmt_inst = PartyRoleAssgnModelTest.create_prty_role_assign(self)
        return Vendor.objects.create(TY_VN = TY_VN, ID_PRTY_RO_ASGMT = prty_ro_asgmt_inst)

    def test_create_vendor(self):
        w = self.create_vendor()
        self.assertTrue(isinstance(w, Vendor))
        self.assertEqual(w.__unicode__(), w.TY_VN)


class ContractorModelTest(WorkerModelTest, VendorModelTest, TestCase):

    def create_contractor(self):
        worker_instance = WorkerModelTest.create_worker(self)
        vendor_instance = VendorModelTest.create_vendor(self)
        return Contractor.objects.create(ID_VN = vendor_instance, ID_WRKR = worker_instance)

    def test_create_contractor(self):
        w = self.create_contractor()
        self.assertTrue(isinstance(w, Contractor))
        self.assertEqual(w.__unicode__(), w.ID_CNTR)

class ManufacturerModelTest(TestCase):
    def test_manufacturer(self):
        w = Manufacturer.objects.create()
        self.assertTrue(isinstance(w, Manufacturer))
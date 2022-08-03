from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from accesscontrol.models import *
from worker.tests.test_models import WorkerModelTest
from store.tests.test_models import BusinessUnitModelTest, WorkLocationModelTest
from job.tests.test_models import JobModelTest
from django.utils.crypto import get_random_string as grs


class OperatorModelTest(TestCase):

    def create_operator(self, PW_ACS_OPR="password", NM_USR="username"):
        return Operator.objects.create(PW_ACS_OPR=PW_ACS_OPR, NM_USR=NM_USR)

    def test_create_operator(self):
        w = self.create_operator()
        self.assertTrue(isinstance(w, Operator))
        self.assertEqual(w.__unicode__(), w.NM_USR)


class AccessPasswordModelTest(OperatorModelTest, TestCase):

    def create_acs_password(self, PS_ACS_OPR="password"):
        oprt_instance = OperatorModelTest.create_operator(self)
        return AccessPassword.objects.create(ID_OPR=oprt_instance, PS_ACS_OPR=PS_ACS_OPR, TS_EP=timezone.now())

    def test_acs_password(self):
        w = self.create_acs_password()
        self.assertTrue(isinstance(w, AccessPassword))
        self.assertEqual(w.__unicode__(), w.ID_OPR)


class OprBsnsUtAsgmtModelTest(OperatorModelTest, TestCase):

    def create_opr_bu_asgmt(self, NU_OPR=1):
        oprt_instance = OperatorModelTest.create_operator(self)
        bu_instance = BusinessUnitModelTest.create_business_unit(self)
        return OperatorBusinessUnitAssignment.objects.create(ID_OPR=oprt_instance, ID_BSN_UN=bu_instance, TS_EF=timezone.now(), TS_EP=timezone.now(), NU_OPR=NU_OPR)

    def test_opr_bu_asgmt(self):
        w = self.create_opr_bu_asgmt()
        self.assertTrue(isinstance(w, OperatorBusinessUnitAssignment))
        self.assertEqual(w.__unicode__(), w.ID_ASGMT_OPR_LCN)


class WrkrOprAsgmtModelTest(OperatorModelTest, TestCase):

    def create_wrkr_opr_asgmt(self):
        oprt_instance = OperatorModelTest.create_operator(self)
        wrkr_instance = WorkerModelTest.create_worker(self)
        return WorkerOperatorAssignment.objects.create(ID_OPR=oprt_instance, ID_WRKR=wrkr_instance, TS_EF=timezone.now(), TS_EP=timezone.now())

    def test_wrkr_opr_asgmt(self):
        w = self.create_wrkr_opr_asgmt()
        self.assertTrue(isinstance(w, WorkerOperatorAssignment))
        self.assertEqual(w.__unicode__(), w.ID_ASGMT_WRKR_OPR)


class WorkGroupModelTest(TestCase):

    def create_work_group(self, DE_GP_WRK="Work Group Description"):
        return WorkGroup.objects.create(DE_GP_WRK=DE_GP_WRK)

    def test_work_group(self):
        w = self.create_work_group()
        self.assertTrue(isinstance(w, WorkGroup))
        self.assertEqual(w.__unicode__(), w.DE_GP_WRK)


class OperatorGroupModelTest(OperatorModelTest, WorkGroupModelTest, TestCase):

    def create_operator_group(self):
        opr_instance = OperatorGroupModelTest.create_operator(self)
        wrk_grp_instance = WorkGroupModelTest.create_work_group(self)
        return OperatorGroup.objects.create(ID_GP_WRK=wrk_grp_instance, ID_OPR=opr_instance)

    def test_operator_group(self):
        w = self.create_operator_group()
        self.assertTrue(isinstance(w, OperatorGroup))
        self.assertEqual(w.__unicode__(), w.ID_GP_OPR)


class ResourceModelTest(TestCase):

    def create_resource(self, DE_RS="Resource Description"):
        return Resource.objects.create(DE_RS=DE_RS)

    def test_create_resource(self):
        w = self.create_resource()
        self.assertTrue(isinstance(w, Resource))
        self.assertEqual(w.__str__(), w.DE_RS)


class GroupResourceAccessModelTest(WorkGroupModelTest, ResourceModelTest, TestCase):

    def create_gp_rs_acs(self):
        wrk_gp = WorkGroupModelTest.create_work_group(self)
        resource = ResourceModelTest.create_resource(self)
        return GroupResourceAccess.objects.create(ID_GP_WRK=wrk_gp, ID_RS=resource)

    def test_create_gp_rs_acs(self):
        w = self.create_gp_rs_acs()
        self.assertTrue(isinstance(w, GroupResourceAccess))
        self.assertEqual(w.__unicode__(), w.ID_ACS_GP_RS)


class OperatorResourceAccessModelTest(OperatorModelTest, ResourceModelTest, TestCase):

    def create_opr_rs_acs(self):
        resource = ResourceModelTest.create_resource(self)
        operator = OperatorModelTest.create_operator(self)
        return OperatorResourceAccess.objects.create(ID_RS=resource, ID_OPR=operator)

    def test_create_opr_rs_acs(self):
        w = self.create_opr_rs_acs()
        self.assertTrue(isinstance(w, OperatorResourceAccess))
        self.assertEqual(w.__unicode__(), w.ID_ACS_OPR_RS)


class TaskSetModelTest(TestCase):

    def create_taskset(self, NM_ST_TSK="Task Set Name"):
        return TaskSet.objects.create(NM_ST_TSK=NM_ST_TSK)

    def test_create_taskset(self):
        w = self.create_taskset()
        self.assertTrue(isinstance(w, TaskSet))
        self.assertEqual(w.__unicode__(), w.ID_ST_TSK)


class TaskModelTest(TaskSetModelTest, TestCase):

    def create_task(self, NM_TSK="Task Name", DE_TSK="Task Description"):
        task_set = TaskSetModelTest.create_taskset(self)
        return Task.objects.create(ID_ST_TSK=task_set, NM_TSK=NM_TSK, DE_TSK=DE_TSK)

    def test_create_task(self):
        w = self.create_task()
        self.assertTrue(isinstance(w, Task))
        self.assertEqual(w.__unicode__(), w.ID_TSK)


class JobTaskSetModelTest(TaskSetModelTest, TestCase):

    def create_job_task_set(self):
        task_set = TaskSetModelTest.create_taskset(self)
        job = JobModelTest.create_job(self)
        return JobTaskSet.objects.create(ID_ST_TSK=task_set, ID_JOB=job)

    def test_create_job_task_set(self):
        w = self.create_job_task_set()
        self.assertTrue(isinstance(w, JobTaskSet))
        self.assertEqual(w.__unicode__(), w.ID_JOB_ST_TSK)


class TaskResourceAccessModelTest(TestCase):
    def create_task_resource_access(self):
        ID_TSK = TaskModelTest.create_task(self)
        ID_RS = ResourceModelTest.create_resource(self)
        return TaskResourceAccess.objects.create(ID_TSK=ID_TSK, ID_RS=ID_RS)

    def test_task_resource_access(self):
        w = self.create_task_resource_access()
        self.assertTrue(isinstance(w, TaskResourceAccess))
        self.assertEqual(w.__unicode__(), w.ID_ACS_TSK_RS)


class WorkstationGroupModelTest(TestCase):
    def create_workstation_group(self):
        NM_WSGP = grs(200)
        return WorkstationGroup.objects.create(NM_WSGP=NM_WSGP)

    def test_workstation_group(self):
        w = self.create_workstation_group()
        self.assertTrue(isinstance(w, WorkstationGroup))

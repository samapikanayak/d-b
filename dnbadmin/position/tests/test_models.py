'''Position model Testing'''
from django.test import TestCase
from position.models import *
from django.utils import timezone
from worker.tests.test_models import WorkerModelTest
from job.tests.test_models import JobModelTest
from store.tests.test_models import WorkLocationModelTest




# models test
class PositionModelTest(TestCase):
    '''Position Model Test'''

    def create_position(self, NM_TTL = "CEO"):
        '''position create'''
        work_loc_instance = WorkLocationModelTest.create_work_location(self)
        job_instance = JobModelTest.create_job(self)
        return Position.objects.create(ID_LCN = work_loc_instance, ID_JOB = job_instance, NM_TTL = NM_TTL)

    def test_create_position(self):
        '''position create test'''
        w = self.create_position()
        self.assertTrue(isinstance(w, Position))
        self.assertEqual(w.__unicode__(), w.NM_TTL)



class PositionWorkScheduleModelTest(PositionModelTest, TestCase):
    '''position work schedule test'''
    def create_position_schedule(self):
        '''position work schedule create'''
        position_instance = PositionModelTest.create_position(self)
        return PositionWorkSchedule.objects.create(ID_PST = position_instance)

    def test_create_position_schedule(self):
        '''position work schedule test'''
        w = self.create_position_schedule()
        self.assertTrue(isinstance(w, PositionWorkSchedule))
        self.assertEqual(w.__unicode__(), w.ID_PST_WRK_SCH)


class PositionHierarchyModelTest(PositionModelTest, TestCase):
    '''position hierarchy test'''
    def create_position_hrchy(self):
        '''position hierarchy create'''
        position_instance = PositionModelTest.create_position(self)
        return PositionHierarchy.objects.create(ID_PST_SUB = position_instance, ID_PST_SPVR = position_instance, DC_EF = timezone.now(), DC_EX = timezone.now())

    def test_create_position_hrchy(self):
        '''position hierarchy test'''
        w = self.create_position_hrchy()
        self.assertTrue(isinstance(w, PositionHierarchy))
        self.assertEqual(w.__unicode__(), w.ID_HRC_PST)


class WorkerPsnAsgmtModelTest(PositionModelTest, TestCase):
    '''worker position assignment test'''
    def create_wrk_psn_asgmt(self, NM_TTL = "Title"):
        '''worker position assignment create'''
        position_instance = PositionModelTest.create_position(self)
        wrkr_instance = WorkerModelTest.create_worker(self)
        return WorkerPositionAssignment.objects.create(ID_PST = position_instance, ID_WRKR = wrkr_instance, DC_EF = timezone.now(), DC_EP = timezone.now(), NM_TTL = NM_TTL)

    def test_wrk_psn_asgmt(self):
        '''worker position assignment test'''
        w = self.create_wrk_psn_asgmt()
        self.assertTrue(isinstance(w, WorkerPositionAssignment))
        self.assertEqual(w.__unicode__(), w.ID_ASGMT_WRKR_PSN)
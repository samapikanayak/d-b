from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from workerschedule.models import *
from worker.tests.test_models import WorkerModelTest
from store.tests.test_models import WorkLocationModelTest
from unitofmeasure.tests.test_models import UnitOfMeasureModelTest



class TimeGroupModelTest(TestCase):

    def create_time_group(self, DE_GP_TM = "Time Group Description"):
        return TimeGroup.objects.create(DE_GP_TM = DE_GP_TM)

    def test_create_time_group(self):
        w = self.create_time_group()
        self.assertTrue(isinstance(w, TimeGroup))
        self.assertEqual(w.__unicode__(), w.ID_GP_TM)


class WorkerAvlbModelTest(TimeGroupModelTest, TestCase):

    def create_time_group(self, DE_GP_TM = "Time Group Description"):
        wrkr_instance = WorkerModelTest.create_worker(self)
        time_grp_instance = TimeGroupModelTest.create_time_group(self)
        wrk_loc_instance = WorkLocationModelTest.create_work_location(self)
        return WorkerAvailability.objects.create(ID_WRKR = wrkr_instance, ID_GP_TM = time_grp_instance, ID_LCN = wrk_loc_instance, DC_EF = timezone.now(), DC_EP = timezone.now())

    def test_create_time_group(self):
        w = self.create_time_group()
        self.assertTrue(isinstance(w, WorkerAvailability))
        self.assertEqual(w.__unicode__(), w.ID_WRKR_AVLB)


class TimePeriodModelTest(TestCase):

    def create_time_period(self, NM_PD_TM = "Time Period Name", WD = "M", SI_DRN = 14):
        unit_msr_instance = UnitOfMeasureModelTest.create_unit_measure(self)
        return TimePeriod.objects.create(NM_PD_TM = NM_PD_TM, WD = WD, TM_SRT = timezone.now().time(), LU_UOM_DRN = unit_msr_instance, SI_DRN = SI_DRN)

    def test_create_time_period(self):
        w = self.create_time_period()
        self.assertTrue(isinstance(w, TimePeriod))
        self.assertEqual(w.__unicode__(), w.ID_PD_TM)



class TimeGroupTimePeriodModelTest(TimeGroupModelTest, TimePeriodModelTest, TestCase):

    def create_tmgp_tmpd(self):
        tmgp_instance = TimeGroupModelTest.create_time_group(self)
        tmpd_instance = TimePeriodModelTest.create_time_period(self)
        return TimeGroupTimePeriod.objects.create(ID_PD_TM = tmpd_instance, ID_GP_TM = tmgp_instance)

    def test_create_tmgp_tmpd(self):
        w = self.create_tmgp_tmpd()
        self.assertTrue(isinstance(w, TimeGroupTimePeriod))
        self.assertEqual(w.__unicode__(), w.ID_GP_PD_TM)

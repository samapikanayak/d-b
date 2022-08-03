from datetime import datetime
from django.test import TestCase
from job.models import *
from django.utils import timezone


class JobModelTest(TestCase):

    def create_job(self, NM_JOB="Manager"):
        return Job.objects.create(NM_JOB = NM_JOB)

    def test_create_job(self):
        w = self.create_job()
        self.assertTrue(isinstance(w, Job))
        self.assertEqual(w.__unicode__(), w.NM_JOB)

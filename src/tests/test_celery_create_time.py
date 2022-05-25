from django.test import TestCase
from django.conf import settings
from django_celery_beat.models import IntervalSchedule
from src.base.celery_create_time import create_interval_schedule


class TestCeleryCreate(TestCase):
    def test_create_interval_schedule(self):
        self.assertEqual(0, IntervalSchedule.objects.count())
        create_interval_schedule()
        self.assertEqual(4, IntervalSchedule.objects.count())

        time_list = settings.TIME_LIST

        for item, schedule in enumerate(IntervalSchedule.objects.all()):
            self.assertEqual(schedule.period, IntervalSchedule.HOURS)
            self.assertEqual(schedule.every, time_list[item])

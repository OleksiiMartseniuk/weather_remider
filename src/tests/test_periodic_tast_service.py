from rest_framework.test import APITestCase

from src.weather.service.periodic_tast_service import ServiceTasks

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.conf import settings

import random
import json


def create_interval_schedule():
    """ Создания Интервального расписания"""
    for time in settings.TIME_LIST:
        IntervalSchedule.objects.get_or_create(
            every=time,
            period=IntervalSchedule.HOURS,
        )


class TestServiceTasks(APITestCase):
    def setUp(self):
        create_interval_schedule()
        self.service_task = ServiceTasks()

    def test_get_schedule(self):
        for time in settings.TIME_LIST:
            self.assertTrue(IntervalSchedule, self.service_task.get_schedule(time))

    def test_create(self):
        self.assertEqual(0, PeriodicTask.objects.count())
        time = random.choice(settings.TIME_LIST)
        task = self.service_task.create(time, 'test', 1, 'test@test.com')
        self.assertEqual(1, PeriodicTask.objects.count())

        self.assertEqual(IntervalSchedule.objects.get(every=time), task.interval)
        self.assertEqual('test', task.name)
        self.assertEqual('src.weather.tasks.sent_weather_email', task.task)
        self.assertEqual(json.dumps([1, 'test@test.com']), task.args)

    def test_update(self):
        task = self.service_task.create(1, 'test', 1, 'test@test.com')
        self.assertEqual(1, PeriodicTask.objects.count())
        self.assertEqual(IntervalSchedule.objects.get(every=1), task.interval)

        self.service_task.update(3, task)
        self.assertEqual(IntervalSchedule.objects.get(every=3), task.interval)

from django_celery_beat.models import IntervalSchedule
from django.conf import settings


def create_interval_schedule():
    """ Создания Интервального расписания"""
    for time in settings.TIME_LIST:
        IntervalSchedule.objects.get_or_create(
            every=time,
            period=IntervalSchedule.HOURS,
        )

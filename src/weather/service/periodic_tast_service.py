from django_celery_beat.models import PeriodicTask, IntervalSchedule


class ServiceTasks:
    def get_schedule(self, time: int):
        return IntervalSchedule.objects.filter(every=time, period=IntervalSchedule.HOURS)[0]

    def create(self, time: int, name: str):
        schedule = self.get_schedule(time)
        PeriodicTask.objects.create(
            interval=schedule,
            name=name,
            task='src.weather.tasks.sent_weather_email'
        )

    def update(self, time: int, task: PeriodicTask):
        schedule = self.get_schedule(time)
        task.interval = schedule
        task.save()

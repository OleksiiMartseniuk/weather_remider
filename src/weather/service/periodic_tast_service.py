from django_celery_beat.models import PeriodicTask, IntervalSchedule


class ServiceTasks:
    def get_schedule(self, time: int) -> None:
        return IntervalSchedule.objects.filter(every=time, period=IntervalSchedule.HOURS)[0]

    def create(self, time: int, name: str, city_id: int) -> PeriodicTask:
        schedule = self.get_schedule(time)
        task = PeriodicTask.objects.create(
            interval=schedule,
            name=name,
            task='src.weather.tasks.sent_weather_email'
        )
        return task

    def update(self, time: int, task: PeriodicTask) -> None:
        schedule = self.get_schedule(time)
        task.interval = schedule
        task.save()


service_task = ServiceTasks()
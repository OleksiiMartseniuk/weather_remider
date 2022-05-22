from django_celery_beat.models import PeriodicTask, IntervalSchedule


class ServiceTasks:
    def get_schedule(self, time: int) -> IntervalSchedule:
        """ Интервальное расписание """
        return IntervalSchedule.objects.filter(every=time, period=IntervalSchedule.HOURS)[0]

    def create(self, time: int, name: str, city_id: int, owner_email: str) -> PeriodicTask:
        """ Создания Периодической задачи"""
        schedule = self.get_schedule(time)
        task = PeriodicTask.objects.create(
            interval=schedule,
            name=name,
            task='src.weather.tasks.sent_weather_email'
        )
        return task

    def update(self, time: int, task: PeriodicTask) -> None:
        """ Обновления Периодической задачи"""
        schedule = self.get_schedule(time)
        task.interval = schedule
        task.save()


service_task = ServiceTasks()

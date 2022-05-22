from django.db import models
from django.conf import settings
from django_celery_beat.models import PeriodicTask


class City(models.Model):
    """ Город """
    id_city = models.IntegerField('Идентификатор города')
    name = models.CharField('Название города', max_length=20, unique=True)
    timezone = models.IntegerField('Сдвиг в секундах от UTC')
    coord_lon = models.FloatField('Географическое положение города, долгота')
    coord_lat = models.FloatField('Географическое положение города, широта')
    weather_id = models.IntegerField('Идентификатор погодных условий')
    weather_main = models.CharField('Группа погодных параметров', max_length=50)
    weather_description = models.CharField('Погодные условия в группе', max_length=255)
    weather_icon = models.CharField('Идентификатор значка погоды', max_length=20)
    base = models.CharField('Внутренний параметр', max_length=50)
    main_temp = models.FloatField('Температура')
    main_feels_like = models.FloatField('Человеческое восприятие температуры ')
    main_temp_min = models.FloatField('Минимальная температура на данный момент')
    main_temp_max = models.FloatField('Максимальная температура на данный момент')
    main_pressure = models.IntegerField('Атмосферное давление гПа')
    main_humidity = models.IntegerField('Влажность, %')
    visibility = models.IntegerField('Видимость, метр. Максимальное значение видимости 10км')
    wind_speed = models.FloatField('Скорость ветра метр/сек')
    wind_deg = models.FloatField('Направление ветра, градусы')
    wind_gust = models.FloatField('Порыв ветра. метр/сек', blank=True, null=True)
    clouds_all = models.IntegerField('Облачность, %')
    dt = models.IntegerField('Время расчета данных, unix, UTC')
    sys_country = models.CharField('Код страны', max_length=10)
    sys_sunrise = models.IntegerField('Время восхода солнца, unix, UTC')
    sys_sunset = models.IntegerField('Время заката, unix, UTC')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SubscriptionCity(models.Model):
    """ Подписка на город """
    PERIODICITY_SEND_EMAIL_CHOICES = [
        ('1', '1 hours'),
        ('3', '3 hours'),
        ('6', '6 hours'),
        ('12', '12 hours'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription_city'
    )
    periodicity_send_email = models.CharField(
        'Периодичность отправить письмо',
        max_length=2,
        choices=PERIODICITY_SEND_EMAIL_CHOICES,
        default='6'
    )
    periodic_task = models.ForeignKey(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        unique_together = ['owner', 'city']

    def __str__(self):
        return f'{self.owner.username} subscription {self.city.name}'

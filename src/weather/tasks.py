from celery import shared_task
from time import sleep
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from src.weather.models import City
from src.base.openweathermaplib import OpenWeatherMapClient


@shared_task
def update_city_data():
    """ Обновления данных всех городов """
    client = OpenWeatherMapClient()

    for position, city in enumerate(City.objects.all(), 1):
        if not position % 60:
            sleep(60)

        data_city = client.get_weather(city_name=city.name)
        if 'Error' in data_city:
            raise ValueError(data_city['Error'])
        else:
            city.timezone = data_city['timezone']
            city.coord_lon = data_city['coord']['lon']
            city.coord_lat = data_city['coord']['lat']
            city.weather_id = data_city['weather'][0]['id']
            city.weather_main = data_city['weather'][0]['main']
            city.weather_description = data_city['weather'][0]['description']
            city.weather_icon = data_city['weather'][0]['icon']
            city.base = data_city['base']
            city.main_temp = data_city['main']['temp']
            city.main_feels_like = data_city['main']['feels_like']
            city.main_temp_min = data_city['main']['temp_min']
            city.main_temp_max = data_city['main']['temp_max']
            city.main_pressure = data_city['main']['pressure']
            city.main_humidity = data_city['main']['humidity']
            city.visibility = data_city['visibility']
            city.wind_speed = data_city['wind']['speed']
            city.wind_deg = data_city['wind']['deg']
            city.wind_gust = data_city['wind'].get('gust')
            city.clouds_all = data_city['clouds']['all']
            city.dt = data_city['dt']
            city.sys_country = data_city['sys']['country']
            city.sys_sunrise = data_city['sys']['sunrise']
            city.sys_sunset = data_city['sys']['sunset']
            city.save()


@shared_task
def sent_weather_email(city_id: int, owner_email: str):
    """ Отправка email пользователю """
    city = City.objects.get(id=city_id)
    message = render_to_string('weather/weather_email.html', {'city': city})
    send_mail(
        subject='Weather',
        html_message=message,
        message=f'Weather in {city.name}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[owner_email]
    )

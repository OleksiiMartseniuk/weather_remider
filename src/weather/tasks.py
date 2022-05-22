from celery import shared_task
from time import sleep
from src.weather.models import City
from src.base.openweathermaplib import OpenWeatherMapClient


@shared_task
def update_city_data():
    client = OpenWeatherMapClient()

    for position, city in enumerate(City.objects.all(), 1):
        print(city)
        if not position % 60:
            sleep(60)

        data_city = client.get_weather(city_name=city.name)

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

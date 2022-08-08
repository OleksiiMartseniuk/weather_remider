import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.test import APITestCase
from unittest import mock

from django.contrib.auth import get_user_model
from django.urls import reverse

from src.tests.test_base import conf_json
from src.weather.models import City, SubscriptionCity

User = get_user_model()


class TestWeather(APITestCase):
    def create_user(self):
        return User.objects.create_user(
            username='test',
            password='password',
            email='test@test.com'
        )

    def authenticate(self, username, password) -> None:
        response = self.client.post(
            '/api/token/',
            data={'username': username, 'password': password}
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access']
        )

    def create_city(self) -> City:
        return City.objects.create(
            id_city=conf_json.london_data['id'],
            name=conf_json.london_data['name'],
            timezone=conf_json.london_data['timezone'],
            coord_lon=conf_json.london_data['coord']['lon'],
            coord_lat=conf_json.london_data['coord']['lat'],
            weather_id=conf_json.london_data['weather'][0]['id'],
            weather_main=conf_json.london_data['weather'][0]['main'],
            weather_description=conf_json.london_data['weather'][0]['description'],
            weather_icon=conf_json.london_data['weather'][0]['icon'],
            base=conf_json.london_data['base'],
            main_temp=conf_json.london_data['main']['temp'],
            main_feels_like=conf_json.london_data['main']['feels_like'],
            main_temp_min=conf_json.london_data['main']['temp_min'],
            main_temp_max=conf_json.london_data['main']['temp_max'],
            main_pressure=conf_json.london_data['main']['pressure'],
            main_humidity=conf_json.london_data['main']['humidity'],
            visibility=conf_json.london_data['visibility'],
            wind_speed=conf_json.london_data['wind']['speed'],
            wind_deg=conf_json.london_data['wind']['deg'],
            wind_gust=conf_json.london_data['wind'].get('gust'),
            clouds_all=conf_json.london_data['clouds']['all'],
            dt=conf_json.london_data['dt'],
            sys_country=conf_json.london_data['sys']['country'],
            sys_sunrise=conf_json.london_data['sys']['sunrise'],
            sys_sunset=conf_json.london_data['sys']['sunset'],
        )

    def test_city_get(self):
        city = self.create_city()
        self.create_user()
        self.authenticate('test', 'password')
        url = reverse('city-ditail', args=[city.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(city.id_city, response.data['id_city'])
        self.assertEqual(city.name, response.data['name'])
        self.assertEqual(city.timezone, response.data['timezone'])
        self.assertEqual(city.coord_lon, response.data['coord_lon'])
        self.assertEqual(city.coord_lat, response.data['coord_lat'])
        self.assertEqual(city.weather_id, response.data['weather_id'])
        self.assertEqual(city.weather_main, response.data['weather_main'])
        self.assertEqual(
            city.weather_description,
            response.data['weather_description']
        )
        self.assertEqual(city.weather_icon, response.data['weather_icon'])
        self.assertEqual(city.base, response.data['base'])
        self.assertEqual(city.main_temp, response.data['main_temp'])
        self.assertEqual(city.main_feels_like, response.data['main_feels_like'])
        self.assertEqual(city.main_temp_min, response.data['main_temp_min'])
        self.assertEqual(city.main_temp_max, response.data['main_temp_max'])
        self.assertEqual(city.main_pressure, response.data['main_pressure'])
        self.assertEqual(city.main_humidity, response.data['main_humidity'])
        self.assertEqual(city.visibility, response.data['visibility'])
        self.assertEqual(city.wind_speed, response.data['wind_speed'])
        self.assertEqual(city.wind_deg, response.data['wind_deg'])
        self.assertEqual(city.wind_gust, response.data['wind_gust'])
        self.assertEqual(city.clouds_all, response.data['clouds_all'])
        self.assertEqual(city.dt, response.data['dt'])
        self.assertEqual(city.sys_country, response.data['sys_country'])
        self.assertEqual(city.sys_sunrise, response.data['sys_sunrise'])
        self.assertEqual(city.sys_sunset, response.data['sys_sunset'])
        self.client.credentials()

    @mock.patch('src.weather.views.weather_s.search_city')
    def test_city_create(self, mock_search_city):
        mock_search_city.return_value = 1
        self.create_user()
        self.authenticate('test', 'password')
        self.assertEqual(0, City.objects.count())
        url = reverse('city-search')
        response = self.client.post(url, data={'name': 'London'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json(), {'name': 'London', 'id': 1})
        self.client.credentials()

    def test_subscription_retrieve(self):
        user = self.create_user()
        schedule = IntervalSchedule.objects.create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        city = self.create_city()
        task = PeriodicTask.objects.create(
            interval=schedule,
            name='test',
            task='src.weather.tasks.sent_weather_email',
            args=json.dumps([1, user.email])
        )
        sub_city = SubscriptionCity.objects.create(
            owner=user,
            periodicity_send_email='1',
            periodic_task=task,
            city=city
        )
        self.authenticate('test', 'password')

        url = reverse('subscription-retrieve', args=[sub_city.id])
        response = self.client.get(url)
        self.assertEqual('1', response.data['periodicity_send_email'])
        self.assertEqual(city.name, response.data['city'])
        self.assertEqual(200, response.status_code)
        self.client.credentials()

    def test_subscription_update(self):
        user = self.create_user()
        schedule = IntervalSchedule.objects.create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        IntervalSchedule.objects.create(
            every=3,
            period=IntervalSchedule.HOURS,
        )
        city = self.create_city()
        task = PeriodicTask.objects.create(
            interval=schedule,
            name='test',
            task='src.weather.tasks.sent_weather_email',
            args=json.dumps([1, user.email])
        )
        sub_city = SubscriptionCity.objects.create(
            owner=user,
            periodicity_send_email='1',
            periodic_task=task,
            city=city
        )
        self.authenticate('test', 'password')

        self.assertEqual(sub_city.periodicity_send_email, '1')
        url = reverse('subscription-update', args=[sub_city.id])
        data = {'periodicity_send_email': '3'}
        response = self.client.put(url, data=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('3', response.data['periodicity_send_email'])
        sub_city = SubscriptionCity.objects.get(id=sub_city.id)
        self.assertEqual(sub_city.periodicity_send_email, '3')
        self.client.credentials()

    def test_subscription_destroy(self):
        user = self.create_user()
        schedule = IntervalSchedule.objects.create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        city = self.create_city()
        task = PeriodicTask.objects.create(
            interval=schedule,
            name='test',
            task='src.weather.tasks.sent_weather_email',
            args=json.dumps([1, user.email])
        )
        sub_city = SubscriptionCity.objects.create(
            owner=user,
            periodicity_send_email='1',
            periodic_task=task,
            city=city
        )
        self.authenticate('test', 'password')

        self.assertEqual(1, PeriodicTask.objects.count())
        self.assertEqual(1, SubscriptionCity.objects.count())
        url = reverse('subscription-destroy', args=[sub_city.id])
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, PeriodicTask.objects.count())
        self.assertEqual(0, SubscriptionCity.objects.count())
        self.client.credentials()

    def test_subscription_list(self):
        user = self.create_user()
        schedule = IntervalSchedule.objects.create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        city = self.create_city()
        task = PeriodicTask.objects.create(
            interval=schedule,
            name='test',
            task='src.weather.tasks.sent_weather_email',
            args=json.dumps([user.id, user.email])
        )
        SubscriptionCity.objects.create(
            owner=user,
            periodicity_send_email='1',
            periodic_task=task,
            city=city
        )

        self.authenticate('test', 'password')
        url = reverse('subscription-list')
        response = self.client.get(url)
        self.assertEqual(1, len(response.data))
        self.client.credentials()

    def test_subscription_create(self):
        self.create_user()
        self.authenticate('test', 'password')
        IntervalSchedule.objects.create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        city = self.create_city()

        self.assertEqual(0, PeriodicTask.objects.count())
        self.assertEqual(0, SubscriptionCity.objects.count())

        url = reverse('subscription-create')
        data = {'periodicity_send_email': '1', 'city': city.id}
        response = self.client.post(url, data=data)

        self.assertEqual(201, response.status_code)
        self.assertEqual('1', response.data['periodicity_send_email'])
        self.assertEqual(city.id, response.data['city'])
        self.assertEqual(1, PeriodicTask.objects.count())
        self.assertEqual(1, SubscriptionCity.objects.count())
        self.client.credentials()

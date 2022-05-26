import json

from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from src.weather.models import SubscriptionCity, City
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from src.tests.test_base import conf_json

User = get_user_model()


class TestAccount(APITestCase):
    def authenticate(self, username, password):
        response = self.client.post('/api/token/', data={'username': username, 'password': password})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_create(self):
        self.assertEqual(0, User.objects.count())
        data = {
            'username': 'test1',
            'password': 'test1test1',
            'email': 'test@test.com'
        }
        response = self.client.post('/api/account/create/', data=data)
        self.assertEqual(1, User.objects.count())
        user = User.objects.get(username='test1')
        self.assertEqual(user.username, response.data['username'])
        self.assertEqual(user.email, response.data['email'])

    def test_get(self):
        user = User.objects.create_user(
            username='test',
            password='password',
            email='test@test.com'
        )
        self.assertEqual(1, User.objects.count())
        self.authenticate('test', 'password')
        response = self.client.get('/api/account/me/')
        self.assertEqual(user.username, response.data['username'])
        self.assertEqual(user.email, response.data['email'])
        self.client.credentials()

    def test_update(self):
        User.objects.create_user(
            username='test',
            password='password',
            email='test@test.com'
        )
        data = {
            'username': 'test2',
            'email': 'test1@test.com'
        }
        self.authenticate('test', 'password')
        response = self.client.put('/api/account/update/', data=data)
        user = User.objects.get(username='test2')
        self.assertEqual(user.username, response.data['username'])
        self.assertEqual(user.email, response.data['email'])
        self.client.credentials()

    def test_delete(self):
        user = User.objects.create_user(
            username='test',
            password='password',
            email='test@test.com'
        )
        schedule = IntervalSchedule.objects.create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        city = City.objects.create(
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
        task = PeriodicTask.objects.create(
            interval=schedule,
            name='test',
            task='src.weather.tasks.sent_weather_email',
            args=json.dumps([1, user.email])
        )
        SubscriptionCity.objects.create(
            owner=user,
            periodicity_send_email='1',
            periodic_task=task,
            city=city
        )
        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, PeriodicTask.objects.count())
        self.assertEqual(1, SubscriptionCity.objects.count())

        self.authenticate('test', 'password')
        response = self.client.delete('/api/account/delete/')
        self.assertEqual(204, response.status_code)

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, PeriodicTask.objects.count())
        self.assertEqual(0, SubscriptionCity.objects.count())

from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError

from src.weather.service.write_db import WriteDB
from src.weather.models import City
from src.tests.test_api import conf_json


class TestWriteDB(APITestCase):
    def setUp(self):
        self.writer = WriteDB()

    def test_create_city(self):
        self.assertEqual(0, City.objects.count())
        self.writer.create_city(conf_json.london_data)
        self.assertEqual(1, City.objects.count())

        city = City.objects.get(id=1)

        self.assertEqual(city.id_city, conf_json.london_data['id'])
        self.assertEqual(city.name, conf_json.london_data['name'])
        self.assertEqual(city.timezone, conf_json.london_data['timezone'])
        self.assertEqual(city.coord_lon, conf_json.london_data['coord']['lon'])
        self.assertEqual(city.coord_lat, conf_json.london_data['coord']['lat'])
        self.assertEqual(city.weather_id, conf_json.london_data['weather'][0]['id'])
        self.assertEqual(city.weather_main, conf_json.london_data['weather'][0]['main'])
        self.assertEqual(city.weather_description, conf_json.london_data['weather'][0]['description'])
        self.assertEqual(city.weather_icon, conf_json.london_data['weather'][0]['icon'])
        self.assertEqual(city.base, conf_json.london_data['base'])
        self.assertEqual(city.main_temp, conf_json.london_data['main']['temp'])
        self.assertEqual(city.main_feels_like, conf_json.london_data['main']['feels_like'])
        self.assertEqual(city.main_temp_min, conf_json.london_data['main']['temp_min'])
        self.assertEqual(city.main_temp_max, conf_json.london_data['main']['temp_max'])
        self.assertEqual(city.main_pressure, conf_json.london_data['main']['pressure'])
        self.assertEqual(city.main_humidity, conf_json.london_data['main']['humidity'])
        self.assertEqual(city.visibility, conf_json.london_data['visibility'])
        self.assertEqual(city.wind_speed, conf_json.london_data['wind']['speed'])
        self.assertEqual(city.wind_deg, conf_json.london_data['wind']['deg'])
        self.assertEqual(city.wind_gust, conf_json.london_data['wind'].get('gust'))
        self.assertEqual(city.clouds_all, conf_json.london_data['clouds']['all'])
        self.assertEqual(city.dt, conf_json.london_data['dt'])
        self.assertEqual(city.sys_country, conf_json.london_data['sys']['country'])
        self.assertEqual(city.sys_sunrise, conf_json.london_data['sys']['sunrise'])
        self.assertEqual(city.sys_sunset, conf_json.london_data['sys']['sunset'])

    def test_create_city_check_error(self):
        self.assertEqual(0, City.objects.count())

        with self.assertRaises(ValidationError) as cm:
            self.writer.create_city(conf_json.error_data_message)

        self.assertTrue(conf_json.error_data_message['Error'] in str(cm.exception))
        self.assertEqual(0, City.objects.count())

    def test_create_city_exists(self):
        self.assertEqual(0, City.objects.count())
        self.writer.create_city(conf_json.london_data)
        self.assertEqual(1, City.objects.count())

        with self.assertRaises(ValidationError) as cm:
            self.writer.create_city(conf_json.london_data)

        self.assertTrue(conf_json.error_exists in str(cm.exception))

    def test_create_city_fake(self):
        self.assertEqual(0, City.objects.count())

        with self.assertRaises(ValidationError) as cm:
            self.writer.create_city({})

        self.assertTrue(conf_json.error_fake in str(cm.exception))
        self.assertEqual(0, City.objects.count())

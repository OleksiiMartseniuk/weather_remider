import unittest
import responses
from responses import matchers
from src.base.openweathermaplib import OpenWeatherMapClient

from src.tests.test_base import conf_json


class TestOpenWeatherMapClient(unittest.TestCase):
    def setUp(self):
        self.client = OpenWeatherMapClient()

    @responses.activate
    def test_get_weather(self):
        responses.add(
            responses.GET,
            'https://api.openweathermap.org/data/2.5/weather',
            match=[matchers.query_param_matcher(conf_json.params_london)],
            status=200,
            json=conf_json.london_data
        )
        res = self.client.get_weather('London')
        self.assertEqual(res, conf_json.london_data)

    @responses.activate
    def test_error_get_weather(self):
        responses.add(
            responses.GET,
            'https://api.openweathermap.org/data/2.5/weather',
            match=[matchers.query_param_matcher(conf_json.params_london)],
            status=300,
            json=conf_json.error_message
        )
        res = self.client.get_weather('London')
        self.assertEqual(res, {'Error': conf_json.error_message['message']})

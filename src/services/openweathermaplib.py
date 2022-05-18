import requests
from django.conf import settings


class OpenWeatherMapClient:
    def __init__(self, api_keys: str = settings.SECRET_KEY_OPEN_WEATHER_MAP,
                 url: str = 'https://api.openweathermap.org/data/2.5/weather') -> None:
        self.__api_keys = api_keys
        self.url = url

    def _get(self, req_dict) -> dict:
        response = requests.post(url=self.url, params=req_dict)
        if response.status_code == 200:
            return response.json()
        return {'Error': response.json()['message']}

    def get_weather(self, city_name: str,
                    units: str = 'metric', lang: str = 'ru') -> dict:
        data = {
            'q': city_name,
            'appid': self.__api_keys,
            'units': units,
            'lang': lang,
        }
        return self._get(data)

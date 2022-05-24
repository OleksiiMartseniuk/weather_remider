from django.conf import settings


london_data = {
    'coord': {
        'lon': -0.1257,
        'lat': 51.5085
    },
    'weather': [
        {
            'id': 803,
            'main': "Clouds",
            'description': "broken clouds",
            'icon': "04d"
        }
    ],
    'base': "stations",
    'main': {
        'temp': 288.2,
        'feels_like': 287.59,
        'temp_min': 284.74,
        'temp_max': 290.45,
        'pressure': 1009,
        'humidity': 70
    },
    'visibility': 10000,
    'wind': {
        'speed': 2.57,
        'deg': 0,
        'gust': 8.23
    },
    'clouds': {
        'all': 75
    },
    'dt': 1653415616,
    'sys': {
        'type': 2,
        'id': 2019646,
        'country': "GB",
        'sunrise': 1653364625,
        'sunset': 1653422274
    },
    'timezone': 3600,
    'id': 2643743,
    'name': "London",
    'cod': 200
}

params_london = {
    'q': 'London',
    'appid': settings.SECRET_KEY_OPEN_WEATHER_MAP,
    'units': 'metric',
    'lang': 'ru',
}

error_message = {'message': 'Text message'}

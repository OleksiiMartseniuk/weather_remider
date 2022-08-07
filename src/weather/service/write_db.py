from rest_framework.exceptions import ValidationError

from src.weather.models import City


class WriteDB:
    def _check_error(self, data: dict) -> None:
        """ Проверка на ошибку данных api """
        if 'Error' in data:
            raise ValidationError(detail=data['Error'], code=400)

    def create_city(self, data: dict) -> int:
        """ Запись Города"""
        self._check_error(data)
        if City.objects.filter(id_city=data.get('id')).exists():
            city = City.objects.get(id_city=data.get('id'))
            return city.id

        try:
            city = City.objects.create(
                id_city=data['id'],
                name=data['name'].lower(),
                timezone=data['timezone'],
                coord_lon=data['coord']['lon'],
                coord_lat=data['coord']['lat'],
                weather_id=data['weather'][0]['id'],
                weather_main=data['weather'][0]['main'],
                weather_description=data['weather'][0]['description'],
                weather_icon=data['weather'][0]['icon'],
                base=data['base'],
                main_temp=data['main']['temp'],
                main_feels_like=data['main']['feels_like'],
                main_temp_min=data['main']['temp_min'],
                main_temp_max=data['main']['temp_max'],
                main_pressure=data['main']['pressure'],
                main_humidity=data['main']['humidity'],
                visibility=data['visibility'],
                wind_speed=data['wind']['speed'],
                wind_deg=data['wind']['deg'],
                wind_gust=data['wind'].get('gust'),
                clouds_all=data['clouds']['all'],
                dt=data['dt'],
                sys_country=data['sys']['country'],
                sys_sunrise=data['sys']['sunrise'],
                sys_sunset=data['sys']['sunset'],
            )
            return city.id
        except Exception:
            raise ValidationError(
                detail='Invalid data api OpenWeatherMapClient'
            )

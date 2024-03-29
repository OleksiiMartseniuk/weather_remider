from src.base.openweathermaplib import OpenWeatherMapClient
from src.weather.service.write_db import WriteDB
from src.weather.models import City


class WeatherService:
    writer = WriteDB()
    client = OpenWeatherMapClient()

    def create(self, city_name: str) -> int:
        """ Создать город """
        data_city = self.client.get_weather(city_name=city_name)
        return self.writer.create_city(data_city)

    def search_city(self, name: str) -> int:
        """Получения города"""
        if City.objects.filter(name=name.lower()).exists():
            city_id = City.objects.filter(name=name.lower()).\
                values_list('id', flat=True)
            return city_id[0]
        return self.create(name)


weather_s = WeatherService()

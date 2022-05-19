from src.base.openweathermaplib import OpenWeatherMapClient
from src.weather.service.write_db import WriteDB


class WeatherService:
    writer = WriteDB()
    client = OpenWeatherMapClient()

    def create(self, city_name: str) -> None:
        """ Создать город """
        data_city = self.client.get_weather(city_name=city_name)
        self.writer.create_city(data_city)


weather_s = WeatherService()

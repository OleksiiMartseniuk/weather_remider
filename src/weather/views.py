from rest_framework import viewsets

from src.weather import serializers
from src.weather.service.service import weather_s
from src.weather import models


class CityView(viewsets.ModelViewSet):
    """ Город """
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    lookup_field = 'name'

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CityCreateSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        weather_s.create(serializer.validated_data['name'])

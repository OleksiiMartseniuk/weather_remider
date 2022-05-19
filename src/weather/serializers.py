from rest_framework import serializers
from src.weather.models import City


class CityCreateSerializer(serializers.Serializer):
    """ Названия города """
    name = serializers.CharField(max_length=20)


class CitySerializer(serializers.ModelSerializer):
    """ Город """
    class Meta:
        model = City
        fields = '__all__'

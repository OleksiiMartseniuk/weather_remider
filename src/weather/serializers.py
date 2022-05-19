from rest_framework import serializers
from src.weather.models import City, SubscriptionCity


class CityCreateSerializer(serializers.Serializer):
    """ Названия города """
    name = serializers.CharField(max_length=20)


class CitySerializer(serializers.ModelSerializer):
    """ Город """
    class Meta:
        model = City
        fields = '__all__'


class SubscriptionCitySerializer(serializers.ModelSerializer):
    """ Подписка """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SubscriptionCity
        fields = '__all__'

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        weather_s.create(serializer.validated_data['name'])


class SubscriptionCityView(viewsets.ModelViewSet):
    """ Подписки """
    serializer_class = serializers.SubscriptionCitySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.SubscriptionCitySerializerUpdate
        else:
            return self.serializer_class

    def get_queryset(self):
        return models.SubscriptionCity.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.periodic_task.delete()
        instance.delete()

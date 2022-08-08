from rest_framework import generics
from rest_framework.response import Response

from src.weather.service.service import weather_s
from src.weather import models

from .utils import SubscriptionMixin
from .serializers import (
    CitySearchSerializer,
    CreateSubscriptionSerializer,
    UpdateSubscriptionSerializer,
    CitySerializer
)


class CityRetrieveView(generics.RetrieveAPIView):
    """
    Полная информация по городу
    ---
    """
    queryset = models.City.objects.all()
    serializer_class = CitySerializer


class CitySearchView(generics.GenericAPIView):
    """
    Поиск Города
    ---
    """
    serializer_class = CitySearchSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            city_id = weather_s.search_city(serializer.data['name'])
            data = serializer.data.copy()
            data.update({'id': city_id})
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


class SubscriptionCreateView(generics.CreateAPIView):
    """
    Создать подписку на город
    ---
    """
    serializer_class = CreateSubscriptionSerializer


class SubscriptionRetrieveView(SubscriptionMixin,
                               generics.RetrieveAPIView):
    """
    Получения полной информации по подписке
    ---
    """


class SubscriptionListView(SubscriptionMixin,
                           generics.ListAPIView):
    """
    Вывод списка подписок
    ---
    """


class SubscriptionUpdateView(generics.UpdateAPIView):
    """
    Обновить подписку
    ---
    """
    serializer_class = UpdateSubscriptionSerializer

    def get_queryset(self):
        return models.SubscriptionCity.objects.filter(owner=self.request.user)


class SubscriptionDestroyView(generics.DestroyAPIView):
    """
    Удаления подписки
    ---
    """

    def get_queryset(self):
        return models.SubscriptionCity.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        # Удаления записи с Periodic task
        instance.periodic_task.delete()
        instance.delete()

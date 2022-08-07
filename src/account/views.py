from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, UserUpdateSerializer
from .utils import UserMixin


class UserCreateView(generics.CreateAPIView):
    """
    Создания пользователя
    ---
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdateView(UserMixin, generics.UpdateAPIView):
    """
    Обновления данных пользователя
    ---
    """
    serializer_class = UserUpdateSerializer


class UserRetrieveView(UserMixin, generics.RetrieveAPIView):
    """
    Получения дынных пользователя
    ---
    """
    serializer_class = UserSerializer


class UserDestroyView(UserMixin, generics.DestroyAPIView):
    """
    Удаления пользователя
    ---
    """

    def perform_destroy(self, instance):
        """
        Удаление пользователя
        """
        # TODO пересмотреть удаления подписанных городов
        # удаления всех городов с подписок
        for subscription_city in instance.subscription_city.all():
            subscription_city.periodic_task.delete()
        instance.delete()

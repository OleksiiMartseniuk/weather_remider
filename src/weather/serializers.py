from rest_framework import serializers
from src.weather.models import City, SubscriptionCity
from src.weather.service.periodic_tast_service import service_task


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
        exclude = ['periodic_task']

    def create(self, validated_data):
        instance = super().create(validated_data)
        task_name = f'{instance.owner.username}_{instance.city.name}'
        instance.periodic_task = service_task.create(
            time=int(instance.periodicity_send_email),
            name=task_name,
            city_id=instance.city.id,
            owner_email=instance.owner.email
        )
        instance.save()
        return instance


class SubscriptionCitySerializerUpdate(serializers.ModelSerializer):
    """ Обновления подписки """
    class Meta:
        model = SubscriptionCity
        fields = ['periodicity_send_email']

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        service_task.update(
            time=int(obj.periodicity_send_email),
            task=obj.periodic_task
        )
        return obj

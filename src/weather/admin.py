from django.contrib import admin
from src.weather.models import City, SubscriptionCity


@admin.register(City)
class CitiAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_city',)
    list_filter = ('name', 'id_city',)


@admin.register(SubscriptionCity)
class SubscriptionCityAdmin(admin.ModelAdmin):
    list_display = ('owner', 'city', 'periodicity_send_email')
    list_filter = ('owner', 'city')

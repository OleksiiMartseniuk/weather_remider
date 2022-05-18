from django.contrib import admin
from src.weather.models import City


@admin.register(City)
class CitiAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_city',)
    list_filter = ('name', 'id_city',)

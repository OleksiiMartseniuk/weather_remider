from django.urls import path
from src.weather.views import CityView

urlpatterns = [
    path('city/<str:name>/', CityView.as_view({'get': 'retrieve'})),
    path('city/', CityView.as_view({'get': 'list', 'post': 'create'})),
]

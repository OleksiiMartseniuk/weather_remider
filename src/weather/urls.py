from django.urls import path
from src.weather import views

urlpatterns = [
    path('city/<str:name>/', views.CityView.as_view({'get': 'retrieve'})),
    path('city/', views.CityView.as_view({'get': 'list', 'post': 'create'})),
    path('subscription/<int:pk>/', views.SubscriptionCityView.as_view({'get': 'retrieve',
                                                                       'put': 'update',
                                                                       'delete': 'destroy'})),
    path('subscription/', views.SubscriptionCityView.as_view({'get': 'list', 'post': 'create'})),
]

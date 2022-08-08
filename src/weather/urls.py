from django.urls import path
from src.weather import views

urlpatterns = [
    path('city-search/', views.SearchCityView.as_view()),
    path('city/<int:pk>/', views.CityRetrieveView.as_view()),
    path('subscription-create/', views.CreateSubscriptionView.as_view()),
    path('subscription-list/', views.ListSubscriptionView.as_view()),
    path('subscription-update/<int:pk>/', views.UpdateSubscriptionView.as_view()),
    path('subscription-destroy/<int:pk>/', views.DestroySubscriptionView.as_view()),
]

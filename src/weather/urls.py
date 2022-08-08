from django.urls import path
from src.weather import views

urlpatterns = [
    path('city-search/',
         views.CitySearchView.as_view(),
         name='city-search'),
    path('city/<int:pk>/',
         views.CityRetrieveView.as_view(),
         name='city-ditail'),
    path('subscription-create/',
         views.SubscriptionCreateView.as_view(),
         name='subscription-create'),
    path('subscription-retrieve/<int:pk>/',
         views.SubscriptionRetrieveView.as_view(),
         name='subscription-retrieve'),
    path('subscription-list/',
         views.SubscriptionListView.as_view(),
         name='subscription-list'),
    path('subscription-update/<int:pk>/',
         views.SubscriptionUpdateView.as_view(),
         name='subscription-update'),
    path('subscription-destroy/<int:pk>/',
         views.SubscriptionDestroyView.as_view(),
         name='subscription-destroy'),
]

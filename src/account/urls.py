from django.urls import path
from src.account import views

urlpatterns = [
    path('create/', views.UserView.as_view({'post': 'create', 'get': 'retrieve'})),
]

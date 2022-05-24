from django.urls import path
from src.account import views

urlpatterns = [
    path('me/', views.UserView.as_view({'get': 'retrieve'})),
    path('create/', views.UserView.as_view({'post': 'create'})),
    path('update/', views.UserView.as_view({'put': 'update'})),
    path('delete/', views.UserView.as_view({'delete': 'destroy'})),
]

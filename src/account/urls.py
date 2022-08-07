from django.urls import path
from src.account import views

urlpatterns = [
    path('me/', views.UserRetrieveView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('update/', views.UserUpdateView.as_view()),
    path('delete/', views.UserDestroyView.as_view()),
]

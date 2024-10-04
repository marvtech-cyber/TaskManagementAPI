from django.urls import path
from .views import UserListAPIView, UserCreateAPIView

urlpatterns = [
    path('users/', UserListAPIView.as_view()),
    path('users/create/', UserCreateAPIView.as_view())
]
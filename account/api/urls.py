from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, ChangePasswordAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
]

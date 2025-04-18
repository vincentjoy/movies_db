from django.urls import path
from .views import RegisterUserView, UserDetailView, LoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
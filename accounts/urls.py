from django.urls import path
from .views import RegisterUserView, UserDetailView, LoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
]
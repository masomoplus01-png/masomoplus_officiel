from django.urls import path
from rest_framework import routers

from .views import LoginView, LogoutView, ProfileView, RegistrationView, UserViewset

router = routers.DefaultRouter()
router.register('users', UserViewset)

urlpatterns = [
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
] + router.urls

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (SignupViewSet, TokenViewSet, UserViewSet)


users_router = DefaultRouter()

users_router.register('users', UserViewSet, basename='users')
users_router.register('auth/signup', SignupViewSet, basename='signup')
users_router.register('auth/token', TokenViewSet, basename='token')

urlpatterns = [
    path('', include(users_router.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, token, signup

app_name = 'users'

users_router = DefaultRouter()
users_router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/token/', token, name='token'),
    path('auth/signup/', signup, name='signup'),
    path('', include(users_router.urls)),
]

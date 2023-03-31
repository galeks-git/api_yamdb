from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet


router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
#router_v1.register('titles', TitleViewSet)
#router_v1.register(
#    r'titles/(?P<title_id>\d+)/reviews',
#    ReviewViewSet,
#    basename='reviews')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]

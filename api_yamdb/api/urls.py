from django.urls import include, path
from rest_framework import routers
# from rest_framework.authtoken import views

from api.views import TitleViewSet, ReviewViewSet
# from api.views import PostViewSet, GroupViewSet, CommentViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet)
# router_v1.register('groups', GroupViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]



# from django.urls import include, path
# from rest_framework import routers

# from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet


# router_v1 = routers.DefaultRouter()
# router_v1.register('posts', PostViewSet, basename='posts')
# router_v1.register('groups', GroupViewSet, basename='groups')
# router_v1.register('follow', FollowViewSet, basename='follow')
# router_v1.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )

# urlpatterns = [
#     path('v1/', include(router_v1.urls)),
#     path('v1/', include('djoser.urls')),
#     path('v1/', include('djoser.urls.jwt')),
# ]


# from api.views import PostViewSet, GroupViewSet, CommentViewSet


# router_v1 = routers.DefaultRouter()
# router_v1.register('posts', PostViewSet)
# router_v1.register('groups', GroupViewSet)
# router_v1.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )

# urlpatterns = [
#     path('v1/', include(router_v1.urls)),
#     path('v1/api-token-auth/', views.obtain_auth_token),
# ]

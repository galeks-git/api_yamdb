from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsAdminPermission
from users.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с юзерами."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminPermission, IsAuthenticated)


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для регистрации пользователя."""

    permission_classes = (AllowAny,)


class TokenViewSet(viewsets.ViewSet):
    """Вьюсет для получения токена."""

    permission_classes = (AllowAny,)

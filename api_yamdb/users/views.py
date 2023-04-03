from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.permissions import IsAdmin
from users.models import User
from users.serializers import (SignupSerializer,
                               TokenSerializer,
                               UsersSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы администратора с юзерами."""

    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['patch', 'get'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """Просмотр и редактирование пользователями своих данных"""
        if request.method == 'GET':
            serializer = UsersSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UsersSerializer(self.request.user,
                                     data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регтстрация пользователей."""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    if User.objects.filter(email=email).exists():
        if not User.objects.filter(username=username).exists():
            # email занят username не занят
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # email занят username занят
        return Response(status=status.HTTP_200_OK)
    else:
        if User.objects.filter(username=username).exists():
            # email не занят username занят
            return Response(status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get_or_create(email=email, username=username)[0]
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Код подтверждения',
        confirmation_code,
        'admin@yamdb.fake',
        [email],
        fail_silently=False
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)

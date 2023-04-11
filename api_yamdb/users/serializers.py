from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.validators import reg_validator
from users.models import User

USER_USERNAME_MAX_LEN = 150
USER_EMAIL_MAX_LEN = 254


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'bio', 'email', 'role']


class SignupSerializer(serializers.Serializer):

    email = serializers.EmailField(
        max_length=USER_EMAIL_MAX_LEN,
        required=True,
    )
    username = serializers.CharField(
        max_length=USER_USERNAME_MAX_LEN,
        required=True,
        validators=(reg_validator,)
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                {'Имя пользователя не может быть "me"'})
        return value


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data

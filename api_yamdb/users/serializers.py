from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if (value == 'me'):
            raise serializers.ValidationError(
                'Для username нельзя выбрать me'
            )
        return value

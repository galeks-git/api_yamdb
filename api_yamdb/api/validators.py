from datetime import datetime
from django.core.validators import RegexValidator
from rest_framework.serializers import ValidationError

reg_message = 'username может содержать латинские буквы, цифры, символы .+-_@'
reg_validator = RegexValidator(r"^[\w.@+-]+", reg_message)


def validate_year(self, value):
    year = datetime.now().year
    if value > year:
        raise ValidationError(
            f'Year не может быть больше {year}')
    return value

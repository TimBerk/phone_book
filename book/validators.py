import phonenumbers

from django.core.exceptions import ValidationError


def phone_validator(value):
    number = phonenumbers.parse(value, None)
    if not value or not phonenumbers.is_valid_number(number):
        raise ValidationError(
            f'Некорректный номер: {number}'
        )

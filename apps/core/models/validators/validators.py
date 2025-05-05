from datetime import date

from django.core.exceptions import ValidationError


def validate_not_future(value):
    if value > date.today():
        raise ValidationError("The date cannot be in the future")

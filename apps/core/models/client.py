import datetime
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import DateField

from . import Address
from .validators.validators import validate_not_future # import with using `.` по суті - це відносний імпорт

class Gender(models.IntegerChoices):
    NOT_SPECIFIED = 0, "Not Specified"
    MALE = 1, "Male"
    FEMALE = 2, "Female"
    OTHER = 3, "Other"


# def validate_not_future(value):
#     if value > date.today():
#         raise ValidationError("The date cannot be in the future")


class Client(models.Model):
    # Основні поля
    id = models.AutoField(primary_key=True) # Autofield - тип поля для id
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    birthday = models.DateField(validators=[validate_not_future])
    email = models.EmailField()
    gender = models.IntegerField(choices=Gender.choices) # Обираємо всі варіанти з `Gender.choices`

    # Додаткові поля
    photo = models.ImageField() # field to save image of person
    
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True) # При створенні чи передачі даних моделі дата і час будуть записуватись в це поле
    updated_at = models.DateTimeField(auto_now=True)

    # Address field
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='addresses')

    # Методи
    def __str__(self):
        return (f"{self.id} "
                f"{self.surname} "
                f"{self.name} "
                f"{self.patronymic} "
                f"{self.birthday} "
                f"{self.email} "
                f"{self.gender} "
                )











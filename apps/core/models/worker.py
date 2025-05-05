from django.db import models

from apps.core.models.client import Gender
from apps.core.models.validators.validators import validate_not_future


class Worker(models.Model):
    # Основні поля
    id = models.AutoField(primary_key=True)  # Autofield - тип поля для id
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    birthday = models.DateField(validators=[validate_not_future])
    email = models.EmailField()
    gender = models.IntegerField(choices=Gender.choices)  # Обираємо всі варіанти з `Gender.choices`
    education = models.TextField() # Worker education, skills and experience

    # Address field

    # Додаткові поля
    photo = models.ImageField()  # field to save image of person

    # Метадані
    created_at = models.DateTimeField(
        auto_now_add=True)  # При створенні чи передачі даних моделі дата і час будуть записуватись в це поле
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.id} "
                f"{self.surname} "
                f"{self.name} "
                f"{self.patronymic} "
                f"{self.birthday} "
                f"{self.email} "
                f"{self.gender} "
                f"{self.education} "
                )
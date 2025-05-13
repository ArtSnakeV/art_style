# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys

import django


from datetime import date, datetime
from random import choices

from django.test import TestCase

from apps.core.models import Specialist
from apps.core.models.client import Gender


# class Specialist(models.Model):
#     # Основні поля
#     id = models.AutoField(primary_key=True)  # Autofield - тип поля для id
#     surname = models.CharField(max_length=21)
#     name = models.CharField(max_length=21)
#     patronymic = models.CharField(max_length=21)
#     birthday = models.DateField(validators=[validate_not_future])
#     email = models.EmailField()
#     gender = models.IntegerField(choices=Gender.choices)  # Обираємо всі варіанти з `Gender.choices`
#     education = models.TextField() # Worker education, skills and experience
#     specialities = models.ManyToManyField("Speciality", related_name="specialists")
#     # Address field#
#     # Додаткові поля
#     # photo = models.ImageField()  # field to save image of person#
#     # Метадані
#     created_at = models.DateTimeField(
#         auto_now_add=True)  # При створенні чи передачі даних моделі дата і час будуть записуватись в це поле
#     updated_at = models.DateTimeField(auto_now=True)#
#     clients = models.ManyToManyField(Client, related_name="specialists")
#     contacts = models.ManyToManyField("Contact", related_name="workers")


class SpecialistModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестового спеціаліста перед кожним тестом"""
        self.specialist_data = {
            'surname' : 'Surname',
            'name' : 'Iol',
            'patronymic': 'Zabiyaka',
            'birthday': date(2015, 11, 10),
            'email': 'iol@zab.com',
            'gender': Gender.MALE,
            'education': 'Beauty Academy of Amazing Color Unlimited',
            # 'specialities': '',
            # 'photo': '',
            # 'created_at': datetime.now(),
            # 'updated_at': datetime.now(),
            # 'clients' : '',
            # 'contacts': '',
        }
        # Створення об'єкта спеціаліста, збереження в базу
        self.specialist = Specialist.objects.create(**self.specialist_data) # Спосіб збереження спеціаліста в базу даних

    def test_create_specialist(self):
        """Перевірка, що спеціаліст правильно створюється в базі даних"""
        specialist = Specialist.objects.get(id=self.specialist.id) # get - метод для тримання спеціаліста
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(specialist.surname, self.specialist_data['surname'])
        self.assertEqual(specialist.name, self.specialist_data['name'])
        self.assertEqual(specialist.patronymic, self.specialist_data['patronymic'])
        self.assertEqual(specialist.birthday, self.specialist_data['birthday'])
        self.assertEqual(specialist.email, self.specialist_data['email'])
        self.assertEqual(specialist.gender, self.specialist_data['gender'])
        self.assertEqual(specialist.education, self.specialist_data['education'])
        # self.assertEqual(specialist.specialities, self.specialist_data['specialities'])
        # self.assertEqual(specialist.photo, self.specialist_data['photo'])
        self.assertEqual(specialist.created_at, self.specialist_data['created_at'])
        self.assertEqual(specialist.updated_at, self.specialist_data['updated_at'])
        # self.assertEqual(specialist.clients, self.specialist_data['clients'])
        # self.assertEqual(specialist.contacts, self.specialist_data['contacts'])

        #2 коли реалізовано метод __eq__ __hash__ в моделі Specialist
        self.assertEqual(specialist, self.specialist)


    def test_read_specialist(self):
        """Перевірка, що дані спеціаліста можна коректно прочитати"""
        specialist = Specialist.objects.get(id=self.specialist.id)
        self.assertEqual(specialist.surname, 'Surname')
        self.assertEqual(specialist.name, 'Iol')
        self.assertEqual(specialist.patronymic, 'Zabiyaka')
        self.assertEqual(specialist.birthday, date(2015, 11, 10))
        self.assertEqual(specialist.email, 'iol@zab.com')
        self.assertEqual(specialist.gender, Gender.MALE)
        self.assertEqual(specialist.education, 'Beauty Academy of Amazing Color Unlimited')
        # self.assertEqual(specialist.specialities, '')
        # self.assertEqual(specialist.photo, '')
        # self.assertEqual(specialist.created_at, datetime.now())
        # self.assertEqual(specialist.updated_at, datetime.now())
        # self.assertEqual(specialist.clients, '')
        # self.assertEqual(specialist.contacts, '')


    def test_update_specialist(self):
        """Перевірка, що спеціаліст оновлюється коректно"""
        self.specialist.surname = 'Givancy'
        self.specialist.name = 'Iohann'
        self.specialist.patronymic = 'Hanovich'
        self.specialist.birthday = date(2021, 1, 15)
        self.specialist.email = 'hanTheOne@givancy.com'
        self.specialist.gender = Gender.MALE
        self.specialist.education = 'The University of Laser Inversion in future life engineering, faculty of Cybernetes'
        # self.specialist.specialities = ''
        # self.specialist.photo = ''
        # self.specialist.created_at = datetime.now()
        # self.specialist.updated_at = datetime.now()
        # self.specialist.clients = ''
        # self.specialist.contacts = ''
        self.specialist.save()

    def test_delete_specialist(self):
        """перевірка, що спеціаліст коректно видаляється"""
        specialist_id = self.specialist.id
        self.specialist.delete()

        with self.assertRaises(Specialist.DoesNotExist):
            Specialist.objects.get(id=specialist_id)









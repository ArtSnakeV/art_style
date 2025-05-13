# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys
from decimal import Decimal

import django


from datetime import date
from random import choices

from django.test import TestCase

from apps.core.models import Speciality


# class Speciality(models.Model):
#     id = models.AutoField(primary_key=True)
#     speciality_name = models.CharField(21)



class SpecialityModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестової спеціальності перед кожним тестом"""
        self.speciality_data = {
            'speciality_name' : 'Haircut master',
        }
        # Створення об'єкта спеціальності, збереження в базу
        self.speciality = Speciality.objects.create(**self.speciality_data) # Спосіб збереження спеціальності в базу даних

    def test_create_speciality(self):
        """Перевірка, що спеціальність правильно створюється в базі даних"""
        speciality = Speciality.objects.get(id=self.speciality.id) # get - метод для тримання спеціальності
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(speciality.speciality_name, self.speciality_data['speciality_name'])
        #2 коли реалізовано метод __eq__ __hash__ в моделі Speciality
        self.assertEqual(speciality, self.speciality)

    def test_read_speciality(self):
        """Перевірка, що дані спеціальності можна коректно прочитати"""
        speciality = Speciality.objects.get(id=self.speciality.id)
        self.assertEqual(speciality.speciality_name, 'Haircut master')

    def test_update_speciality(self):
        """Перевірка, що спеціальність оновлюється коректно"""
        self.speciality.speciality_name = 'Haircut master'
        self.speciality.save()

    def test_delete_speciality(self):
        """перевірка, що спеціальність коректно видаляється"""
        speciality_id = self.speciality.id
        self.speciality.delete()

        with self.assertRaises(Speciality.DoesNotExist):
            Speciality.objects.get(id=speciality_id)









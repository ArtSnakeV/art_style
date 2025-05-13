# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys
from decimal import Decimal

import django


from datetime import date
from random import choices

from django.test import TestCase

from apps.core.models import Service


# class Service(models.Model):
#     id = models.AutoField(primary_key=True)  # Id
#     service_title = models.CharField(50)
#     service_description = models.CharField(50)
#     service_price= models.DecimalField(max_digits=8, decimal_places=2, default=0)



class ServiceModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестової послуги перед кожним тестом"""
        self.service_data = {
            'service_title' : 'Classic haircut, man',
            'service_description' : 'Classic man haircut as per list attached',
            'service_price': Decimal(140.00),
        }
        # Створення об'єкта послуги, збереження в базу
        self.service = Service.objects.create(**self.service_data) # Спосіб збереження послуги в базу даних

    def test_create_service(self):
        """Перевірка, що послуга правильно створюється в базі даних"""
        service = Service.objects.get(id=self.service.id) # get - метод для тримання послугу
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(service.service_title, self.service_data['service_title'])
        self.assertEqual(service.service_description, self.service_data['service_description'])
        self.assertEqual(service.service_price, self.service_data['service_price'])
        #2 коли реалізовано метод __eq__ __hash__ в моделі Service
        self.assertEqual(service, self.service)

    def test_read_service(self):
        """Перевірка, що дані послуги можна коректно прочитати"""
        service = Service.objects.get(id=self.service.id)
        self.assertEqual(service.service_title, 'Classic haircut, man')
        self.assertEqual(service.service_description, 'Classic man haircut as per list attached')
        self.assertEqual(service.service_price, Decimal(140.00))

    def test_update_service(self):
        """Перевірка, що послуга оновлюється коректно"""
        self.service.service_title = 'Classic haircut, man'
        self.service.service_description = 'Classic man haircut as per list attached'
        self.service.service_price = Decimal(140.00)
        self.service.save()

    def test_delete_service(self):
        """перевірка, що послуга коректно видаляється"""
        service_id = self.service.id
        self.service.delete()

        with self.assertRaises(Service.DoesNotExist):
            Service.objects.get(id=service_id)









# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys

import django


from datetime import date
from random import choices

from django.test import TestCase

from apps.core.models import Address

# class Address(TimeStampedModel):
#     id = models.BigAutoField(primary_key=True)  # Id
#     country = models.CharField(max_length=20)
#     region = models.CharField(max_length=20)
#     district = models.CharField(max_length=20)
#     street = models.CharField(max_length=20)
#     house = models.CharField(max_length=5)
#     flat = models.CharField(max_length=5)

class AddressModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестової адреси перед кожним тестом"""
        self.address_data = {
            'country' : 'Antigua and Barbuda',
            'region' : 'Caribbean',
            'district' : 'St Mary',
            'street': 'Road Harbour, Nelson`s Dockyard',
            'house': '1',
            'flat': '15',
        }
        # Створення об'єкта акаунта, збереження в базу
        self.address = Address.objects.create(**self.address_data) # Спосіб збереження адреси в базу даних

    def test_create_address(self):
        """Перевірка, що адреса правильно створюється в базі даних"""
        address = Address.objects.get(id=self.address.id) # get - метод для тримання адреси
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(address.country, self.address_data['country'])
        self.assertEqual(address.region, self.address_data['region'])
        self.assertEqual(address.district, self.address_data['district'])
        self.assertEqual(address.street, self.address_data['street'])
        self.assertEqual(address.house, self.address_data['house'])
        self.assertEqual(address.flat, self.address_data['flat'])
        #2 коли реалізовано метод __eq__ __hash__ в моделі Address
        self.assertEqual(address, self.address)


    def test_read_address(self):
        """Перевірка, що дані адреси можна коректно прочитати"""
        address = Address.objects.get(id=self.address.id)
        self.assertEqual(address.country, 'Antigua and Barbuda')
        self.assertEqual(address.region, 'Caribbean')
        self.assertEqual(address.district, 'St Mary')
        self.assertEqual(address.street, 'Road Harbour, Nelson`s Dockyard')
        self.assertEqual(address.house, '1')
        self.assertEqual(address.flat, '15')

    def test_update_address(self):
        """Перевірка, що адреса оновлюється коректно"""
        self.address.country = 'Antigua and Barbuda'
        self.address.region = 'Caribbean'
        self.address.district = 'St Mary'
        self.address.street = 'Road Harbour, Nelson`s Dockyard'
        self.address.house = '1'
        self.address.flat = '15'
        self.address.save()

    def test_delete_address(self):
        """перевірка, що адресв коректно видаляється"""
        address_id = self.address.id
        self.address.delete()

        with self.assertRaises(Address.DoesNotExist):
            Address.objects.get(id=address_id)









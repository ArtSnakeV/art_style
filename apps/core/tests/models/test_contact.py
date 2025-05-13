# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys

import django


from datetime import date
from random import choices

from django.test import TestCase

from apps.core.models import Contact


# class Contact(models.Model):
#
#     id = models.AutoField(primary_key=True) # Id
#
#     contact_type = models.CharField(max_length=21) # phone, telegram, etc
#
#     contact_value = models.CharField(max_length=21) # value



class ContactModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестового контакту перед кожним тестом"""
        self.contact_data = {
            'contact_type' : 'Instagramm',
            'contact_value' : '@ExampleAccount',
        }
        # Створення об'єкта контакту, збереження в базу
        self.contact = Contact.objects.create(**self.contact_data) # Спосіб збереження контакту в базу даних

    def test_create_contact(self):
        """Перевірка, що контакт правильно створюється в базі даних"""
        contact = Contact.objects.get(id=self.contact.id) # get - метод для тримання контакту
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(contact.contact_type, self.contact_data['contact_type'])
        self.assertEqual(contact.contact_value, self.contact_data['contact_value'])
        #2 коли реалізовано метод __eq__ __hash__ в моделі Contact
        self.assertEqual(contact, self.contact)


    def test_read_contact(self):
        """Перевірка, що дані контакту можна коректно прочитати"""
        contact = Contact.objects.get(id=self.contact.id)
        self.assertEqual(contact.contact_type, 'Instagramm')
        self.assertEqual(contact.contact_value, '@ExampleAccount')

    def test_update_contact(self):
        """Перевірка, що контакт оновлюється коректно"""
        self.contact.contact_type = 'Instagramm'
        self.contact.contact_value = '@ExampleAccount'
        self.contact.save()

    def test_delete_contact(self):
        """перевірка, що контакт коректно видаляється"""
        contact_id = self.contact.id
        self.contact.delete()

        with self.assertRaises(Contact.DoesNotExist):
            Contact.objects.get(id=contact_id)









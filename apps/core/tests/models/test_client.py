# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys

import django

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()

from datetime import date
from random import choices

from django.test import TestCase

from apps.core.models.client import Gender, Client


# id = models.AutoField(primary_key=True) # AutoField - тип поля для id
#     surname = models.CharField(max_length=21)
#     name = models.CharField(max_length=21)
#     patronymic = models.CharField(max_length=21)
#     birthday = models.DateField(validators=[validate_not_future])
#     email = models.EmailField()
#     gender = models.IntegerField(choices=Gender.choices) # Обираємо всі варіанти з `Gender.choices`

class ClientModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестового клієнта перед кожним тестом"""
        self.client_data = {
            'surname' : 'Voronko',
            'name' : 'Amelia',
            'patronymic' : 'Aaronivna',
            'birthday' : date(1990, 5, 15),
            'email': 'a@t.com',
            'gender': Gender.FEMALE,
        }
        # Створення об'єкта клієнта, збереження в базу
        self.client = Client.objects.create(**self.client_data) # Спосіб збереження клієнта в базу даних

    def test_create_client(self):
        """Перевірка, що клієнт правильно створюється в базі даних"""
        client = Client.objects.get(id=self.client.id) # get - метод для тримання клієнта
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(client.surname, self.client_data['surname'])
        self.assertEqual(client.name, self.client_data['name'])
        self.assertEqual(client.patronymic, self.client_data['patronymic'])
        self.assertEqual(client.birthday, self.client_data['birthday'])
        self.assertEqual(client.email, self.client_data['email'])
        self.assertEqual(client.gender, self.client_data['gender'])
        #2 коли реалізовано метод __eq__ __hash__ в моделі Client
        self.assertEqual(client, self.client)


    def test_read_client(self):
        """Перевірка, що дані клієнта можна коректно прочитати"""
        client = Client.objects.get(id=self.client.id)
        self.assertEqual(client.surname, 'Voronko')
        self.assertEqual(client.name, 'Amelia')
        self.assertEqual(client.patronymic,'Aaronivna')
        self.assertEqual(client.birthday, date(1990, 5, 15))
        self.assertEqual(client.email, 'a@t.com')
        self.assertEqual(client.gender, Gender.FEMALE)

    def test_update_client(self):
        """Перевірка, що клієнт оновлюється коректно"""
        self.client.name = 'Gavrylo'
        self.client.surname = 'Gregory'
        self.client.patronymic = 'Izyaslavovich'
        self.client.birthday = date(2012, 10, 10)
        self.client.email = 'gIzi@ton.ton'
        self.client.gender = Gender.MALE
        self.client.save()

    def test_delete_client(self):
        """перевірка, що клієнт коректно видаляється"""
        client_id = self.client.id
        self.client.delete()

        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(id=client_id)


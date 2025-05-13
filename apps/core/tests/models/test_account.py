# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys

import django


from datetime import date
from random import choices

from django.test import TestCase

from apps.core.models import Account


# id = models.BigAutoField(primary_key=True) # Id
#     account_type = models.CharField(50)
#     account_number = models.CharField(50)


class AccountModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестового акаунта перед кожним тестом"""
        self.account_data = {
            'account_type' : 'myPay',
            'account_number' : '111111111111111',
        }
        # Створення об'єкта акаунта, збереження в базу
        self.account = Account.objects.create(**self.account_data) # Спосіб збереження акаунта в базу даних

    def test_create_account(self):
        """Перевірка, що акаунт правильно створюється в базі даних"""
        account = Account.objects.get(id=self.account.id) # get - метод для тримання акаунта
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(account.account_type, self.account_data['account_type'])
        self.assertEqual(account.account_number, self.account_data['account_number'])
        #2 коли реалізовано метод __eq__ __hash__ в моделі Account
        self.assertEqual(account, self.account)


    def test_read_account(self):
        """Перевірка, що дані акаунта можна коректно прочитати"""
        account = Account.objects.get(id=self.account.id)
        self.assertEqual(account.account_type, 'myPay')
        self.assertEqual(account.account_number, '111111111111111')

    def test_update_account(self):
        """Перевірка, що акаунт оновлюється коректно"""
        self.account.account_type = 'smartAcc'
        self.account.account_number = '33333333333333333'
        self.account.save()

    def test_delete_account(self):
        """перевірка, що акаунт коректно видаляється"""
        account_id = self.account.id
        self.account.delete()

        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(id=account_id)









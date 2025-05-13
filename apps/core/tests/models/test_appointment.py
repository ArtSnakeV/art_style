# Підготуємо django, щоб мати можливість запускати тест з файлу класу
import os
import sys

import django


from datetime import date, datetime
from random import choices

from django.test import TestCase

from apps.core.models import Appointment


# class Appointment(models.Model):
#     id = models.BigAutoField(primary_key=True)  # BigAutoField for large amount of `id`s
#     time_from = models.DateTimeField() # Date and time of beginning of visit
#     time_till = models.DateTimeField() # Date and time of end of visit
#     appointment_details = models.CharField(max_length=300) # Provided service
#     price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
#     service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
#     is_completed = models.BooleanField(False) # Field to know if appointment passed and service completed

class AppointmentModelTest(TestCase): #TestCase class - клас набір тестів для однієї задачі
    def setUp(self):
        """"Створення тестового запису перед кожним тестом"""
        self.appointment_data = {
            'time_from' : datetime(2025, 9, 20, 12, 0, 0),
            'time_till' : datetime(2025, 9, 20, 14, 0, 0),
            'appointment_details': 'Detailed haircut with washing head, drying and style',
            'price': '300.00',
            'client': '1',
            'service': '3',
            'is_completed': 'True',
        }
        # Створення об'єкта запису, збереження в базу
        self.appointment = Appointment.objects.create(**self.appointment_data) # Спосіб збереження запису в базу даних

    def test_create_appointment(self):
        """Перевірка, що запис правильно створюється в базі даних"""
        appointment = Appointment.objects.get(id=self.appointment.id) # get - метод для тримання запису
        # Перевірка ідентичності через співпадіння полів
        #1
        self.assertEqual(appointment.time_from, self.appointment_data['time_from'])
        self.assertEqual(appointment.time_till, self.appointment_data['time_till'])
        self.assertEqual(appointment.appointment_details, self.appointment_data['appointment_details'])
        self.assertEqual(appointment.price, self.appointment_data['price'])
        # self.assertEqual(appointment.client, self.appointment_data['client'])
        # self.assertEqual(appointment.service, self.appointment_data['service'])
        self.assertEqual(appointment.is_completed, self.appointment_data['is_completed'])
        #2 коли реалізовано метод __eq__ __hash__ в моделі Appointment
        self.assertEqual(appointment, self.appointment)


    def test_read_appointment(self):
        """Перевірка, що дані запису можна коректно прочитати"""
        appointment = Appointment.objects.get(id=self.appointment.id)
        self.assertEqual(appointment.time_from, datetime(2025, 9, 20, 12, 0, 0))
        self.assertEqual(appointment.time_till, datetime(2025, 9, 20, 14, 0, 0))
        self.assertEqual(appointment.appointment_details, 'Detailed haircut with washing head, drying and style')
        self.assertEqual(appointment.price, '300.00')
        # self.assertEqual(appointment.client, '1')
        # self.assertEqual(appointment.service, '3')
        self.assertEqual(appointment.is_completed, 'True')

    def test_update_appointment(self):
        """Перевірка, що запис оновлюється коректно"""
        self.appointment.time_from = datetime(2025, 9, 20, 12, 0, 0)
        self.appointment.time_till = datetime(2025, 9, 20, 14, 0, 0)
        self.appointment.time_till = 'Detailed haircut with washing head, drying and style'
        self.appointment.time_till = '300.00'
        self.appointment.time_till = '1'
        # self.appointment.time_till = '3'
        # self.appointment.time_till = 'True'
        self.appointment.save()

    def test_delete_appointment(self):
        """перевірка, що запис коректно видаляється"""
        appointment_id = self.appointment.id
        self.appointment.delete()

        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=appointment_id)









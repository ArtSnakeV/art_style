from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# Можемо реалізовувати методи, які будуть реагувати на певну адресу

def hello(request): # Один параметр `request`, що прийматиме запити від браузеру
    return HttpResponse("Hello World!")

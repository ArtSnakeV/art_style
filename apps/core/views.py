from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# Можемо реалізовувати методи, які будуть реагувати на певну адресу

def hello(request): # Один параметр `request`, що прийматиме запити від браузеру
    # return HttpResponse("Hello World!", content_type='text/plain')
    return HttpResponse("<h1>Hello World!</h1>", content_type='text/html')

def about_project(request):
    return render(request, 'about_project.html') # render - повертає html-сторінку

def about_core(request):
    return render(request, 'core/about_core.html')

def clients(request):
    return render(request, 'core/pages/clients.html') #
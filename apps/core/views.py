from django import views
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.core.forms import ClientForm
from apps.core.models import Client
from apps.core.models.client import Gender


# Create your views here.

# Можемо реалізовувати методи, які будуть реагувати на певну адресу

def hello(request): # Один параметр `request`, що прийматиме запити від браузеру
    # return HttpResponse("Hello World!", content_type='text/plain')
    return HttpResponse("<h1>Hello World!</h1>", content_type='text/html')

def about_project(request):
    return render(request, 'about_project.html') # render - повертає html-сторінку

def about_core(request):
    return render(request, 'core/about_core.html')

@require_http_methods(['GET', 'POST'])
def clients(request):
    # POST
    if request.method == 'POST':
        surname =  request.POST.get('surname')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')

        # Можна додати валідацію

        Client.objects.create(
            surname = surname,
            name = name,
            patronymic = patronymic,
            email = email,
            birthday = birthday,
            gender = gender
        )

        return redirect('core:clients')


    # GET
    context = {
        'client_list': Client.objects.all(),
        'gender_choices': Gender,
    }
    return render(request, 'core/pages/clients.html', context) #


class ClientDetailUpdateView(views.View):
    def get(self, request, pk): # parameter `request` given to make running it as `get`
        client = get_object_or_404(Client, pk=pk)
        print(client)
        client_form = ClientForm(instance=client)

        context={
            'client_form': client_form,
        }
        return render(request, 'core/pages/client_detail.html', context)

    def post(self, request, pk):
        pass



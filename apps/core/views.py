from contextlib import nullcontext

from django import views
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.core.forms import ClientForm, AddressForm, ContactForm
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

        # Спроба отримати клієнта, або помилка
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        contact_list = getattr(client, 'contacts', None).all()

        print(client)
        # Створення об'єкта форми, з даними client
        client_form = ClientForm(instance=client, prefix='client') #client-surname
        address_form = AddressForm(instance=address, prefix='address')
        contact_form_list = [ContactForm(instance=contact, prefix=str(i)) for i, contact in contact_list]  # Creating list generator
        contact_form = ContactForm(prefix='contact')

        # Передача форми на сторінку
        context={
            'client_form': client_form,
            'address_form': address_form,
            'client': client, # Transferring `client` to the page
            'contact_form_list': contact_form_list,
            'contact_form': contact_form,
        }
        return render(request, 'core/pages/client_detail.html', context)

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)

        # Check if delete button was pressed
        if 'delete_client' in request.POST:
            if client.address:
                client.address.delete()  # Deleting
            client.delete()
            return redirect('core:clients')  # redirect to clients list or elsewhere

        if 'delete_address' in request.POST:
            if address:
                address.delete()
            return redirect('core:client_detail', pk=pk)


        # Для отримання файлу з форми!!!
        client_form = ClientForm(request.POST, request.FILES, instance=client, prefix='client')   # механізм instance дозволяє дістати поля, які не видимі в формі, щоб коректно зберегти дані згодом
        address_form = AddressForm(request.POST, instance=address, prefix='address')

        if 'submit_client' in request.POST: # Обираємо наш `submit` в post запиті
            
            if client_form.is_valid():
                client_form.save() # Зберігаємо дані прямо через саму форму
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(client_form.errors)

        elif 'submit_address' in request.POST: # Обираємо наш `submit` в post запиті
            if address_form.is_valid():
                # client = get_object_or_404(Client, pk=pk)
                address = address_form.save() # Зберігаємо дані прямо другої форми
                client.address = address # Присвоюємо об'єкт адреси полю клієнта
                client.save() # Зберігаємо дані в клієнті
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(address_form.errors)


        elif 'submit_contact' in request.POST: #form for simple adding contact
            contact_form = ContactForm(request.POST, prefix='contact')
            if contact_form.is_valid():
                contact = contact_form.save(commit = False) # We are not saving directly in database jet
                # contact.client = client
                contact.save()
                return redirect ('core:client_detail', pk=client.pk)
            else:
                print(address_form.errors)

        # Deleting `contact`
        elif 'submit_contact_delete' in request.POST:
            prefix=request.POST.get('submit_contact_delete')
            contact_list = client.contacts.all() # Getting from database list of contacts
            try:
                contact=contact_list[int(prefix)]
            except (IndexError, ValueError):
                return redirect('core:client_detail', pk=client.pk)
            contact.delete()
            return redirect('core/client_detail', pk=client.pk)

        # Рендер у випадку помилки, залишаємо дані, введені у форму
        context = {
            'client_form': client_form,
            'address_form': address_form,
            'client': client,
        }

        return render(request, 'core/pages/client_detail.html', context)



# icons for ondelete: 🗑️ 💾 ❌ ✖ ⋮






from contextlib import nullcontext

from django import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.core import forms
from apps.core.forms import ClientForm, AddressForm, ContactForm
from apps.core.models import Client, Contact
from apps.core.models.client import Gender


# Create your views here.

# Можемо реалізовувати методи, які будуть реагувати на певну адресу

def hello(request): # Один параметр `request`, що прийматиме запити від браузеру
    # return HttpResponse("Hello World!", content_type='text/plain')
    return HttpResponse("<h1>Hello World!</h1>", content_type='text/html')

def about_project(request):
    return render(request, 'about_project.html') # render - повертає html-сторінку

# SECURITY 1
@login_required
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

#SECURITY 2 LoginRequiredMixin Має наслідуватись першим
class ClientDetailUpdateView(LoginRequiredMixin, views.View):
    def get(self, request, pk): # parameter `request` given to make running it as `get`

        # Спроба отримати клієнта, або помилка
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        # contact_list = getattr(client, 'contacts', None).all()
        contacts_qs = client.contacts.all()
        # print(f"contacts_qs:{contacts_qs}")

        print(client)
        # Створення об'єкта форми, з даними client
        client_form = ClientForm(instance=client, prefix='client') #client-surname
        address_form = AddressForm(instance=address, prefix='address')
        # contact_form_list = [ContactForm(instance=contact, prefix=str(i)) for i, contact in enumerate(contacts_qs)]  # Creating list generator
        contact_form_list = [
            ContactForm(instance=contact, prefix=f'contact_{i}')
            for i, contact in enumerate(contacts_qs)
        ]
        contact_form = ContactForm(prefix='contact')

        # Передача форми на сторінку
        context={
            'client_form': client_form,
            'address_form': address_form,
            'client': client, # Transferring `client` to the page
            'contact_form_list': contact_form_list,
            # 'contact_form_list': contacts_qs,
            'contact_form': contact_form,

            'contact_list': contacts_qs,
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
        # contact_form = ContactForm(request.POST, instance = contacts, prefix='contacts' )

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



        elif 'submit_contact' in request.POST:  # form for simple adding contact
            contact_form = ContactForm(request.POST, prefix='contact')
            if contact_form.is_valid():
                contact = contact_form.save(commit=False)  # We are not saving directly in database jet
                # n_contact = Contact(contact_form.cleaned_data['contact_type'], contact_form.cleaned_data['contact_value'])
                n_contact = contact_form.save()
                client.contacts.add(n_contact)

                print(n_contact)
                # print(client.contacts.all)

                print("Here we are")



                # contact_list = client.contacts.all()
                # print(f"Client contact: {contact}")
                # client.contacts.add(contact)
                # # contacts_from_client = client.contacts.all().add(contact)
                # # client.contacts = contacts_from_client
                # print("Client contact1")
                # contact.save()
                # # client.contacts.save()
                # print("Client contact2")
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(address_form.errors)

        # Deleting `contact`
        elif 'submit_contact_delete' in request.POST:
            # print("Delete contact pressed")
            prefix=request.POST.get('submit_contact_delete')
            # Let's extract numeric part from prefix
            index_str = prefix.split('_')[-1]  # '0' as an example
            index = int(index_str)
            print(f"our prefix for deleting: {index}")
            contact_list = client.contacts.all() # Getting from database list of contacts
            try:
                contact_del=contact_list[index]
            except (IndexError, ValueError) as e:
                print(f"An exception occurred: {type(e).__name__}: {e}") # Getting information about our error
                return redirect('core:client_detail', pk=client.pk)
            contact_del.delete() # Let's delete mentioned contact
            return redirect('core:client_detail', pk=client.pk)

        elif 'submit_contact_update' in request.POST:
            contact_list = client.contacts.all()
            prefix = request.POST.get('submit_contact_update')
            index = int(prefix.split('_')[-1])  # getting last number from the prefix (id in our contact table for mentioned Client)
            # Fetch the existing contact
            existing_contact = contact_list[index]
            # Bind the form to the existing instance
            contact_form = ContactForm(request.POST, prefix=prefix, instance=existing_contact)

            if contact_form.is_valid():
                contact_form.save()
                return redirect('core:client_detail', pk=client.pk)
            else:
                print("Errors occurs while trying to save updated contact.")
                return redirect('core:client_detail', pk=client.pk)

        # Рендер у випадку помилки, залишаємо дані, введені у форму
        context = {
            'client_form': client_form,
            'address_form': address_form,
            'client': client,
        }

        return render(request, 'core/pages/client_detail.html', context)



# icons for ondelete: 🗑️ 💾 ❌ ✖ ⋮

# @csrf_exempt # annotation to avoid using csrf token, better use csrf token
def address_form(request, pk):
    print('views address_form')
    print(request)
    if request.method == 'POST':
        # region = request.POST.get('region') # Example of getting data form the POST
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        address_form = AddressForm(request.POST, instance=address, prefix='address')
        if address_form.is_valid():
            # client = get_object_or_404(Client, pk=pk)
            address = address_form.save()  # Зберігаємо дані прямо другої форми
            client.address = address  # Присвоюємо об'єкт адреси полю клієнта
            client.save()  # Зберігаємо дані в клієнті
            return JsonResponse({'message': f'Successfully updated address for Client {pk}!'})
    return JsonResponse({'message': f'Wrong Method!'}, status=400)








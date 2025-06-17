from contextlib import nullcontext

from django import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model # replaced default user with Custom user

from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.core import forms
from apps.core.forms import ClientForm, AddressForm, ContactForm, AccountForm, SpecialistForm
from apps.core.models import Client, Contact, Service, Speciality, Specialist, Appointment
from apps.core.models.client import Gender
from django.contrib import messages

from datetime import datetime


# Create your views here.

# Можемо реалізовувати методи, які будуть реагувати на певну адресу

def hello(request): # Один параметр `request`, що прийматиме запити від браузера
    # return HttpResponse("Hello World!", content_type='text/plain')
    return HttpResponse("<h1>Hello World!</h1>", content_type='text/html')

def about_project(request):
    return render(request, 'about_project.html') # render - повертає html-сторінку

# SECURITY 1
# @login_required
def about_core(request):
    return render(request, 'core/about_core.html')

@require_http_methods(['GET', 'POST'])
def clients(request):
    # POST
    if request.method == 'POST':
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
# class ClientDetailUpdateView(LoginRequiredMixin, views.View):
class ClientDetailUpdateView(views.View):
    def get(self, request, pk): # parameter `request` given to make running it as `get`

        # Спроба отримати клієнта, або помилка
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        # contact_list = getattr(client, 'contacts', None).all()
        contacts_qs = client.contacts.all()
        # print(f"contacts_qs:{contacts_qs}")
        accounts = client.accounts.all()

        # print(client)
        # Створення об'єкта форми, з даними client
        client_form = ClientForm(instance=client, prefix='client') #client-surname
        address_form = AddressForm(instance=address, prefix='address')
        # contact_form_list = [ContactForm(instance=contact, prefix=str(i)) for i, contact in enumerate(contacts_qs)]  # Creating list generator
        contact_form_list = [
            ContactForm(instance=contact, prefix=f'contact_{i}')
            for i, contact in enumerate(contacts_qs)
        ]
        contact_form = ContactForm(prefix='contact')
        account_form_list = [
            AccountForm(instance=account, prefix=f'accocunt_{i}')
            for i, account in enumerate(accounts)
        ]
        account_form = AccountForm(prefix='account')

        # Передача форми на сторінку
        context={
            'client_form': client_form,
            'address_form': address_form,
            'client': client, # Transferring `client` to the page
            'contact_form_list': contact_form_list,
            # 'contact_form_list': contacts_qs,
            'contact_form': contact_form,

            'account_form': account_form,
            'account_form_list': account_form_list,
            'contact_list': contacts_qs,
            'account_list': accounts,
        }
        return render(request, 'core/pages/client_details.html', context)

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)


        # Check if delete button for client was pressed
        if 'delete_client' in request.POST:
            if client.address:
                client.address.delete()  # Deleting addresses related with Client
            contact_list = client.contacts.all() # Getting list of all contacts, related with our Client
            if len(contact_list)!=0: # Checking if we have any contacts related with our Client
                contact_list.delete() # Deleting all Client contacts
            client.delete()
            return redirect('core:clients')  # redirect to clients list or elsewhere

        if 'delete_address' in request.POST:
            if client.address:
                address.delete()
            return redirect('core:client_detail', pk=pk)


        # Для отримання файлу з форми!!!
        client_form = ClientForm(request.POST, request.FILES, instance=client, prefix='client')   # механізм instance дозволяє дістати поля, які не видимі в формі, щоб коректно зберегти дані згодом
        address_form = AddressForm(request.POST, instance=address, prefix='address')
        # contact_form = ContactForm(request.POST, instance = contacts, prefix='contacts' )

        if 'submit_client' in request.POST:
            form = ClientForm(request.POST, request.FILES, instance=client, prefix='client')
            if form.is_valid():
                print(request.POST)
                # Check if the clear checkbox was checked
                print(form.cleaned_data.get('client-photo-clear'))
                if request.POST.get('client-photo-clear'):
                    print("Inside `client-photo-clear`")
                    print(request.POST.get('photo'))
                    #Photo already empty in form
                    # if client.photo:
                        # client.photo.delete(save=False)
                    client.photo.delete()
                    client.photo = None
                # Save form and client
                form.save()
                client.save()
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(form.errors)

# https://stackoverflow.com/questions/11456410/image-file-not-deleted-when-object-with-imagefield-field-is-deleted
# EXPLANATION:
# Deletion of files associated with FileFields and ImageFields was intentionally removed in Django 1.3.See ticket  # 6456. Django uses transactions extensively to prevent data corruption if something goes wrong with the request. If a deletion transaction is rolled-backed, after the file has been deleted from the filesystem, then you now have a record pointing to a non-existent file. All tickets asking for automatic deletion to return have been summarily marked "Won't Fix", so this is not going to change.
# So we will leave like it is.

        # # Trying to delete image properly from database
        # if 'submit_client' in request.POST:  # Обираємо наш `submit` в post запиті
        #     form = ClientForm(request.POST, request.FILES, instance=client, prefix='client')
        #     if form.is_valid():
        #         # Check if the clear checkbox was checked
        #         # print("Form is valid")
        #         # print(form)
        #         # if form.cleaned_data.get('client-photo-clear'):
        #         print(f"form.cleaned_data:{form.cleaned_data['photo']}")
        #
        #         # if form.cleaned_data.get('client-photo-clear'):
        #         if not form.cleaned_data['photo']:
        #             print("Deleting photo from form.")
        #             # Delete the existing photo file
        #             if client.photo:
        #                 # client.photo.delete(save=False)
        #                 print("Let's delete photo")
        #                 form.cleaned_data['photo'].delete()
        #                 # client.photo.delete()
        #                 print(client.photo)
        #             client.photo = None
        #         form.save()
        #         client.save() # Saving changes in database
        #         # Redirect or respond accordingly
        #         return redirect('core:client_detail', pk=client.pk)
        #     else:
        #         print(client_form.errors)


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
                # contact = contact_form.save(commit=False)  # We are not saving directly in database jet
                # n_contact = Contact(contact_form.cleaned_data['contact_type'], contact_form.cleaned_data['contact_value'])
                n_contact = contact_form.save()
                client.contacts.add(n_contact)
                # print(n_contact)
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(contact_form.errors)

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


        # Accounts
        elif 'submit_account' in request.POST:  # form for simple adding account
            account_form = AccountForm(request.POST, prefix='account')
            if account_form.is_valid():
                n_account = account_form.save()
                client.accounts.add(n_account)
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(address_form.errors)

        # Deleting `account`
        elif 'submit_account_delete' in request.POST:
            # print("Delete account pressed")
            prefix=request.POST.get('submit_account_delete')
            # Let's extract numeric part from prefix
            index_str = prefix.split('_')[-1]  # '0' as an example
            index = int(index_str)
            print(f"our prefix for deleting: {index}")
            account_list = client.accounts.all() # Getting from database list of contacts
            try:
                account_del=account_list[index]
            except (IndexError, ValueError) as e:
                print(f"An exception occurred: {type(e).__name__}: {e}") # Getting information about our error
                return redirect('core:client_detail', pk=client.pk)
            account_del.delete() # Let's delete mentioned contact
            return redirect('core:client_detail', pk=client.pk)

        elif 'submit_account_update' in request.POST:
            account_list = client.accounts.all()
            prefix = request.POST.get('submit_account_update')
            index = int(prefix.split('_')[-1])  # getting last number from the prefix (id in our account table for mentioned Client)
            # Fetch the existing account
            existing_account = account_list[index]
            # Bind the form to the existing instance
            account_form = AccountForm(request.POST, prefix=prefix, instance=existing_account)

            if account_form.is_valid():
                account_form.save()
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

        return render(request, 'core/pages/client_details.html', context)


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


def welcome(request):
    return render(request, 'core/pages/welcome.html')


class RegisterView(views.View):
    pass


@require_http_methods(['GET', 'POST'])
def services(request):
    # POST
    if request.method == 'POST':
        service_title = request.POST.get('service_title')
        service_description = request.POST.get('service_description')
        service_price = request.POST.get('service_price')

        # Case when we are adding new object
        if 'submit_service_create' in request.POST:
            Service.objects.create(
                service_title=service_title,
                service_description=service_description,
                service_price=service_price,
            )
            return redirect('core:services')

        # If pressed `update_button`
        if 'submit_service_update' in request.POST:
            print(f"Update pressed.")
            service_id = request.POST.get('submit_service_update')
            # Fetch and update the specific service
            service = Service.objects.get(id=service_id)
            service.service_title = request.POST.get('service_title')
            service.service_description = request.POST.get('service_description')
            service.service_price = request.POST.get('service_price')
            service.save()
            return redirect('core:services')

        # If pressed `update_button`
        if 'submit_service_delete' in request.POST:
            print(f"Delete pressed.")
            service_id = request.POST.get('submit_service_delete')
            Service.objects.get(id=service_id).delete()
            return redirect('core:services')

    # GET
    context = {
        'service_form_list': Service.objects.all(),
    }
    return render(request, 'core/pages/services.html', context)

require_http_methods(['GET', 'POST'])
def specialities(request):
    # POST
    if request.method == 'POST':
        speciality_name = request.POST.get('speciality_name')

        # Case when we are adding new object
        if 'submit_speciality_create' in request.POST:
            print(f"Creating new speciality")
            Speciality.objects.create(
                speciality_name=speciality_name,
            )
            return redirect('core:specialities')

        # If pressed `update_button`
        if 'submit_speciality_update' in request.POST:
            print(f"Update pressed.")
            speciality_id = request.POST.get('submit_speciality_update')
            # Fetch and update the specific speciality
            speciality = Service.objects.get(id=speciality_id)
            speciality.speciality_name = request.POST.get('speciality_name')
            speciality.save()
            return redirect('core:specialities')

        # If pressed `update_button`
        if 'submit_speciality_delete' in request.POST:
            print(f"Delete pressed.")
            speciality_id = request.POST.get('submit_speciality_delete')
            Speciality.objects.get(id=speciality_id).delete()
            return redirect('core:speciality')

    # GET
    context = {
        'speciality_form_list': Speciality.objects.all(),
    }
    return render(request, 'core/pages/specialities.html', context)


# Specialists
@require_http_methods(['GET', 'POST'])
def specialists(request):
    # POST
    if request.method == 'POST':
        surname =  request.POST.get('surname')
        name = request.POST.get('name')
        patronymic = request.POST.get('patronymic')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')


        Specialist.objects.create(
            surname = surname,
            name = name,
            patronymic = patronymic,
            email = email,
            birthday = birthday,
            gender = gender
        )

        return redirect('core:specialists')


    # GET
    context = {
        'specialist_list': Specialist.objects.all(),
        'gender_choices': Gender,
    }
    return render(request, 'core/pages/specialists.html', context) #


# Specialists details
# class SpecialistDetailUpdateView(LoginRequiredMixin, views.View):
class SpecialistDetailUpdateView(views.View):
    def get(self, request, pk): # parameter `request` given to make running it as `get`

        # Спроба отримати спеціаліста, або помилка
        specialist = get_object_or_404(Specialist, pk=pk)
        contacts_qs = specialist.contacts.all()

        print(f"specialist:{specialist}")
        # Створення об'єкта форми, з даними specialist
        specialist_form = SpecialistForm(instance=specialist, prefix='specialist') #specialist-surname
        # contact_form_list = [ContactForm(instance=contact, prefix=str(i)) for i, contact in enumerate(contacts_qs)]  # Creating list generator
        contact_form_list = [
            ContactForm(instance=contact, prefix=f'contact_{i}')
            for i, contact in enumerate(contacts_qs)
        ]
        contact_form = ContactForm(prefix='contact')

        # Передача форми на сторінку
        context={
            'specialist_form': specialist_form,
            'specialist': specialist, # Transferring `specialist` to the page
            'contact_form_list': contact_form_list,
            # 'contact_form_list': contacts_qs,
            'contact_form': contact_form,


            'contact_list': contacts_qs,
        }
        return render(request, 'core/pages/specialist_details.html', context)

    def post(self, request, pk):
        specialist = get_object_or_404(Specialist, pk=pk)


        # Check if delete button for specialist was pressed
        if 'delete_specialist' in request.POST:
            contact_list = specialist.contacts.all() # Getting list of all contacts, related with our Client
            if len(contact_list)!=0: # Checking if we have any contacts related with our Client
                contact_list.delete() # Deleting all Client contacts
            specialist.delete()
            return redirect('core:specialists')  # redirect to specialists list or elsewhere


        # Для отримання файлу з форми!!!
        specialist_form = SpecialistForm(request.POST, request.FILES, instance=specialist, prefix='specialist')   # механізм instance дозволяє дістати поля, які не видимі в формі, щоб коректно зберегти дані згодом
        # contact_form = ContactForm(request.POST, instance = contacts, prefix='contacts' )

        if 'submit_specialist' in request.POST:
            form = SpecialistForm(request.POST, request.FILES, instance=specialist, prefix='specialist')
            if form.is_valid():
                print(request.POST)
                # Check if the clear checkbox was checked
                print(form.cleaned_data.get('specialist-photo-clear'))
                if request.POST.get('specialist-photo-clear'):
                    print("Inside `specialist-photo-clear`")
                    print(request.POST.get('photo'))
                    #Photo already empty in form
                    # if specialist.photo:
                        # specialist.photo.delete(save=False)
                    specialist.photo.delete()
                    specialist.photo = None
                # Save form and specialist
                form.save()
                specialist.save()
                return redirect('core:specialist_details', pk=specialist.pk)
            else:
                print(form.errors)

        elif 'submit_contact' in request.POST:  # form for simple adding contact
            contact_form = ContactForm(request.POST, prefix='contact')
            if contact_form.is_valid():
                # contact = contact_form.save(commit=False)  # We are not saving directly in database jet
                # n_contact = Contact(contact_form.cleaned_data['contact_type'], contact_form.cleaned_data['contact_value'])
                n_contact = contact_form.save()
                specialist.contacts.add(n_contact)
                # print(n_contact)
                return redirect('core:specialist_details', pk=specialist.pk)
            else:
                print(contact_form.errors)

        # Deleting `contact`
        elif 'submit_contact_delete' in request.POST:
            # print("Delete contact pressed")
            prefix=request.POST.get('submit_contact_delete')
            # Let's extract numeric part from prefix
            index_str = prefix.split('_')[-1]  # '0' as an example
            index = int(index_str)
            print(f"our prefix for deleting: {index}")
            contact_list = specialist.contacts.all() # Getting from database list of contacts
            try:
                contact_del=contact_list[index]
            except (IndexError, ValueError) as e:
                print(f"An exception occurred: {type(e).__name__}: {e}") # Getting information about our error
                return redirect('core:specialist_details', pk=specialist.pk)
            contact_del.delete() # Let's delete mentioned contact
            return redirect('core:specialist_details', pk=specialist.pk)

        elif 'submit_contact_update' in request.POST:
            contact_list = specialist.contacts.all()
            prefix = request.POST.get('submit_contact_update')
            index = int(prefix.split('_')[-1])  # getting last number from the prefix (id in our contact table for mentioned Client)
            # Fetch the existing contact
            existing_contact = contact_list[index]
            # Bind the form to the existing instance
            contact_form = ContactForm(request.POST, prefix=prefix, instance=existing_contact)

            if contact_form.is_valid():
                contact_form.save()
                return redirect('core:specialist_details', pk=specialist.pk)
            else:
                print("Errors occurs while trying to save updated contact.")
                return redirect('core:specialist_details', pk=specialist.pk)
        else:
            print("Errors occurs while trying to save updated contact.")
            return redirect('core:specialist_details', pk=specialist.pk)

        # Рендер у випадку помилки, залишаємо дані, введені у форму
        context = {
            'specialist_form': specialist_form,
            'specialist': specialist,
        }

        return render(request, 'core/pages/specialist_details.html', context)


# Appointments
@require_http_methods(['GET', 'POST'])
def appointments(request):
    services = Service.objects.all()
    clients = Client.objects.all()
    specialists = Specialist.objects.all()
    appointments = Appointment.objects.all()

    # POST
    if request.method == 'POST':
        # # service = request.POST.get('service')
        # # time_from = request.POST.get('time_from')
        # # time_till = request.POST.get('time_till')
        #
        # time_from_str = request.POST.get('time_from')
        # time_till_str = request.POST.get('time_till')
        #
        # time_from_dt = datetime.strptime(time_from_str, '%Y-%m-%dT%H:%M')
        # time_till_dt = datetime.strptime(time_till_str, '%Y-%m-%dT%H:%M')
        #
        # appointment_details = request.POST.get('appointment_details')
        # # price = request.POST.get('price')
        # price = float(request.POST.get('price', 0))
        # is_completed = request.POST.get('is_completed')
        # # client = request.POST.get('client')
        # # specialist = request.POST.get('specialist')
        #
        # service_id = request.POST.get('service')
        # service_obj = Service.objects.get(id=service_id)
        # client_id = request.POST.get('client')
        # client_obj = Client.objects.get(id=client_id)
        # specialist_id = request.POST.get('specialist')
        # specialist_obj = Specialist.objects.get(id=specialist_id)




        # Case when we are adding new object
        # if 'submit_appointment_create' in request.POST:
        #     Appointment.objects.create(
        #         # service=service,
        #         # time_from=time_from,
        #         # time_till=time_till,
        #         appointment_details=appointment_details,
        #         price=price,
        #         is_completed=is_completed,
        #         # client=client,
        #         # specialist=specialist,
        #         service = service_obj,
        #         client = client_obj,
        #         specialist = specialist_obj,
        #         time_from = time_from_dt,
        #         time_till = time_till_dt,
        #     )
        #     print('We are creating new appointment')
        #     return redirect('core:appointments')
        if 'submit_appointment_create' in request.POST:
            service_id = request.POST.get('service')
            client_id = request.POST.get('client')
            specialist_id = request.POST.get('specialist')

            service_obj = Service.objects.get(id=service_id)
            client_obj = Client.objects.get(id=client_id)
            specialist_obj = Specialist.objects.get(id=specialist_id)

            time_from_str = request.POST.get('time_from')
            time_till_str = request.POST.get('time_till')
            time_from_dt = datetime.strptime(time_from_str, '%Y-%m-%dT%H:%M')
            time_till_dt = datetime.strptime(time_till_str, '%Y-%m-%dT%H:%M')

            price_value = float(request.POST.get('price', 0))
            appointment_details = request.POST.get('appointment_details')
            is_completed = False  # default or based on a checkbox

            Appointment.objects.create(
                service=service_obj,
                time_from=time_from_dt,
                time_till=time_till_dt,
                appointment_details=appointment_details,
                price=price_value,
                is_completed=is_completed,
                client=client_obj,
                specialist=specialist_obj,
            )
            return redirect('core:appointments')

    context = {
        'services': services,
        'clients': clients,
        'specialists': specialists,
        'appointments': appointments,
    }
    return render(request, 'core/pages/appointments.html', context)



@require_http_methods(['GET', 'POST'])
def admin_appointments(request):
    services = Service.objects.all()
    clients = Client.objects.all()
    specialists = Specialist.objects.all()
    appointments = Appointment.objects.all()

    # POST
    if request.method == 'POST':

        if 'submit_appointment_create' in request.POST:
            service_id = request.POST.get('service')
            client_id = request.POST.get('client')
            specialist_id = request.POST.get('specialist')

            service_obj = Service.objects.get(id=service_id)
            client_obj = Client.objects.get(id=client_id)
            specialist_obj = Specialist.objects.get(id=specialist_id)

            time_from_str = request.POST.get('time_from')
            time_till_str = request.POST.get('time_till')
            time_from_dt = datetime.strptime(time_from_str, '%Y-%m-%dT%H:%M')
            time_till_dt = datetime.strptime(time_till_str, '%Y-%m-%dT%H:%M')

            price_value = float(request.POST.get('price', 0))
            appointment_details = request.POST.get('appointment_details')
            is_completed = False  # default or based on a checkbox

            Appointment.objects.create(
                service=service_obj,
                time_from=time_from_dt,
                time_till=time_till_dt,
                appointment_details=appointment_details,
                price=price_value,
                is_completed=is_completed,
                client=client_obj,
                specialist=specialist_obj,
            )
            return redirect('core:admin_appointments')

        # If pressed `update_button`
        if 'submit_appointment_update' in request.POST:
            appointment_id = request.POST.get('submit_appointment_update')
            appointment = Appointment.objects.get(id=appointment_id)
            # Fetch and set service
            service_id = request.POST.get('service')
            appointment.service = Service.objects.get(id=service_id)
            # Update date fields - parse from string
            time_from_str = request.POST.get('time_from')
            time_till_str = request.POST.get('time_till')
            appointment.is_completed = 'is_completed' in request.POST
            if time_from_str:
                appointment.time_from = datetime.strptime(time_from_str, '%Y-%m-%dT%H:%M')
            if time_till_str:
                appointment.time_till = datetime.strptime(time_till_str, '%Y-%m-%dT%H:%M')
            # Other fields
            appointment.appointment_details = request.POST.get('appointment_details')
            appointment.price = float(request.POST.get('price', 0))
            # Update foreign keys
            client_id = request.POST.get('client')
            specialist_id = request.POST.get('specialist')
            appointment.client = Client.objects.get(id=client_id)
            appointment.specialist = Specialist.objects.get(id=specialist_id)
            # Save changes
            appointment.save()
            return redirect('core:admin_appointments')

        # If pressed `delete_button`
        if 'submit_appointment_delete' in request.POST:
            print(f"Delete pressed.")
            appointment_id = request.POST.get('submit_appointment_delete')
            Appointment.objects.get(id=appointment_id).delete()
            return redirect('core:admin_appointments')

    context = {
        'services': services,
        'clients': clients,
        'specialists': specialists,
        'appointments': appointments,
    }
    return render(request, 'core/pages/admin_appointments.html', context)


# Users
User = get_user_model()
@require_http_methods(['GET', 'POST'])
def user_management(request):
    if request.method == 'POST':
        # Handle user update
        if 'update_user' in request.POST:
            user_id = request.POST.get('update_user')
            user = get_object_or_404(User, id=user_id)
            user.username = request.POST.get(f'username_{user_id}')
            user.email = request.POST.get(f'email_{user_id}')
            role = request.POST.get(f'role_{user_id}')
            # Assign role to user's 'role' field
            user.role = role
            user.save()
            messages.success(request, f'User {user.username} updated.')
            return redirect('core:user_management')

        # Handle user deletion
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('delete_user')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, f'User {user.username} deleted.')
            return redirect('core:user_management')

        # Handle adding new user
        elif 'add_user' in request.POST:
            username = request.POST.get('new_username')
            email = request.POST.get('new_email')
            password = request.POST.get('new_password')
            role = request.POST.get('new_role')
            if username and email and password:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.role = role
                user.save()
                messages.success(request, f'User {username} added.')
            else:
                messages.error(request, 'Please fill all fields to add a new user.')
            return redirect('core:user_management')

    users = User.objects.all()
    return render(request, 'registration/users.html', {'users': users})
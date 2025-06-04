from django import forms

from apps.core.models import Client, Address, Contact, Account, Service, Specialist, Appointment


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        # Вибрані поля
        # fields=['surname', 'name', 'email']
        # Всі поля
        fields = '__all__'
        # exclude - виключає поля
        exclude=['created_at', 'updated_at', 'address', 'accounts', 'contacts']
        # Налаштування полів
        widgets={
            'surname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Surname'}),
            'birthday': forms.DateInput(attrs={'type':'date', 'class':'form-control'}, format='%Y-%m-%d'), # form-control це класс з bootstrap
            # 'photo': forms.ClearableFileInput(attrs={'initial': True}),
            'photo': forms.ClearableFileInput(attrs={'multiple': False}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        # exclude = 'created_at', 'updated_at' #not in our case

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        # exclude = ['created_at', 'updated_at', 'client '] # not applicable for our case as we don't have such fields

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

class SpecialistForm(forms.ModelForm):
    class Meta:
        model = Specialist
        # Всі поля
        fields = '__all__'
        # exclude - виключає поля
        exclude=['created_at', 'updated_at', 'address', 'contacts', 'clients']
        # Налаштування полів
        widgets={
            'surname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Surname'}),
            'birthday': forms.DateInput(attrs={'type':'date', 'class':'form-control'}, format='%Y-%m-%d'), # form-control це класс з bootstrap
            'photo': forms.ClearableFileInput(attrs={'multiple': False}),
        }


 # id = models.BigAutoField(primary_key=True)  # BigAutoField for large amount of `id`s
 #    time_from = models.DateTimeField() # Date and time of beginning of visit
 #    time_till = models.DateTimeField() # Date and time of end of visit
 #    appointment_details = models.CharField(max_length=300) # Provided service
 #    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
 #    is_completed = models.BooleanField(False)  # Field to know if appointment passed and service completed
 #
 #    client = models.ForeignKey('Client', on_delete=models.CASCADE)
 #    specialist = models.ForeignKey('Specialist', on_delete=models.CASCADE)
 #    service = models.ForeignKey('Service', on_delete=models.CASCADE)



# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         # Всі поля
#         fields = '__all__'
#         # exclude - виключає поля
#         # exclude=['']
#         # Налаштування полів
#         widgets={
#             'time_from': forms.DateInput(attrs={'type':'date', 'class':'form-control'}, format='%Y-%m-%d'),
#             'time_till': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
#             'appointment_details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '{{appointment_details}}'}),
#         }

from django import forms

from apps.core.models import Client, Address, Contact, Account, Service


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



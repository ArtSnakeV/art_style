from django import forms

from apps.core.models import Client, Address, Contact


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
            'birthday': forms.DateInput(attrs={'type':'date', 'class':'form-control'}, format='%Y-%m-%d') # form-control це класс з bootstrap
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



# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = '__all__'
#         widgets = {
#             'contact_type': forms.Select(attrs={'class': 'form-control'}),
#             'contact_value': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'contact_type': 'Type of Contact',
#             'contact_value': 'Contact Details',
#         }
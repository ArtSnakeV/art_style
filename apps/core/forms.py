from django import forms

from apps.core.models import Client


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
            'birthday': forms.DateInput(attrs={'type':'date', 'class':'form-control'}, format='%Y-%m-%d') # form-control це класс з bootstrap
        }
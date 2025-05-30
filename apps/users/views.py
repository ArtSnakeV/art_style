from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from apps.users.forms import CustomUserCreationForm


# Create your views here.
class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

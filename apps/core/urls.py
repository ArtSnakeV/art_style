from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView

from apps.core import views
from apps.core.views import hello, about_project, about_core


# Оголошення простору імен namespace
app_name = 'core'



urlpatterns = [
    # # path('', hello), #  View `hello` will run while we come to the main page of our website
    # path('', about_project),
    # path('core/', about_core),
    # # about-core адреса має писатись в стилі kebab-case
    # path('about-core/', about_core),
    # # Приклад використання вкладеної адреси
    # path('about/core/', about_core),

    path('about/', about_project, name='about_project'),

    path('about/core/', about_core),

    # path('', RedirectView.as_view(pattern_name='core:clients', permanent=False)),
    path('', RedirectView.as_view(pattern_name='core:appointments', permanent=False)),

    # path('clients/', login_required(views.clients), name='clients'), # core:clients
    path('clients/', views.clients, name='clients'),  # core:clients

    path('clients/<int:pk>/', views.ClientDetailUpdateView.as_view(), name='client_detail'), # pk - primary key

    path('clients/<int:pk>/address-form', views.address_form, name='address_form'),
    path('welcome/', views.welcome, name='welcome'),
    # path('users/', views.RegisterView.as_view(), name='accounts/users'), # Тимчасово перекидаємо на сторінку реєстрації
    # path('users/', views.users, name='users'), # Тимчасово перекидаємо на сторінку реєстрації
    path('users/', views.user_management, name='user_management'),

    path('services/', views.services, name='services'),

    path('specialities/', views.specialities, name='specialities'),


    path('specialists/', views.specialists, name='specialists'),
    path('specialists/<int:pk>/', views.SpecialistDetailUpdateView.as_view(), name='specialist_details'), # pk - primary key

    path('appointments/', views.appointments, name='appointments'),
    path('admin_appointments/', views.admin_appointments, name='admin_appointments')
]

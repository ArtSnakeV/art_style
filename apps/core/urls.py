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

    path('about/', about_project),
    path('about/core/', about_core),

    path('', RedirectView.as_view(pattern_name='core:clients', permanent=False)),
    path('clients/', views.clients, name='clients'), # core:clients
    path('clients/<int:pk>/', views.ClientDetailUpdateView.as_view(), name='client_detail'), # pk - primary key
    
]

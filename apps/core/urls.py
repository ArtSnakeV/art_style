from django.urls import path

from apps.core.views import hello

urlpatterns = [
    path('', hello), #  View `hello` will run while we come to the main page of our website
]
from django.urls import path
from django.contrib.auth import views as auth_views

from apps.core.views import about_project
from apps.users import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('about/', about_project, name='about_project'),
]
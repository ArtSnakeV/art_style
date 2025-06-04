from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('user', 'User'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    ]
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_worker = False # Field to know if our User is Specialist, Client by default
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')


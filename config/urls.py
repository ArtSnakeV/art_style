"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Added imports below:
from django.conf import settings
from django.conf.urls.static import static

from apps.core import views

urlpatterns = [
    # http://localhost:8000/admin/
    path('admin/', admin.site.urls),
    # '' http:// localhost:8000/   - root-адреса
    path('', include('apps.core.urls')), # Перший параметр - адреса, по якій ми переходимо (якщо пусті лапки, то це root адреса проєкту
                # на сторінку, другий - View, який обробляє сторінку,
                # також тут може бути псевдонім, який обробляє сторінку

    path('accounts/', include('apps.users.urls')), # Префікс адреси accounts/ для додатку users
    path('welcome/', views.welcome, name='welcome'),
]

#!!!!! MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# pip install Pillow
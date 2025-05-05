from django.apps import AppConfig

# !!! apps.core назва додатку
# підключаємо також в config/settings
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

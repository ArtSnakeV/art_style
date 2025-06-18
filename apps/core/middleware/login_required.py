from django.shortcuts import redirect
from django.urls import resolve

from config import settings

EXEMPT_URLS = [
    'login',
    'logout',
    'register',
    'core:welcome',
    # 'admin:login',
    # 'admin:logout',
    # 'admin:index',
    # 'admin:appointments',
    # 'user:admin_appointments',
    # 'user:services',
    # 'user:specialist_details',
    # 'core:about_project',
    # 'worker:clients',
    # 'worker:client_detail',
    # 'worker:services',
    # 'worker:specialists',
    # 'worker:admin_appointments',
    # 'core:welcome',
]


#Pages protection
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        resolver_match = resolve(request.path)
        # view_name включає namespace
        view_name = resolver_match.view_name

        if view_name in EXEMPT_URLS: # Перевіряємо, чи користувач аутентифікований
            return self.get_response(request) # Продовжуємо запит до view

        if not request.user.is_authenticated: # Якщо ми не авторизовані
            return redirect(f'{settings.LOGIN_URL}?next={request.path}') # Основна сторінка переходу: LOGIN_URL, далі сторінка після успішнох авторизації

        return self.get_response(request)

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
          # Proceed only if user is authenticated
        if request.user.is_authenticated:
            try:
                resolver_match = resolve(request.path)
                view_name = resolver_match.view_name  # e.g., 'namespace:viewname'
                url_name = resolver_match.url_name  # e.g., 'clients'
            except:
                # If resolve fails, proceed
                 return self.get_response(request)

            user_role = getattr(request.user, 'role', None)

            # Admin can access any page
            if user_role == 'admin':
                 return self.get_response(request)

            # Non-admin role restrictions
            if user_role != 'admin':
            # Restrict access based on URL name
                if view_name and 'admin' in view_name:
                    return redirect('core:appointments')  # or other page

                # Role-based page access
                if url_name == 'clients' and user_role != 'worker':
                    return self.get_response(request)
                if url_name == 'service' and user_role != 'admin':
                    return self.get_response(request)
                if url_name == 'specialist' and user_role != 'admin':
                    return self.get_response(request)
                if url_name == 'address' and user_role != 'admin':
                   return self.get_response(request)

                # Guest role handling
                if user_role == 'guest':
                    if view_name in ['core:welcome', 'core:about', 'core:register']:
                        return self.get_response(request)
                    return redirect('core:about_project')

        return self.get_response(request)




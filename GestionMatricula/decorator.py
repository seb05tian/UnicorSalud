from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

# Decorador para verificar si el usuario tiene un rol específico
def role_required(allowed_roles=[]):    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print(request.user.rol)
            # Primero: verificar si está autenticado
            if not request.user.is_authenticated:
                messages.error(request, "Debes iniciar sesión para acceder.")
                return redirect('login')

            # Segundo: validar que el rol exista en los permitidos
            if request.user.rol.lower() not in [role.lower() for role in allowed_roles]:
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return redirect('no_autorizado')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
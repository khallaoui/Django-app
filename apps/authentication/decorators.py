from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def role_required(*roles):
    """
    Décorateur pour restreindre l'accès aux vues selon les rôles.
    
    Usage:
        @role_required('admin', 'gestionnaire')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, 
                    'Vous n\'avez pas les permissions nécessaires pour accéder à cette page.'
                )
                return redirect('stock_debord:dashboard')
        return wrapper
    return decorator

def consultant_required(view_func):
    """Décorateur pour les vues accessibles aux consultants (opérateurs/caristes)"""
    return role_required('consultant', 'gestionnaire', 'admin')(view_func)

def gestionnaire_required(view_func):
    """Décorateur pour les vues accessibles aux gestionnaires et administrateurs"""
    return role_required('gestionnaire', 'admin')(view_func)

def admin_required(view_func):
    """Décorateur pour les vues accessibles uniquement aux administrateurs"""
    return role_required('admin')(view_func)

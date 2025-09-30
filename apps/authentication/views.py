from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CustomUserCreationForm
from .models import CustomUser
from .decorators import admin_required
from .permissions import UserPermissions

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}!')
            return redirect('auth:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@admin_required
def user_list_view(request):
    """Liste tous les utilisateurs - Accessible uniquement aux administrateurs"""
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    
    users = CustomUser.objects.all().order_by('-created_at')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Calculer les statistiques par rôle (sur tous les utilisateurs, pas juste les filtrés)
    total_users = CustomUser.objects.count()
    consultants_count = CustomUser.objects.filter(role='consultant').count()
    gestionnaires_count = CustomUser.objects.filter(role='gestionnaire').count()
    admins_count = CustomUser.objects.filter(role='admin').count()
    
    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': CustomUser.ROLE_CHOICES,
        'total_users': total_users,
        'consultants_count': consultants_count,
        'gestionnaires_count': gestionnaires_count,
        'admins_count': admins_count,
    }
    return render(request, 'authentication/user_list.html', context)

@admin_required
def user_create_view(request):
    """Créer un nouvel utilisateur - Accessible uniquement aux administrateurs"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Utilisateur {user.username} créé avec succès!')
            return redirect('auth:user_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/user_form.html', {
        'form': form,
        'title': 'Créer un utilisateur',
        'action': 'create'
    })

@admin_required
def user_edit_view(request, user_id):
    """Modifier un utilisateur - Accessible uniquement aux administrateurs"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        # Mise à jour des informations de l'utilisateur
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.role = request.POST.get('role', user.role)
        user.phone = request.POST.get('phone', user.phone)
        user.is_active = request.POST.get('is_active') == 'on'
        
        try:
            user.save()
            messages.success(request, f'Utilisateur {user.username} modifié avec succès!')
            return redirect('auth:user_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification: {str(e)}')
    
    return render(request, 'authentication/user_edit.html', {
        'user_obj': user,
        'role_choices': CustomUser.ROLE_CHOICES,
    })

@admin_required
def user_delete_view(request, user_id):
    """Supprimer un utilisateur - Accessible uniquement aux administrateurs"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Empêcher la suppression de son propre compte
    if user.id == request.user.id:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte!')
        return redirect('auth:user_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Utilisateur {username} supprimé avec succès!')
        return redirect('auth:user_list')
    
    return render(request, 'authentication/user_confirm_delete.html', {
        'user_obj': user,
    })

@login_required
def profile_view(request):
    """Profil de l'utilisateur connecté"""
    return render(request, 'authentication/profile.html', {
        'user': request.user,
    })

@login_required
def change_password_view(request):
    """Changer le mot de passe de l'utilisateur connecté"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour ne pas déconnecter l'utilisateur
            messages.success(request, 'Votre mot de passe a été modifié avec succès!')
            return redirect('auth:profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'authentication/change_password.html', {
        'form': form,
    })
# 🚀 Référence Rapide - Utilisateurs et Rôles

## 📝 Comptes de Test Créés

```
┌─────────────────┬──────────────┬──────────────────┬─────────────────────────────┐
│ Rôle            │ Username     │ Password         │ Email                       │
├─────────────────┼──────────────┼──────────────────┼─────────────────────────────┤
│ Consultant      │ consultant   │ consultant123    │ consultant@stellantis.com   │
│ Gestionnaire    │ gestionnaire │ gestionnaire123  │ gestionnaire@stellantis.com │
│ Administrateur  │ admin        │ admin123         │ admin@stellantis.com        │
└─────────────────┴──────────────┴──────────────────┴─────────────────────────────┘
```

## ⚡ Commandes Rapides

### Créer les utilisateurs de test
```bash
py manage.py create_users
```

### Recréer les utilisateurs (supprime et recrée)
```bash
py manage.py create_users --reset
```

### Créer un superuser Django
```bash
py manage.py createsuperuser
```

### Lancer le serveur
```bash
py manage.py runserver
```

## 🔗 URLs Essentielles

```
Connexion:              http://localhost:8000/auth/login/
Inscription:            http://localhost:8000/auth/register/
Profil:                 http://localhost:8000/auth/profile/
Gestion utilisateurs:   http://localhost:8000/auth/users/
Admin Django:           http://localhost:8000/admin/
Dashboard:              http://localhost:8000/dashboard/
```

## 🎯 Matrice des Permissions

```
Action                          Consultant  Gestionnaire  Admin
─────────────────────────────────────────────────────────────────
Consulter le stock              ✓           ✓             ✓
Entrées/Sorties                 ✓           ✓             ✓
Gérer le magasin                ✗           ✓             ✓
Valider mouvements              ✗           ✓             ✓
Consulter historique            ✗           ✓             ✓
Créer utilisateurs              ✗           ✗             ✓
Modifier utilisateurs           ✗           ✗             ✓
Supprimer utilisateurs          ✗           ✗             ✓
Admin Django                    ✗           ✗             ✓
```

## 💻 Code Snippets

### Utiliser les décorateurs
```python
from apps.authentication.decorators import (
    consultant_required,
    gestionnaire_required,
    admin_required
)

@consultant_required
def view_for_all(request):
    pass

@gestionnaire_required  
def view_for_managers(request):
    pass

@admin_required
def view_for_admins(request):
    pass
```

### Vérifier les rôles dans les templates
```django
{% if user.is_consultant %}
    <!-- Pour consultants, gestionnaires et admins -->
{% endif %}

{% if user.is_gestionnaire %}
    <!-- Pour gestionnaires et admins -->
{% endif %}

{% if user.is_admin %}
    <!-- Pour admins uniquement -->
{% endif %}
```

### Vérifier les permissions
```python
from apps.authentication.permissions import UserPermissions

if UserPermissions.can_manage_users(request.user):
    # Code pour la gestion des utilisateurs
    pass
```

## 🔐 Sécurité

### Mots de passe par défaut
⚠️ **IMPORTANT:** Changez les mots de passe par défaut en production!

### Bonnes pratiques
- Utilisez des mots de passe complexes (8+ caractères, majuscules, chiffres, symboles)
- Activez HTTPS en production
- Limitez les tentatives de connexion
- Loggez les actions sensibles
- Effectuez des backups réguliers

## 📁 Structure des Fichiers

```
apps/authentication/
├── models.py                    # Modèle CustomUser avec rôles
├── views.py                     # Vues de gestion des utilisateurs
├── forms.py                     # Formulaires
├── decorators.py                # Décorateurs de permissions
├── permissions.py               # Classe de vérification des permissions
├── urls.py                      # URLs d'authentification
├── admin.py                     # Configuration admin Django
└── management/
    └── commands/
        └── create_users.py      # Commande de création d'utilisateurs
```

## 🎨 Templates

```
templates/authentication/
├── user_list.html               # Liste des utilisateurs
├── user_form.html               # Formulaire création
├── user_edit.html               # Formulaire modification
├── user_confirm_delete.html     # Confirmation suppression
├── profile.html                 # Profil utilisateur
└── change_password.html         # Changement mot de passe
```

## 🆘 Problèmes Courants

### Impossible de se connecter
```bash
# Vérifier que l'utilisateur existe
py manage.py shell
>>> from apps.authentication.models import CustomUser
>>> CustomUser.objects.all()
```

### Recréer un utilisateur
```bash
py manage.py create_users --reset
```

### Réinitialiser le mot de passe d'un utilisateur
```bash
py manage.py shell
>>> from apps.authentication.models import CustomUser
>>> user = CustomUser.objects.get(username='consultant')
>>> user.set_password('nouveau_mot_de_passe')
>>> user.save()
```

### Promouvoir un utilisateur en admin
```bash
py manage.py shell
>>> from apps.authentication.models import CustomUser
>>> user = CustomUser.objects.get(username='mon_user')
>>> user.role = 'admin'
>>> user.is_staff = True
>>> user.is_superuser = True
>>> user.save()
```

## 📊 Statistiques et Monitoring

### Compter les utilisateurs par rôle
```python
from apps.authentication.models import CustomUser

consultants = CustomUser.objects.filter(role='consultant').count()
gestionnaires = CustomUser.objects.filter(role='gestionnaire').count()
admins = CustomUser.objects.filter(role='admin').count()
```

### Lister les utilisateurs actifs
```python
active_users = CustomUser.objects.filter(is_active=True)
```

### Dernières connexions
```python
recent_logins = CustomUser.objects.exclude(
    last_login__isnull=True
).order_by('-last_login')[:10]
```

## 📚 Documentation Complète

Pour plus de détails, consultez `GUIDE_UTILISATEURS_ROLES.md`

---

**Dernière mise à jour:** 29 septembre 2025
**Version:** 1.0

# Guide des Utilisateurs et Rôles

## 📋 Vue d'ensemble

Ce système de gestion des utilisateurs propose trois rôles différents avec des permissions spécifiques adaptées aux besoins de votre application Django.

## 👥 Les 3 Rôles

### 1. 🔵 Consultant (Opérateur / Cariste)

**Objectif:** Responsable des entrées et sorties des pièces et consultation du stock.

**Permissions:**
- ✅ Consulter le stock (Dashboard)
- ✅ Ajouter des références (Entrées de pièces)
- ✅ Effectuer les sorties de pièces
- ❌ Pas d'accès à la gestion des références
- ❌ Pas d'accès aux historiques complets
- ❌ Pas d'accès aux exports Excel
- ❌ Pas d'accès à la gestion des zones
- ❌ Pas d'accès à la gestion des utilisateurs

**Pages accessibles:**
- Dashboard (consultation du stock)
- Ajouter Référence (entrées)
- Saisie Sortie (sorties)
- Boot KIT, Cross DOCK, Map Débord, FLC, Log ext, How to use it
- Mon Profil
- Changement de mot de passe

**Cas d'usage:**
- Opérateurs de terrain
- Caristes
- Personnel d'entrepôt

---

### 2. 🟡 Gestionnaire de Magasin

**Objectif:** Assure la gestion globale du magasin et contrôle les mouvements de stock entre l'entrepreneur et le client.

**Permissions:**
- ✅ Toutes les permissions du Consultant
- ✅ Gérer le magasin (références, zones, travées)
- ✅ Valider et assurer les mouvements d'entrées/sorties
- ✅ Superviser les opérations
- ✅ Consulter l'historique complet des mouvements
- ✅ Exporter les données en Excel
- ✅ Extraire les mouvements de stock
- ✅ Imprimer les rapports de stock
- ✅ Modifier et supprimer des références
- ❌ Pas d'accès à la gestion des utilisateurs

**Pages accessibles:**
- Toutes les pages du Consultant +
- Gestion des références (modifier/supprimer)
- Historique complet des mouvements
- Extraction des mouvements
- Exports Excel
- Gestion des zones/travées
- Impression des rapports

**Cas d'usage:**
- Responsables d'entrepôt
- Superviseurs de stock
- Gestionnaires logistiques
- Contrôleurs de flux entre entrepreneur et client

---

### 3. 🔴 Administrateur

**Objectif:** Responsable de la gestion des utilisateurs et du suivi des activités.

**Permissions:**
- ✅ Toutes les permissions du Gestionnaire
- ✅ Créer des comptes utilisateurs
- ✅ Modifier les comptes utilisateurs
- ✅ Supprimer des comptes utilisateurs
- ✅ Consulter l'historique complet des mouvements
- ✅ Accès aux paramètres système
- ✅ Accès à l'interface d'administration Django

**Cas d'usage:**
- Administrateurs système
- Directeurs IT
- Responsables de plateforme

---

## 🚀 Démarrage Rapide

### 1. Créer les utilisateurs de test

Exécutez la commande suivante pour créer automatiquement un utilisateur pour chaque rôle:

```bash
python manage.py create_users
```

Cette commande créera 3 utilisateurs:

| Rôle | Username | Password | Email |
|------|----------|----------|-------|
| Consultant | `consultant` | `consultant123` | consultant@stellantis.com |
| Gestionnaire | `gestionnaire` | `gestionnaire123` | gestionnaire@stellantis.com |
| Administrateur | `admin` | `admin123` | admin@stellantis.com |

### 2. Réinitialiser les utilisateurs

Pour supprimer et recréer les utilisateurs de test:

```bash
python manage.py create_users --reset
```

---

## 🔐 Gestion des Utilisateurs

### Accès à la gestion (Admin uniquement)

1. Connectez-vous avec un compte administrateur
2. Accédez à: `/auth/users/`
3. Ou cliquez sur "Gestion des utilisateurs" dans le menu

### Créer un utilisateur

1. Allez dans "Gestion des utilisateurs"
2. Cliquez sur "Nouvel Utilisateur"
3. Remplissez le formulaire:
   - Nom d'utilisateur (obligatoire)
   - Email (obligatoire)
   - Rôle (obligatoire)
   - Mot de passe (obligatoire)
4. Cliquez sur "Créer l'utilisateur"

### Modifier un utilisateur

1. Dans la liste des utilisateurs
2. Cliquez sur l'icône "✏️ Modifier"
3. Modifiez les informations nécessaires
4. Cliquez sur "Enregistrer les modifications"

**Note:** Le mot de passe ne peut pas être modifié depuis cette interface. L'utilisateur doit le changer depuis son profil.

### Supprimer un utilisateur

1. Dans la liste des utilisateurs
2. Cliquez sur l'icône "🗑️ Supprimer"
3. Confirmez la suppression

**⚠️ Attention:** 
- Cette action est irréversible
- Vous ne pouvez pas supprimer votre propre compte
- Les données associées à l'utilisateur seront conservées

---

## 🔒 Utilisation des Permissions dans le Code

### Décorateurs de vue

```python
from apps.authentication.decorators import (
    consultant_required,
    gestionnaire_required, 
    admin_required,
    role_required
)

# Vue accessible aux consultants, gestionnaires et admins
@consultant_required
def view_stock(request):
    # ...
    pass

# Vue accessible aux gestionnaires et admins
@gestionnaire_required
def manage_warehouse(request):
    # ...
    pass

# Vue accessible uniquement aux admins
@admin_required
def manage_users(request):
    # ...
    pass

# Vue avec rôles personnalisés
@role_required('gestionnaire', 'admin')
def custom_view(request):
    # ...
    pass
```

### Vérification des permissions

```python
from apps.authentication.permissions import UserPermissions

# Dans une vue
def my_view(request):
    user = request.user
    
    if UserPermissions.can_view_stock(user):
        # Afficher le stock
        pass
    
    if UserPermissions.can_manage_users(user):
        # Afficher les options de gestion
        pass
```

### Dans les templates

```django
{% if user.is_consultant %}
    <!-- Contenu pour consultants -->
{% endif %}

{% if user.is_gestionnaire %}
    <!-- Contenu pour gestionnaires -->
{% endif %}

{% if user.is_admin %}
    <!-- Contenu pour administrateurs -->
{% endif %}

<!-- Vérification par rôle -->
{% if user.role == 'admin' %}
    <a href="{% url 'auth:user_list' %}">Gérer les utilisateurs</a>
{% endif %}
```

---

## 📊 Matrice des Permissions

| Action | Consultant | Gestionnaire | Admin |
|--------|:----------:|:------------:|:-----:|
| **Stock & Mouvements** | | | |
| Consulter le stock (Dashboard) | ✅ | ✅ | ✅ |
| Ajouter référence (Entrées) | ✅ | ✅ | ✅ |
| Saisie sortie de pièces | ✅ | ✅ | ✅ |
| Gérer les références | ❌ | ✅ | ✅ |
| Modifier les références | ❌ | ✅ | ✅ |
| Supprimer les références | ❌ | ✅ | ✅ |
| **Historiques & Exports** | | | |
| Consulter l'historique complet | ❌ | ✅ | ✅ |
| Exporter en Excel | ❌ | ✅ | ✅ |
| Extraction des mouvements | ❌ | ✅ | ✅ |
| Imprimer le stock | ❌ | ✅ | ✅ |
| **Gestion** | | | |
| Gérer les zones/travées | ❌ | ✅ | ✅ |
| Superviser les opérations | ❌ | ✅ | ✅ |
| **Administration** | | | |
| Créer des utilisateurs | ❌ | ❌ | ✅ |
| Modifier des utilisateurs | ❌ | ❌ | ✅ |
| Supprimer des utilisateurs | ❌ | ❌ | ✅ |
| Accès admin Django | ❌ | ❌ | ✅ |

---

## 🛠️ Configuration Avancée

### Personnaliser les rôles

Modifiez `apps/authentication/models.py`:

```python
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('consultant', 'Consultant (Opérateur / Cariste)'),
        ('gestionnaire', 'Gestionnaire de magasin'),
        ('admin', 'Administrateur'),
        # Ajoutez vos rôles personnalisés ici
        ('custom_role', 'Mon Rôle Personnalisé'),
    ]
```

### Ajouter des permissions personnalisées

Modifiez `apps/authentication/permissions.py`:

```python
class UserPermissions:
    @staticmethod
    def can_custom_action(user):
        """Permission personnalisée"""
        return user.is_authenticated and user.role in ['custom_role', 'admin']
```

---

## 🔄 Workflow Typique

### Pour un Consultant
1. Se connecter
2. Accéder au stock
3. Effectuer des entrées/sorties
4. Consulter son profil
5. Se déconnecter

### Pour un Gestionnaire
1. Se connecter
2. Superviser les opérations (mouvements entre entrepreneur et client)
3. Valider et contrôler les mouvements d'entrées/sorties
4. Consulter l'historique complet des mouvements
5. Gérer le magasin (références, zones, travées)
6. Exporter et extraire les données pour rapports
7. Se déconnecter

### Pour un Administrateur
1. Se connecter
2. Toutes les actions du Gestionnaire
3. Créer/modifier/supprimer des utilisateurs
4. Consulter les statistiques
5. Accéder à l'admin Django
6. Se déconnecter

---

## 📱 URLs Importantes

| URL | Description | Accès |
|-----|-------------|-------|
| `/auth/login/` | Page de connexion | Public |
| `/auth/register/` | Inscription | Public |
| `/auth/logout/` | Déconnexion | Connecté |
| `/auth/profile/` | Profil utilisateur | Connecté |
| `/auth/change-password/` | Changer mot de passe | Connecté |
| `/auth/users/` | Liste des utilisateurs | Admin |
| `/auth/users/create/` | Créer un utilisateur | Admin |
| `/auth/users/<id>/edit/` | Modifier un utilisateur | Admin |
| `/auth/users/<id>/delete/` | Supprimer un utilisateur | Admin |
| `/admin/` | Interface Django Admin | Admin |

---

## 🐛 Dépannage

### L'utilisateur ne peut pas se connecter
- Vérifiez que le compte est actif (is_active = True)
- Vérifiez les identifiants
- Consultez les logs Django

### Permission refusée
- Vérifiez le rôle de l'utilisateur
- Vérifiez les décorateurs de vue
- Consultez la matrice des permissions

### Impossible de créer un utilisateur
- Vérifiez que vous êtes connecté en tant qu'admin
- Vérifiez que l'username n'existe pas déjà
- Vérifiez le format de l'email

---

## 📞 Support

Pour toute question ou problème:
1. Consultez ce guide
2. Vérifiez les logs Django
3. Contactez l'équipe de développement

---

## 🔄 Changelog

### Version 1.0 (2025-09-29)
- ✅ Système de rôles à 3 niveaux
- ✅ Gestion complète des utilisateurs
- ✅ Interface d'administration
- ✅ Décorateurs de permissions
- ✅ Profils utilisateurs
- ✅ Changement de mot de passe
- ✅ Documentation complète

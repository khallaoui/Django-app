# 📍 Où Trouver les Fonctionnalités de Rôles dans l'Interface

## 🎨 Vue d'Ensemble de l'Interface

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          STELLANTIS DIZ                                    │
│                                                                            │
│  ┌──────────────────┐                                                     │
│  │  👤 admin        │                                                     │
│  │  [Administrateur]│ ← Badge de rôle avec couleur                       │
│  └──────────────────┘                                                     │
│  ─────────────────────                                                    │
│  📊 Dashboard                                                             │
│  📦 Gestion Références                                                    │
│  ➕ Ajouter Référence                                                     │
│  🕐 Historique                                                            │
│  📤 Extraction Mouvements                                                 │
│  🗺️  Gestion Zones                                                        │
│  🔧 Boot KIT                                                              │
│  🚚 Cross DOCK                                                            │
│  🗺️  Map Débord                                                           │
│  📦 FLC                                                                   │
│  📄 Log ext                                                               │
│  ❓ How to use it                                                         │
│  ─────────────────────                                                    │
│  👥 Gestion Utilisateurs  ← SEULEMENT SI ADMIN                           │
│  🛠️  Admin Django          ← SEULEMENT SI ADMIN                           │
│  ─────────────────────                                                    │
│  👤 Mon Profil            ← TOUS LES UTILISATEURS                         │
│  🔑 Mot de passe          ← TOUS LES UTILISATEURS                         │
│  🚪 Déconnexion           ← TOUS LES UTILISATEURS                         │
└────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Localisation Détaillée

### 1️⃣ **En Haut de la Sidebar** (Zone utilisateur)

```
┌──────────────────┐
│   👤              │
│   admin           │ ← Nom d'utilisateur
│ [Administrateur]  │ ← Badge rouge si Admin
│ [Gestionnaire]    │ ← Badge jaune si Gestionnaire  
│ [Consultant]      │ ← Badge bleu si Consultant
└──────────────────┘
```

**Couleurs des badges:**
- 🔴 Rouge = Administrateur
- 🟡 Jaune = Gestionnaire de magasin
- 🔵 Bleu = Consultant

### 2️⃣ **Menu Principal** (Toujours visible)

Tous les utilisateurs voient:
```
📊 Dashboard
📦 Gestion Références
➕ Ajouter Référence
🕐 Historique
📤 Extraction Mouvements
🗺️  Gestion Zones
🔧 Boot KIT
🚚 Cross DOCK
🗺️  Map Débord
📦 FLC
📄 Log ext
❓ How to use it
```

### 3️⃣ **Section Admin** (Visible UNIQUEMENT pour les Admins)

Après "How to use it", une ligne de séparation apparaît, puis:
```
─────────────────────
👥 Gestion Utilisateurs  ← Cliquez ici pour gérer les utilisateurs
🛠️  Admin Django          ← Accès à l'interface d'administration Django
─────────────────────
```

**Pour accéder:** Connectez-vous avec le compte `admin` / `admin123`

### 4️⃣ **Menu Utilisateur** (Visible pour TOUS)

En bas de la sidebar:
```
👤 Mon Profil         ← Voir vos informations et permissions
🔑 Mot de passe       ← Changer votre mot de passe
🚪 Déconnexion        ← Se déconnecter (texte en rouge)
```

## 🔍 Comment Accéder aux Fonctionnalités

### Pour TOUS les utilisateurs (Consultant, Gestionnaire, Admin)

| Fonctionnalité | Comment y accéder | URL |
|----------------|-------------------|-----|
| **Mon Profil** | Sidebar → "Mon Profil" | `/auth/profile/` |
| **Changer mot de passe** | Sidebar → "Mot de passe" | `/auth/change-password/` |
| **Dashboard** | Sidebar → "Dashboard" | `/stock_debord/dashboard/` |

### Pour Gestionnaires et Admins

| Fonctionnalité | Comment y accéder | Visible dans |
|----------------|-------------------|--------------|
| **Valider mouvements** | Dans l'historique | Boutons de validation |
| **Gestion zones** | Sidebar → "Gestion Zones" | Menu principal |
| **Historique complet** | Sidebar → "Historique" | Toutes les données |

### Pour Admins UNIQUEMENT

| Fonctionnalité | Comment y accéder | URL |
|----------------|-------------------|-----|
| **Liste utilisateurs** | Sidebar → "Gestion Utilisateurs" | `/auth/users/` |
| **Créer utilisateur** | Gestion Utilisateurs → "Nouvel Utilisateur" | `/auth/users/create/` |
| **Modifier utilisateur** | Liste → Cliquer sur ✏️ Modifier | `/auth/users/<id>/edit/` |
| **Supprimer utilisateur** | Liste → Cliquer sur 🗑️ Supprimer | `/auth/users/<id>/delete/` |
| **Admin Django** | Sidebar → "Admin Django" | `/admin/` |

## 📱 Captures d'Écran Textuelles

### Vue Consultant

```
╔════════════════════════════════════════════════════════════╗
║ STELLANTIS DIZ                                             ║
║                                                            ║
║    👤 consultant                                           ║
║    [Consultant (Opérateur/Cariste)]                       ║
║                                                            ║
║ ──────────────────────────────────────────────────────     ║
║ 📊 Dashboard                                               ║
║ 📦 Gestion Références                                      ║
║ ➕ Ajouter Référence                                       ║
║ 🕐 Historique                                              ║
║ ... (menu standard)                                        ║
║ ❓ How to use it                                           ║
║ ──────────────────────────────────────────────────────     ║
║ 👤 Mon Profil                                              ║
║ 🔑 Mot de passe                                            ║
║ 🚪 Déconnexion                                             ║
╚════════════════════════════════════════════════════════════╝
```

### Vue Gestionnaire

```
╔════════════════════════════════════════════════════════════╗
║ STELLANTIS DIZ                                             ║
║                                                            ║
║    👤 gestionnaire                                         ║
║    [Gestionnaire de magasin]                              ║
║                                                            ║
║ ──────────────────────────────────────────────────────     ║
║ 📊 Dashboard                                               ║
║ 📦 Gestion Références                                      ║
║ ... (menu standard)                                        ║
║ ❓ How to use it                                           ║
║ ──────────────────────────────────────────────────────     ║
║ 👤 Mon Profil                                              ║
║ 🔑 Mot de passe                                            ║
║ 🚪 Déconnexion                                             ║
╚════════════════════════════════════════════════════════════╝
```

### Vue Admin

```
╔════════════════════════════════════════════════════════════╗
║ STELLANTIS DIZ                                             ║
║                                                            ║
║    👤 admin                                                ║
║    [Administrateur]                                        ║
║                                                            ║
║ ──────────────────────────────────────────────────────     ║
║ 📊 Dashboard                                               ║
║ 📦 Gestion Références                                      ║
║ ... (menu standard)                                        ║
║ ❓ How to use it                                           ║
║ ──────────────────────────────────────────────────────     ║
║ 👥 Gestion Utilisateurs    ← NOUVEAU                       ║
║ 🛠️  Admin Django            ← NOUVEAU                       ║
║ ──────────────────────────────────────────────────────     ║
║ 👤 Mon Profil                                              ║
║ 🔑 Mot de passe                                            ║
║ 🚪 Déconnexion                                             ║
╚════════════════════════════════════════════════════════════╝
```

## 🎯 Workflow Typique

### Scénario 1: Admin veut créer un nouvel utilisateur

1. Se connecter avec `admin` / `admin123`
2. Dans la sidebar, voir le lien **"Gestion Utilisateurs"**
3. Cliquer sur "Gestion Utilisateurs"
4. Page s'ouvre avec la liste des utilisateurs
5. Cliquer sur le bouton **"Nouvel Utilisateur"**
6. Remplir le formulaire
7. Cliquer sur **"Créer l'utilisateur"**
8. ✅ Nouvel utilisateur créé!

### Scénario 2: Utilisateur veut changer son mot de passe

1. Se connecter (n'importe quel rôle)
2. Dans la sidebar, cliquer sur **"Mot de passe"**
3. Entrer l'ancien mot de passe
4. Entrer le nouveau mot de passe (2 fois)
5. Cliquer sur **"Changer le mot de passe"**
6. ✅ Mot de passe changé!

### Scénario 3: Voir son profil et ses permissions

1. Se connecter (n'importe quel rôle)
2. Dans la sidebar, cliquer sur **"Mon Profil"**
3. Voir:
   - Nom d'utilisateur
   - Email
   - Rôle avec badge
   - Liste des permissions
   - Date de création

## 🎨 Codes Couleurs

### Badges de Rôle
```
Admin:        [■■■] Rouge (#dc3545)
Gestionnaire: [■■■] Jaune/Warning (#ffc107)
Consultant:   [■■■] Bleu/Info (#0dcaf0)
```

### Liens Spéciaux
```
Déconnexion: Rouge (text-danger)
Navigation:  Gris clair sur fond sombre
Actif:       Bleu (#3498db)
Hover:       Bleu foncé (#2980b9)
```

## 🔍 Débogage: "Je ne vois pas le lien Gestion Utilisateurs"

### Vérifications:

1. **Êtes-vous connecté en tant qu'Admin?**
   - Regardez le badge sous votre nom
   - Doit afficher "Administrateur" en rouge

2. **Avez-vous rafraîchi la page?**
   - Appuyez sur F5 ou Ctrl+F5

3. **Vérifier votre rôle:**
   ```python
   # Dans Django shell
   py manage.py shell
   >>> from apps.authentication.models import CustomUser
   >>> user = CustomUser.objects.get(username='admin')
   >>> print(user.role)  # Doit afficher 'admin'
   ```

4. **Template mis à jour?**
   - Vérifiez que `stock_debord/templates/stock_debord/base.html` a été modifié
   - Recherchez `{% if user.is_admin %}`

## 📞 Aide Rapide

| Je veux... | Où aller? | Rôle requis |
|------------|-----------|-------------|
| Créer un utilisateur | Sidebar → Gestion Utilisateurs → Nouvel Utilisateur | Admin |
| Voir tous les utilisateurs | Sidebar → Gestion Utilisateurs | Admin |
| Changer mon mot de passe | Sidebar → Mot de passe | Tous |
| Voir mes permissions | Sidebar → Mon Profil | Tous |
| Accéder à l'admin Django | Sidebar → Admin Django | Admin |
| Me déconnecter | Sidebar → Déconnexion | Tous |

---

**Note:** Tous les changements sont maintenant actifs! Déconnectez-vous et reconnectez-vous pour voir les mises à jour.

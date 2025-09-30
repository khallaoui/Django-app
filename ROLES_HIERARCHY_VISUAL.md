# Hiérarchie des Rôles - Diagramme Visuel

## 🏗️ Structure des Permissions

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          🔴 ADMINISTRATEUR                               │
│                                                                          │
│  ✅ Toutes les permissions du Gestionnaire                              │
│  ✅ Créer/Modifier/Supprimer des utilisateurs                           │
│  ✅ Accès à l'interface Django Admin                                    │
│  ✅ Accès aux paramètres système                                        │
│                                                                          │
│  Identifiants test : admin / admin123                                   │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   │ hérite de
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      🟡 GESTIONNAIRE DE MAGASIN                          │
│                                                                          │
│  MISSION : Contrôle des mouvements de stock entre entrepreneur & client │
│                                                                          │
│  ✅ Toutes les permissions du Consultant                                │
│  ✅ Gérer les références (modifier/supprimer)                           │
│  ✅ Consulter l'historique complet                                      │
│  ✅ Valider et assurer les mouvements d'entrées/sorties                 │
│  ✅ Superviser les opérations                                           │
│  ✅ Exporter en Excel                                                   │
│  ✅ Extraction des mouvements                                           │
│  ✅ Imprimer le stock                                                   │
│  ✅ Gérer les zones/travées                                             │
│                                                                          │
│  Identifiants test : gestionnaire / gestionnaire123                     │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   │ hérite de
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   🔵 CONSULTANT (Opérateur / Cariste)                    │
│                                                                          │
│  ✅ Consulter le stock (Dashboard)                                      │
│  ✅ Ajouter des références (Entrées)                                    │
│  ✅ Saisie sortie de pièces                                             │
│  ✅ Accéder aux fonctionnalités opérationnelles                         │
│  ✅ Gérer son profil et mot de passe                                    │
│                                                                          │
│  Identifiants test : consultant / consultant123                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Comparaison des Accès

### Dashboard & Stock
```
Feature                 │ Consultant │ Gestionnaire │ Admin
────────────────────────┼────────────┼──────────────┼───────
Consulter le stock      │     ✅     │      ✅      │  ✅
Rechercher              │     ✅     │      ✅      │  ✅
Filtrer par date        │     ✅     │      ✅      │  ✅
```

### Mouvements
```
Feature                 │ Consultant │ Gestionnaire │ Admin
────────────────────────┼────────────┼──────────────┼───────
Ajouter référence       │     ✅     │      ✅      │  ✅
Saisie sortie           │     ✅     │      ✅      │  ✅
Modifier référence      │     ❌     │      ✅      │  ✅
Supprimer référence     │     ❌     │      ✅      │  ✅
```

### Historique & Rapports
```
Feature                 │ Consultant │ Gestionnaire │ Admin
────────────────────────┼────────────┼──────────────┼───────
Historique complet      │     ❌     │      ✅      │  ✅
Exporter Excel          │     ❌     │      ✅      │  ✅
Extraction mouvements   │     ❌     │      ✅      │  ✅
Imprimer stock          │     ❌     │      ✅      │  ✅
```

### Gestion
```
Feature                 │ Consultant │ Gestionnaire │ Admin
────────────────────────┼────────────┼──────────────┼───────
Gérer zones/travées     │     ❌     │      ✅      │  ✅
Superviser              │     ❌     │      ✅      │  ✅
```

### Administration
```
Feature                 │ Consultant │ Gestionnaire │ Admin
────────────────────────┼────────────┼──────────────┼───────
Gérer utilisateurs      │     ❌     │      ❌      │  ✅
Django Admin            │     ❌     │      ❌      │  ✅
```

---

## 🔐 Mécanismes de Protection

### 1. Protection Backend (Views)

```python
# Exemple : Historique (Gestionnaire/Admin uniquement)
class HistoriqueView(GestionnaireRequiredMixin, LoginRequiredMixin, ListView):
    # ...
    pass

# Exemple : Export (Gestionnaire/Admin uniquement)
@login_required
@gestionnaire_required
def exporter_stock_excel(request):
    # ...
    pass
```

### 2. Protection Frontend (Templates)

```django
<!-- Navigation : Consultant ne voit pas ces liens -->
{% if user.is_gestionnaire or user.is_admin %}
    <li class="nav-item">
        <a href="{% url 'stock_debord:historique' %}">
            <i class="fas fa-history"></i>Historique
        </a>
    </li>
    <li class="nav-item">
        <a href="{% url 'stock_debord:gestion_references' %}">
            <i class="fas fa-boxes"></i>Gestion Références
        </a>
    </li>
{% endif %}
```

---

## 🌊 Flux de Travail par Rôle

### Consultant 🔵
```
Login
  │
  ▼
Dashboard (Consultation)
  │
  ├──► Ajouter Référence ──► Entrée enregistrée
  │
  ├──► Saisie Sortie ──► Sortie enregistrée
  │
  └──► Fonctionnalités opérationnelles
           │
           ▼
         Logout
```

### Gestionnaire 🟡 - Contrôle des Flux
```
ENTREPRENEUR/FOURNISSEUR
        │
        │ (Livraison pièces)
        ▼
┌────────────────────────┐
│       Login            │
│    Gestionnaire        │
└───────────┬────────────┘
            │
            ▼
    Dashboard (KPIs)
            │
    ┌───────┴───────┐
    │               │
    ▼               ▼
ENTRÉE          SUPERVISION
Ajouter Réf     Historique
Valider         Export Excel
    │           Extraction
    │               │
    └───────┬───────┘
            │
            ▼
    Gestion Stock
    - Références
    - Zones/Travées
    - Optimisation
            │
            ▼
        SORTIE
    Saisie Sortie
    Valider sortie
            │
            ▼
        CLIENT
            │
            ▼
        Logout
```

### Admin 🔴
```
Login
  │
  ▼
Dashboard (Consultation)
  │
  ├──► Actions du Gestionnaire
  │
  ├──► Gestion Utilisateurs ──► Créer/Modifier/Supprimer
  │
  ├──► Django Admin ──► Configuration système
  │
  └──► Paramètres système
           │
           ▼
         Logout
```

---

## 🎯 Matrice de Décision

### "Puis-je faire cette action ?"

```
                        ┌─────────────────────┐
                        │  Quelle action ?    │
                        └──────────┬──────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
         [Consultation]      [Mouvement]       [Gestion]
                │                  │                  │
                ▼                  ▼                  ▼
         ✅ Tous rôles      ✅ Tous rôles      ❌ Consultant
                                                ✅ Gestionnaire
                                                ✅ Admin
```

### "Puis-je accéder à cette page ?"

```
Page demandée
     │
     ├─ Dashboard? ──────────────────► ✅ Tous
     │
     ├─ Ajouter/Saisie sortie? ──────► ✅ Tous
     │
     ├─ Historique? ─────────────────► ❌ Consultant
     │                                  ✅ Gestionnaire/Admin
     │
     ├─ Export/Gestion? ─────────────► ❌ Consultant
     │                                  ✅ Gestionnaire/Admin
     │
     └─ Gestion Utilisateurs? ───────► ❌ Consultant/Gestionnaire
                                        ✅ Admin uniquement
```

---

## 📱 Interface Visuelle par Rôle

### Consultant 🔵 - Menu Simplifié
```
╔══════════════════════════╗
║ STELLANTIS DIZ           ║
║                          ║
║ 👤 consultant            ║
║ 🔵 Consultant            ║
╠══════════════════════════╣
║ 📊 Dashboard             ║ ← Visible
║ ➕ Ajouter Référence     ║ ← Visible
║ ➖ Saisie Sortie         ║ ← Visible
╠══════════════════════════╣
║ ... Autres fonctions ... ║
╠══════════════════════════╣
║ 👤 Mon Profil            ║
║ 🔑 Mot de passe          ║
║ 🚪 Déconnexion           ║
╚══════════════════════════╝

❌ Pas de : Historique, Export, Gestion
```

### Gestionnaire 🟡 - Menu Complet
```
╔══════════════════════════╗
║ STELLANTIS DIZ           ║
║                          ║
║ 👤 gestionnaire          ║
║ 🟡 Gestionnaire          ║
╠══════════════════════════╣
║ 📊 Dashboard             ║ ← Visible
║ ➕ Ajouter Référence     ║ ← Visible
║ ➖ Saisie Sortie         ║ ← Visible
╠══════════════════════════╣
║ 📦 Gestion Références    ║ ← Nouveau !
║ 📜 Historique            ║ ← Nouveau !
║ 📥 Extraction Mouvements ║ ← Nouveau !
║ 🗺️ Gestion Zones         ║ ← Nouveau !
╠══════════════════════════╣
║ ... Autres fonctions ... ║
╠══════════════════════════╣
║ 👤 Mon Profil            ║
║ 🔑 Mot de passe          ║
║ 🚪 Déconnexion           ║
╚══════════════════════════╝

✅ Accès complet au stock
```

### Admin 🔴 - Menu Maximum
```
╔══════════════════════════╗
║ STELLANTIS DIZ           ║
║                          ║
║ 👤 admin                 ║
║ 🔴 Administrateur        ║
╠══════════════════════════╣
║ ... Menu Gestionnaire... ║
╠══════════════════════════╣
║ 👥 Gestion Utilisateurs  ║ ← Nouveau !
║ ⚙️ Admin Django          ║ ← Nouveau !
╠══════════════════════════╣
║ 👤 Mon Profil            ║
║ 🔑 Mot de passe          ║
║ 🚪 Déconnexion           ║
╚══════════════════════════╝

✅ Accès total au système
```

---

## 🔥 Points Clés

### ⚡ Ce qui a changé pour les Consultants

**AVANT (❌ Problématique) :**
- Accès à tout
- Pouvait voir l'historique complet
- Pouvait exporter les données
- Pouvait gérer les références

**APRÈS (✅ Corrigé) :**
- Accès limité aux opérations de base
- Ne peut pas voir l'historique complet
- Ne peut pas exporter
- Ne peut pas gérer les références
- Interface épurée et claire

### 🛡️ Sécurité Renforcée

1. **Double protection** : Backend + Frontend
2. **Messages clairs** : L'utilisateur sait pourquoi il ne peut pas accéder
3. **Redirection automatique** : Pas de pages d'erreur 404/403
4. **Audit trail** : Toutes les actions sont tracées dans l'historique

---

**Version :** 1.1  
**Date :** 29 septembre 2025

# Application de Gestion de Stock Débord - STELLANTIS DIZ

## Description

Cette application Django permet la gestion complète du stock en débord pour STELLANTIS DIZ. Elle offre une interface web moderne pour gérer les références, les entrées/sorties, et l'historique des mouvements de stock.

## Fonctionnalités

### Dashboard Principal
- Vue d'ensemble du stock avec KPI (total des bacs, nombre de références)
- Tableau de bord avec recherche en temps réel
- Boutons d'action rapide pour toutes les opérations

### Gestion des Références
- **Ajouter Référence** : Formulaire complet pour ajouter une nouvelle référence
- **Vider Travée** : Fonction pour vider complètement une travée
- **Saisie Sortie** : Enregistrement des sorties de stock avec validation
- **Historique E/S** : Consultation de l'historique complet des mouvements

### Fonctionnalités d'Export
- **Export Excel** : Téléchargement du stock au format Excel
- **Impression** : Version imprimable du stock actuel

### Navigation
- **Dashboard** : Vue principale du stock
- **Boot KIT** : Module spécialisé (à développer)
- **Cross DOCK** : Gestion cross-docking (à développer)
- **Map Débord** : Visualisation cartographique (à développer)
- **FLC** : Gestion des flux logistiques (à développer)
- **Log ext** : Journal des événements externes (à développer)
- **How to use it** : Documentation utilisateur (à développer)

## Modèles de Données

### Reference
- Emplacement SM
- Référence
- Nombre de bacs
- Date d'entrée
- Travée débord
- Code condi
- Quantité pièce/UC
- Appro
- Fournisseur
- CMJ
- F

### Historique
- Référence (clé étrangère)
- Type d'action (entrée/sortie)
- Nombre de bacs
- Date d'action
- Utilisateur

### Travée
- Nom
- Capacité
- Relations avec les références

## Installation et Configuration

### 1. Migrations
```bash
cd "c:\Users\Admin\Desktop\students\py project\Django app\mon_projet"
python manage.py makemigrations stock_debord
python manage.py migrate
```

### 2. Données d'exemple
```bash
python manage.py populate_stock_data
```

### 3. Accès à l'application
L'application est accessible via : `http://localhost:8000/stock-debord/`

## Structure des Templates

```
stock_debord/templates/stock_debord/
├── base.html                 # Template de base avec sidebar
├── dashboard.html            # Dashboard principal
├── ajouter_reference.html    # Formulaire d'ajout
├── vider_travee.html         # Interface pour vider une travée
├── saisie_sortie.html        # Formulaire de sortie
├── historique.html           # Liste de l'historique
├── imprimer_stock.html       # Version imprimable
└── partials/
    └── table_stock.html      # Tableau réutilisable du stock
```

## Fonctionnalités Techniques

### Authentification
- Toutes les vues nécessitent une authentification
- Utilisation du système d'authentification Django existant

### Responsive Design
- Interface adaptée mobile et desktop
- Utilisation de Bootstrap 5
- Icônes Font Awesome

### Recherche
- Recherche en temps réel dans le tableau de stock
- Filtrage côté client avec JavaScript

### Validation
- Validation des formulaires côté serveur
- Messages d'erreur et de succès
- Vérification des stocks avant sortie

## URLs de l'Application

- `/stock-debord/` - Dashboard principal
- `/stock-debord/ajouter/` - Ajouter une référence
- `/stock-debord/vider-travee/` - Vider une travée
- `/stock-debord/saisie-sortie/` - Saisie de sortie
- `/stock-debord/historique/` - Historique des mouvements
- `/stock-debord/exporter-excel/` - Export Excel
- `/stock-debord/imprimer/` - Version imprimable

## Tests

L'application inclut des tests unitaires pour :
- Modèles de données
- Vues principales
- Authentification

Exécuter les tests :
```bash
python manage.py test stock_debord
```

## Dépendances Optionnelles

Pour l'export Excel, installer pandas :
```bash
pip install pandas openpyxl
```

## Administration Django

Les modèles sont enregistrés dans l'admin Django avec :
- Filtres par travée, date, fournisseur
- Recherche par référence, emplacement
- Tri par date d'entrée

## Sécurité

- Protection CSRF sur tous les formulaires
- Authentification requise pour toutes les vues
- Validation des données d'entrée
- Messages de confirmation pour les actions critiques

## Personnalisation

L'application peut être étendue avec :
- Nouveaux types d'actions dans l'historique
- Alertes automatiques pour stock bas
- Intégration avec systèmes externes
- Rapports avancés
- API REST pour intégration mobile
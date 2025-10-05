##  Description

Application web Django pour la gestion des alertes dans un environnement logistique. L'application permet de créer, suivre et gérer des alertes liées aux stocks et aux zones de kit.

##  Architecture

### Structure du Projet
```
mon_projet/
├── manage.py
├── requirements.txt
├── README.md
├── check_app.py
├── mon_projet/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── authentication/     # Gestion des utilisateurs
│   ├── alertes/           # Gestion des alertes
│   └── dashboard/         # Tableau de bord
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    ├── registration/
    ├── alertes/
    ���── dashboard/
```

### Applications Django

#### 1. Authentication
- **Modèles**: CustomUser avec rôles (admin, agent_kit, agent_cross, agent_debord)
- **Vues**: Inscription, connexion, déconnexion
- **Fonctionnalités**: Authentification personnalisée avec rôles

#### 2. Alertes
- **Modèles**: Alerte, HistoriqueAlerte, StockDebord
- **Vues**: Création, liste, mise à jour des statuts
- **Fonctionnalités**: Gestion complète du cycle de vie des alertes

#### 3. Dashboard
- **Vues**: Tableau de bord avec métriques
- **Fonctionnalités**: Vue d'ensemble des alertes et statistiques

##  Installation et Configuration

### Prérequis
- Python 3.8+
- MySQL 5.7+ ou MariaDB
- pip (gestionnaire de paquets Python)

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Configuration de la base de données

#### Option A: MySQL (Recommandé pour la production)
1. Créer une base de données MySQL:
```sql
CREATE DATABASE gestion_alertes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'votre_username'@'localhost' IDENTIFIED BY 'votre_password';
GRANT ALL PRIVILEGES ON gestion_alertes_db.* TO 'votre_username'@'localhost';
FLUSH PRIVILEGES;
```

2. Modifier `settings.py` avec vos paramètres:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_alertes_db',
        'USER': 'votre_username',
        'PASSWORD': 'votre_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### Option B: SQLite (Pour le développement)
Décommentez la configuration SQLite dans `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 3. Migrations de la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 5. Vérification de l'installation
```bash
python check_app.py
```

### 6. Démarrer le serveur de développement
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse: http://127.0.0.1:8000/

##  Utilisation

### Rôles Utilisateur

1. **Administrateur**: Accès complet à toutes les fonctionnalités
2. **Agent Bord Kit**: Création et gestion des alertes de kit
3. **Agent Cross Dock**: Gestion des transferts et livraisons
4. **Agent Débord**: Gestion des stocks de débordement

### Fonctionnalités Principales

#### 1. Dashboard
- Vue d'ensemble des alertes par statut
- Métriques en temps réel
- Alertes récentes
- Statistiques par zone

#### 2. Gestion des Alertes
- **Création**: Nouvelle alerte avec référence, zone, nombre de bacs
- **Suivi**: Historique complet des modifications
- **Statuts**: En cours → Livré → FLC envoyé → Clôturé
- **Filtrage**: Par statut, zone, date

#### 3. Authentification
- Connexion sécurisée
- Inscription avec validation des rôles
- Gestion des sessions

##  Configuration Avancée

### Variables d'Environnement
Créez un fichier `.env` pour les paramètres sensibles:
```
SECRET_KEY=votre_clé_secrète
DEBUG=True
DB_NAME=gestion_alertes_db
DB_USER=votre_username
DB_PASSWORD=votre_password
DB_HOST=localhost
DB_PORT=3306
```

### Sécurité
- CSRF protection activée
- XSS protection
- Authentification requise pour toutes les vues
- Validation des formulaires côté client et serveur

### Performance
- Auto-refresh du dashboard (30 secondes)
- Requêtes optimisées avec select_related
- Pagination pour les grandes listes
- Cache des métriques

##  Interface Utilisateur

### Technologies Frontend
- **Bootstrap 5**: Framework CSS responsive
- **Font Awesome**: Icônes
- **jQuery**: Interactions JavaScript
- **AJAX**: Mises à jour en temps réel

### Fonctionnalités UI
- Interface responsive (mobile-friendly)
- Notifications en temps réel
- Confirmations pour les actions critiques
- Indicateurs de chargement
- Tri et filtrage des tables

##  Base de Données

### Modèles Principaux

#### CustomUser
```python
- username, email, password (hérité d'AbstractUser)
- role: Choix parmi les 4 rôles
- phone: Numéro de téléphone (optionnel)
- created_at: Date de création
```

#### Alerte
```python
- reference: Référence unique
- zone_kit: Zone de kit (1-11)
- nombre_bacs: Nombre de bacs restants
- statut: en_cours, livre, flc, cloture
- date_creation, date_cloture
- createur, traite_par: Relations vers CustomUser
- commentaires: Texte libre
```

#### HistoriqueAlerte
```python
- alerte: Relation vers Alerte
- action: Description de l'action
- utilisateur: Qui a fait l'action
- date_modification: Quand
- ancien_statut, nouveau_statut: Changements
```

##  Tests et Vérification

### Script de Vérification
```bash
python check_app.py
```

Ce script vérifie:
- ✅ Configuration Django
- ✅ Modèles et relations
- ✅ Vues et URLs
- ✅ Templates et fichiers statiques
- ✅ Connexion base de données

### Tests Unitaires
```bash
python manage.py test
```

##  Déploiement

### Préparation pour la Production
1. Modifier `DEBUG = False` dans settings.py
2. Configurer `ALLOWED_HOSTS`
3. Utiliser une base de données robuste (MySQL/PostgreSQL)
4. Configurer les fichiers statiques avec `collectstatic`
5. Utiliser un serveur web (Nginx + Gunicorn)

### Variables de Production
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

##  API et Extensions

### URLs Principales
- `/` - Dashboard
- `/auth/login/` - Connexion
- `/auth/register/` - Inscription
- `/alertes/create/` - Créer une alerte
- `/alertes/list/` - Liste des alertes
- `/alertes/update-statut/<id>/` - Mise à jour AJAX

### Extensions Possibles
- API REST avec Django REST Framework
- Notifications par email/SMS
- Export Excel/PDF
- Graphiques avancés avec Chart.js
- Intégration avec des systèmes externes

##  Dépannage

### Problèmes Courants

1. **Erreur de connexion MySQL**
   - Vérifier que MySQL est démarré
   - Contrôler les paramètres de connexion
   - Vérifier les permissions utilisateur

2. **Erreur de migration**
   ```bash
   python manage.py makemigrations --empty apps.authentication
   python manage.py migrate --fake-initial
   ```

3. **Fichiers statiques non trouvés**
   ```bash
   python manage.py collectstatic
   ```

4. **Erreur CSRF**
   - Vérifier que `{% csrf_token %}` est présent dans les formulaires
   - Contrôler la configuration CSRF dans settings.py

---

**Version**: 1.0.0  
**Dernière mise à jour**: Décembre 2024  
**Compatibilité**: Django 4.2+, Python 3.8+" 

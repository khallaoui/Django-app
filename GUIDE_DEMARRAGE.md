# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## ⚡ Démarrage Ultra-Rapide (Recommandé)

### Option 1: Script Automatique
1. **Double-cliquez sur `start.bat`**
2. Suivez les instructions à l'écran
3. L'application se configurera automatiquement

### Option 2: Script Python
```cmd
py setup_quick.py
```

## 🔧 Résolution des Problèmes Identifiés

### ❌ Problème 1: "pip n'est pas reconnu"
**Solution**: Utiliser `py -m pip` au lieu de `pip`
```cmd
py -m pip install Django
py -m pip install python-decouple
py -m pip install Pillow
```

### ❌ Problème 2: "Can't connect to MySQL server"
**Solution**: Configuration SQLite (déjà fait dans settings.py)
- ✅ L'application utilise maintenant SQLite au lieu de MySQL
- ✅ Aucune installation de MySQL requise
- ✅ Base de données créée automatiquement

### ❌ Problème 3: "python n'est pas reconnu"
**Solution**: Utiliser `py` au lieu de `python`
```cmd
py manage.py runserver
py manage.py migrate
py manage.py createsuperuser
```

## 📋 Étapes Manuelles (si les scripts automatiques échouent)

### 1. Installation des Dépendances
```cmd
py -m pip install Django==4.2.7
py -m pip install python-decouple
py -m pip install Pillow
```

### 2. Configuration de la Base de Données
```cmd
py manage.py makemigrations
py manage.py migrate
```

### 3. Création d'un Compte Admin
```cmd
py manage.py createsuperuser
```
Ou utilisez le compte créé automatiquement:
- **Nom d'utilisateur**: admin
- **Mot de passe**: admin123

### 4. Démarrage du Serveur
```cmd
py manage.py runserver
```
Ou double-cliquez sur `run_server.bat`

## 🌐 Accès à l'Application

Une fois le serveur démarré:

- **🏠 Application principale**: http://127.0.0.1:8000/
- **🔐 Page de connexion**: http://127.0.0.1:8000/auth/login/
- **📝 Inscription**: http://127.0.0.1:8000/auth/register/
- **⚙️ Administration Django**: http://127.0.0.1:8000/admin/

## 👥 Comptes de Démonstration

### Compte Administrateur
- **Nom d'utilisateur**: admin
- **Mot de passe**: admin123
- **Rôle**: Administrateur complet

### Comptes Agents
- **agent_kit** / demo123 (Agent Bord Kit)
- **agent_cross** / demo123 (Agent Cross Dock)
- **agent_debord** / demo123 (Agent Débord)

## 🎯 Fonctionnalités Disponibles

### 📊 Dashboard
- Vue d'ensemble des alertes
- Métriques en temps réel
- Statistiques par statut

### 🚨 Gestion des Alertes
- Création d'alertes
- Liste avec filtres
- Mise à jour des statuts (AJAX)
- Historique complet

### 👤 Authentification
- Connexion/Déconnexion
- Inscription avec rôles
- Gestion des permissions

## 🔍 Vérification du Fonctionnement

### Test Rapide
1. Aller sur http://127.0.0.1:8000/
2. Se connecter avec admin/admin123
3. Créer une nouvelle alerte
4. Vérifier le dashboard

### Test Complet
```cmd
py test_connectivity.py
```

## 🆘 En Cas de Problème

### Erreur de Migration
```cmd
del db.sqlite3
py manage.py makemigrations
py manage.py migrate
```

### Erreur de Dépendances
```cmd
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

### Erreur de Port (8000 occupé)
```cmd
py manage.py runserver 8001
```
Puis accéder à http://127.0.0.1:8001/

### Réinitialisation Complète
1. Supprimer `db.sqlite3`
2. Supprimer les dossiers `__pycache__`
3. Relancer `py setup_quick.py`

## 📞 Support

Si vous rencontrez encore des problèmes:

1. **Vérifiez les logs** dans la console
2. **Utilisez le script de diagnostic**: `py check_app.py`
3. **Consultez le README.md** pour plus de détails

## 🎉 Félicitations !

Si vous voyez cette page dans votre navigateur, votre application Django de gestion des alertes fonctionne parfaitement ! 🚀

---

**Version**: 1.0.0 - Configuration Windows  
**Base de données**: SQLite (développement)  
**Python**: Utilisation de `py` au lieu de `python`
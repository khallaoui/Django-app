# 🐬 GUIDE MYSQL - APPLICATION DJANGO

## 🚨 RÉSOLUTION DU PROBLÈME ACTUEL

Vous avez l'erreur : `no such table: authentication_customuser`

### ✅ SOLUTION RAPIDE (Recommandée)

```cmd
py fix_migrations.py
```

Ce script va :
1. ✅ Nettoyer les anciennes migrations
2. ✅ Créer de nouvelles migrations
3. ✅ Appliquer les migrations
4. ✅ Créer un compte admin
5. ✅ Tester l'application

## 🐬 CONFIGURATION MYSQL COMPLÈTE

### Option 1: Script Automatique
```cmd
py setup_mysql.py
```

### Option 2: Double-clic
```
Double-cliquez sur: setup_mysql.bat
```

## 📋 PRÉREQUIS MYSQL

### 1. Installer MySQL

#### Option A: MySQL Community Server
1. Téléchargez : https://dev.mysql.com/downloads/mysql/
2. Installez avec les paramètres par défaut
3. Notez le mot de passe root

#### Option B: XAMPP (Plus simple)
1. Téléchargez : https://www.apachefriends.org/
2. Installez XAMPP
3. Démarrez MySQL depuis le panneau XAMPP

#### Option C: WAMP
1. Téléchargez : https://www.wampserver.com/
2. Installez WAMP
3. Démarrez tous les services

### 2. Vérifier MySQL
```cmd
mysql --version
```

## 🔧 CONFIGURATION MANUELLE

### 1. Installer mysqlclient
```cmd
py -m pip install mysqlclient
```

Si erreur, essayez :
```cmd
py -m pip install --only-binary=all mysqlclient
```

### 2. Créer la Base de Données

#### Via MySQL Command Line
```sql
CREATE DATABASE gestion_alertes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'django_password';
GRANT ALL PRIVILEGES ON gestion_alertes_db.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Via phpMyAdmin (XAMPP/WAMP)
1. Ouvrez http://localhost/phpmyadmin/
2. Créez une base de données : `gestion_alertes_db`
3. Collation : `utf8mb4_unicode_ci`

### 3. Configurer settings.py

Modifiez dans `mon_projet/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_alertes_db',
        'USER': 'root',  # ou 'django_user'
        'PASSWORD': '',  # votre mot de passe MySQL
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

### 4. Appliquer les Migrations
```cmd
py manage.py makemigrations
py manage.py migrate
```

### 5. Créer un Superutilisateur
```cmd
py manage.py createsuperuser
```

## 🔍 DIAGNOSTIC DES PROBLÈMES

### Erreur: "Can't connect to MySQL server"
**Solutions** :
1. Vérifiez que MySQL est démarré
2. Vérifiez les paramètres de connexion
3. Testez la connexion : `mysql -u root -p`

### Erreur: "Access denied for user"
**Solutions** :
1. Vérifiez le nom d'utilisateur et mot de passe
2. Créez un nouvel utilisateur MySQL
3. Utilisez l'utilisateur root

### Erreur: "mysqlclient installation failed"
**Solutions** :
1. Installez Visual Studio Build Tools
2. Utilisez une version précompilée : `py -m pip install --only-binary=all mysqlclient`
3. Utilisez conda : `conda install mysqlclient`

### Erreur: "no such table"
**Solution** :
```cmd
py fix_migrations.py
```

## 🎯 PARAMÈTRES MYSQL RECOMMANDÉS

### Pour XAMPP
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_alertes_db',
        'USER': 'root',
        'PASSWORD': '',  # Vide par défaut dans XAMPP
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Pour WAMP
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_alertes_db',
        'USER': 'root',
        'PASSWORD': '',  # Vide par défaut dans WAMP
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Pour MySQL Community Server
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_alertes_db',
        'USER': 'root',
        'PASSWORD': 'votre_mot_de_passe',  # Défini lors de l'installation
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 🚀 DÉMARRAGE APRÈS CONFIGURATION

### 1. Vérifier la Configuration
```cmd
py manage.py check
```

### 2. Tester la Connexion
```cmd
py manage.py dbshell
```

### 3. Démarrer le Serveur
```cmd
py manage.py runserver
```

### 4. Accéder à l'Application
- **Application** : http://127.0.0.1:8000/
- **Admin** : http://127.0.0.1:8000/admin/
- **Connexion** : admin / admin123

## 📊 AVANTAGES DE MYSQL

### ✅ Avantages
- Performance supérieure pour les grandes applications
- Support des transactions ACID
- Réplication et clustering
- Outils d'administration avancés
- Compatible avec la production

### ⚠️ Considérations
- Installation plus complexe que SQLite
- Nécessite un serveur MySQL
- Configuration réseau requise

## 🔄 BASCULER ENTRE SQLITE ET MYSQL

### Vers SQLite (Développement)
1. Modifiez `settings.py` :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
2. `py manage.py migrate`

### Vers MySQL (Production)
1. Modifiez `settings.py` avec les paramètres MySQL
2. `py manage.py migrate`

## 🆘 SUPPORT

### En cas de problème :
1. **Exécutez** : `py fix_migrations.py`
2. **Vérifiez** : `py manage.py check`
3. **Testez** : `py manage.py dbshell`
4. **Consultez** les logs d'erreur

### Scripts disponibles :
- `fix_migrations.py` - Répare les migrations
- `setup_mysql.py` - Configuration complète MySQL
- `check_app.py` - Diagnostic complet

---

**🎉 Une fois MySQL configuré, votre application sera prête pour la production !**
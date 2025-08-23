#!/usr/bin/env python
"""
Script de configuration MySQL pour l'application Django
Ce script installe MySQL, configure la base de données et résout les problèmes de migration
"""

import os
import sys
import subprocess
import django
from pathlib import Path
import time

def print_header(title):
    """Afficher un en-tête formaté"""
    print("\n" + "="*70)
    print(f"🔧 {title}")
    print("="*70)

def run_command(command, description, ignore_errors=False):
    """Exécuter une commande et afficher le résultat"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                # Afficher les dernières lignes importantes
                lines = result.stdout.strip().split('\n')
                for line in lines[-3:]:
                    if line.strip() and not line.startswith('WARNING'):
                        print(f"   {line}")
            return True
        else:
            if ignore_errors:
                print(f"⚠️  {description} - Ignoré")
                return True
            print(f"❌ {description} - Erreur")
            if result.stderr.strip():
                print(f"   Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def install_mysql_dependencies():
    """Installer les dépendances MySQL"""
    print_header("INSTALLATION DES DÉPENDANCES MYSQL")
    
    print("📦 Installation de mysqlclient...")
    print("   Note: Cela peut prendre quelques minutes...")
    
    # Essayer différentes méthodes d'installation
    methods = [
        "py -m pip install mysqlclient",
        "py -m pip install --only-binary=all mysqlclient",
        "py -m pip install --upgrade pip setuptools wheel && py -m pip install mysqlclient",
    ]
    
    for method in methods:
        print(f"\n🔄 Tentative: {method}")
        if run_command(method, "Installation mysqlclient", ignore_errors=True):
            break
        print("   Échec, tentative suivante...")
    
    # Installer les autres dépendances
    other_deps = [
        "Django==4.2.7",
        "python-decouple",
        "Pillow"
    ]
    
    for dep in other_deps:
        run_command(f"py -m pip install {dep}", f"Installation {dep}")
    
    return True

def check_mysql_server():
    """Vérifier si MySQL est installé et démarré"""
    print_header("VÉRIFICATION DU SERVEUR MYSQL")
    
    # Vérifier si MySQL est installé
    mysql_paths = [
        "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe",
        "C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysql.exe",
        "C:\\xampp\\mysql\\bin\\mysql.exe",
        "C:\\wamp64\\bin\\mysql\\mysql8.0.31\\bin\\mysql.exe",
        "mysql"  # Si dans le PATH
    ]
    
    mysql_found = False
    mysql_path = None
    
    for path in mysql_paths:
        if path == "mysql":
            # Tester si mysql est dans le PATH
            result = subprocess.run("mysql --version", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                mysql_found = True
                mysql_path = "mysql"
                print(f"✅ MySQL trouvé dans le PATH")
                print(f"   Version: {result.stdout.strip()}")
                break
        else:
            if Path(path).exists():
                mysql_found = True
                mysql_path = path
                print(f"✅ MySQL trouvé: {path}")
                break
    
    if not mysql_found:
        print("❌ MySQL non trouvé sur le système")
        print("\n💡 Options pour installer MySQL:")
        print("   1. Télécharger MySQL Community Server: https://dev.mysql.com/downloads/mysql/")
        print("   2. Installer XAMPP: https://www.apachefriends.org/")
        print("   3. Installer WAMP: https://www.wampserver.com/")
        
        choice = input("\nVoulez-vous continuer avec une installation automatique de MySQL ? (o/N): ").lower()
        if choice in ['o', 'oui', 'y', 'yes']:
            return install_mysql_automatically()
        else:
            return False
    
    return True, mysql_path

def install_mysql_automatically():
    """Installer MySQL automatiquement via Chocolatey"""
    print_header("INSTALLATION AUTOMATIQUE DE MYSQL")
    
    print("🍫 Installation via Chocolatey...")
    print("   Note: Cela nécessite des privilèges administrateur")
    
    # Vérifier si Chocolatey est installé
    choco_result = subprocess.run("choco --version", shell=True, capture_output=True, text=True)
    
    if choco_result.returncode != 0:
        print("❌ Chocolatey non installé")
        print("\n💡 Pour installer Chocolatey (en tant qu'administrateur):")
        print('   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))')
        return False
    
    # Installer MySQL via Chocolatey
    if run_command("choco install mysql -y", "Installation MySQL via Chocolatey"):
        print("✅ MySQL installé avec succès")
        print("⚠️  Redémarrez votre ordinateur pour finaliser l'installation")
        return True
    
    return False

def create_mysql_database():
    """Créer la base de données MySQL"""
    print_header("CRÉATION DE LA BASE DE DONNÉES MYSQL")
    
    print("🗄️  Création de la base de données 'gestion_alertes_db'...")
    
    # Script SQL pour créer la base de données
    sql_commands = [
        "CREATE DATABASE IF NOT EXISTS gestion_alertes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "CREATE USER IF NOT EXISTS 'django_user'@'localhost' IDENTIFIED BY 'django_password';",
        "GRANT ALL PRIVILEGES ON gestion_alertes_db.* TO 'django_user'@'localhost';",
        "FLUSH PRIVILEGES;"
    ]
    
    # Essayer de se connecter avec différents utilisateurs
    mysql_users = [
        ("root", ""),
        ("root", "root"),
        ("root", "password"),
        ("", "")
    ]
    
    for user, password in mysql_users:
        print(f"\n🔑 Tentative de connexion avec utilisateur: {user or 'anonymous'}")
        
        for sql_command in sql_commands:
            if password:
                cmd = f'mysql -u {user} -p{password} -e "{sql_command}"'
            else:
                cmd = f'mysql -u {user} -e "{sql_command}"'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                if "Access denied" in result.stderr:
                    print(f"   ❌ Accès refusé pour {user}")
                    break
                else:
                    print(f"   ⚠️  Erreur SQL: {result.stderr.strip()}")
            else:
                print(f"   ✅ Commande SQL exécutée: {sql_command[:50]}...")
        else:
            # Si toutes les commandes ont réussi
            print(f"✅ Base de données créée avec l'utilisateur {user}")
            
            # Mettre à jour settings.py avec les bonnes informations
            update_database_settings(user, password)
            return True
    
    print("❌ Impossible de créer la base de données automatiquement")
    print("\n💡 Créez manuellement la base de données:")
    print("   1. Ouvrez MySQL Command Line Client")
    print("   2. Exécutez: CREATE DATABASE gestion_alertes_db;")
    print("   3. Modifiez les paramètres dans settings.py")
    
    return False

def update_database_settings(user, password):
    """Mettre à jour les paramètres de base de données dans settings.py"""
    print(f"🔧 Mise à jour des paramètres de connexion...")
    
    settings_path = Path("mon_projet/settings.py")
    if not settings_path.exists():
        print("❌ Fichier settings.py non trouvé")
        return False
    
    # Lire le fichier settings.py
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les paramètres de base de données
    old_user_line = "'USER': 'root',"
    new_user_line = f"'USER': '{user}',"
    content = content.replace(old_user_line, new_user_line)
    
    old_password_line = "'PASSWORD': '',"
    new_password_line = f"'PASSWORD': '{password}',"
    content = content.replace(old_password_line, new_password_line)
    
    # Écrire le fichier modifié
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Paramètres mis à jour: USER={user}, PASSWORD={'***' if password else '(vide)'}")
    return True

def reset_migrations():
    """Réinitialiser les migrations"""
    print_header("RÉINITIALISATION DES MIGRATIONS")
    
    # Supprimer les anciens fichiers de migration
    migration_dirs = [
        "apps/authentication/migrations",
        "apps/alertes/migrations",
        "apps/dashboard/migrations"
    ]
    
    for migration_dir in migration_dirs:
        migration_path = Path(migration_dir)
        if migration_path.exists():
            print(f"🗑️  Nettoyage des migrations: {migration_dir}")
            for file in migration_path.glob("*.py"):
                if file.name != "__init__.py":
                    file.unlink()
                    print(f"   Supprimé: {file.name}")
    
    # Supprimer l'ancienne base SQLite si elle existe
    sqlite_db = Path("db.sqlite3")
    if sqlite_db.exists():
        sqlite_db.unlink()
        print("🗑️  Ancienne base SQLite supprimée")
    
    return True

def create_migrations():
    """Créer les nouvelles migrations"""
    print_header("CRÉATION DES MIGRATIONS")
    
    # Créer les migrations pour chaque app
    apps = ["authentication", "alertes", "dashboard"]
    
    for app in apps:
        if run_command(f"py manage.py makemigrations {app}", f"Migrations pour {app}"):
            print(f"✅ Migrations créées pour {app}")
        else:
            print(f"⚠️  Problème avec les migrations de {app}")
    
    # Créer les migrations générales
    run_command("py manage.py makemigrations", "Migrations générales")
    
    return True

def apply_migrations():
    """Appliquer les migrations"""
    print_header("APPLICATION DES MIGRATIONS")
    
    # Appliquer les migrations
    if run_command("py manage.py migrate", "Application des migrations"):
        print("✅ Toutes les migrations appliquées avec succès")
        return True
    else:
        print("❌ Erreur lors de l'application des migrations")
        return False

def create_superuser():
    """Créer un superutilisateur"""
    print_header("CRÉATION DU SUPERUTILISATEUR")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Vérifier si un superutilisateur existe déjà
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Un superutilisateur existe déjà")
            return True
        
        # Créer un superutilisateur par défaut
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        
        print("✅ Superutilisateur créé avec succès!")
        print("   👤 Nom d'utilisateur: admin")
        print("   🔑 Mot de passe: admin123")
        print("   📧 Email: admin@example.com")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du superutilisateur: {e}")
        print("\n💡 Créez manuellement avec: py manage.py createsuperuser")
        return False

def test_mysql_connection():
    """Tester la connexion MySQL"""
    print_header("TEST DE LA CONNEXION MYSQL")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        django.setup()
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            
        print(f"✅ Connexion MySQL réussie!")
        print(f"   Version MySQL: {version[0]}")
        
        # Tester les modèles
        from django.contrib.auth import get_user_model
        from apps.alertes.models import Alerte
        
        User = get_user_model()
        users_count = User.objects.count()
        alertes_count = Alerte.objects.count()
        
        print(f"   Utilisateurs: {users_count}")
        print(f"   Alertes: {alertes_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion MySQL: {e}")
        return False

def main():
    """Fonction principale"""
    print("="*70)
    print("🐬 CONFIGURATION MYSQL - APPLICATION GESTION DES ALERTES")
    print("="*70)
    
    # Vérifications préliminaires
    if not Path('manage.py').exists():
        print("❌ Fichier manage.py non trouvé. Êtes-vous dans le bon répertoire ?")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    print("✅ Configuration pour MySQL")
    print("✅ Utilisation de 'py' au lieu de 'python'")
    
    # Étapes de configuration
    steps = [
        ("Installation des dépendances MySQL", install_mysql_dependencies),
        ("Vérification du serveur MySQL", check_mysql_server),
        ("Création de la base de données", create_mysql_database),
        ("Réinitialisation des migrations", reset_migrations),
        ("Création des nouvelles migrations", create_migrations),
        ("Application des migrations", apply_migrations),
        ("Création du superutilisateur", create_superuser),
        ("Test de la connexion MySQL", test_mysql_connection),
    ]
    
    results = []
    for step_name, step_func in steps:
        try:
            if step_name == "Vérification du serveur MySQL":
                result = step_func()
                if isinstance(result, tuple):
                    result = result[0]
            else:
                result = step_func()
            results.append((step_name, result))
            
            if not result and step_name in ["Vérification du serveur MySQL", "Création de la base de données"]:
                print(f"\n⚠️  Étape critique échouée: {step_name}")
                print("Impossible de continuer sans MySQL configuré")
                break
                
        except Exception as e:
            print(f"\n❌ Erreur critique à l'étape {step_name}: {e}")
            results.append((step_name, False))
    
    # Résumé
    print_header("RÉSUMÉ DE LA CONFIGURATION MYSQL")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for step_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"{step_name:<45} {status}")
    
    print(f"\n🎯 Résultat: {passed}/{total} étapes réussies")
    
    if passed >= 6:  # Au moins 6 étapes sur 8
        print("\n🎉 CONFIGURATION MYSQL RÉUSSIE!")
        print("\n📋 Informations de connexion:")
        print("   👤 Admin: admin / admin123")
        print("   🗄️  Base de données: gestion_alertes_db")
        print("   🔗 MySQL: localhost:3306")
        
        print("\n🌐 URLs importantes:")
        print("   🏠 Accueil: http://127.0.0.1:8000/")
        print("   🔐 Connexion: http://127.0.0.1:8000/auth/login/")
        print("   ⚙️  Admin: http://127.0.0.1:8000/admin/")
        
        # Proposer de démarrer le serveur
        response = input("\n🚀 Voulez-vous démarrer le serveur maintenant ? (o/N): ").lower()
        if response in ['o', 'oui', 'y', 'yes']:
            print("\n🚀 Démarrage du serveur...")
            print("📱 Application accessible sur: http://127.0.0.1:8000/")
            print("⏹️  Appuyez sur Ctrl+C pour arrêter")
            print("="*70)
            try:
                subprocess.run(['py', 'manage.py', 'runserver'], check=True)
            except KeyboardInterrupt:
                print("\n⏹️  Serveur arrêté")
        else:
            print("\n✅ Configuration MySQL terminée!")
            print("Pour démarrer le serveur: py manage.py runserver")
    else:
        print("\n⚠️  CONFIGURATION INCOMPLÈTE")
        print("Certaines étapes ont échoué. Vérifiez les erreurs ci-dessus.")
        print("\n💡 Solutions possibles:")
        print("   1. Installer MySQL manuellement")
        print("   2. Vérifier les paramètres de connexion")
        print("   3. Utiliser SQLite temporairement")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
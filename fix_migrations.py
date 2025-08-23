#!/usr/bin/env python
"""
Script de réparation des migrations
Résout le problème "no such table: authentication_customuser"
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def print_step(step, description):
    """Afficher une étape"""
    print(f"\n{'='*60}")
    print(f"🔧 ÉTAPE {step}: {description}")
    print('='*60)

def run_command(command, description):
    """Exécuter une commande"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                for line in lines[-3:]:
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print(f"❌ {description} - Erreur")
            if result.stderr.strip():
                print(f"   Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    """Fonction principale de réparation"""
    print("="*70)
    print("🔧 RÉPARATION DES MIGRATIONS - GESTION DES ALERTES")
    print("   Résolution du problème: no such table: authentication_customuser")
    print("="*70)
    
    # Étape 1: Arrêter le serveur s'il tourne
    print_step(1, "ARRÊT DU SERVEUR")
    print("⏹️  Si le serveur Django tourne, appuyez sur Ctrl+C pour l'arrêter")
    input("Appuyez sur Entrée quand le serveur est arrêté...")
    
    # Étape 2: Nettoyer les anciens fichiers
    print_step(2, "NETTOYAGE DES FICHIERS")
    
    # Supprimer l'ancienne base SQLite
    sqlite_files = ["db.sqlite3", "db.sqlite3-journal"]
    for sqlite_file in sqlite_files:
        if Path(sqlite_file).exists():
            Path(sqlite_file).unlink()
            print(f"🗑️  Supprimé: {sqlite_file}")
    
    # Nettoyer les migrations
    migration_dirs = [
        "apps/authentication/migrations",
        "apps/alertes/migrations", 
        "apps/dashboard/migrations"
    ]
    
    for migration_dir in migration_dirs:
        migration_path = Path(migration_dir)
        if migration_path.exists():
            print(f"🧹 Nettoyage: {migration_dir}")
            for file in migration_path.glob("*.py"):
                if file.name != "__init__.py":
                    file.unlink()
                    print(f"   Supprimé: {file.name}")
    
    # Nettoyer les caches Python
    cache_dirs = []
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_dirs.append(Path(root) / dir_name)
    
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"🧹 Cache supprimé: {cache_dir}")
        except:
            pass
    
    # Étape 3: Créer les nouvelles migrations
    print_step(3, "CRÉATION DES NOUVELLES MIGRATIONS")
    
    # Créer les migrations pour chaque app
    apps = ["authentication", "alertes", "dashboard"]
    
    for app in apps:
        run_command(f"py manage.py makemigrations {app}", f"Migrations pour {app}")
    
    # Migrations générales
    run_command("py manage.py makemigrations", "Migrations générales")
    
    # Étape 4: Appliquer les migrations
    print_step(4, "APPLICATION DES MIGRATIONS")
    
    if run_command("py manage.py migrate", "Application des migrations"):
        print("✅ Migrations appliquées avec succès!")
    else:
        print("❌ Erreur lors des migrations")
        print("\n💡 Si vous utilisez MySQL, essayez:")
        print("   py setup_mysql.py")
        return
    
    # Étape 5: Créer un superutilisateur
    print_step(5, "CRÉATION DU SUPERUTILISATEUR")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Vérifier si un superutilisateur existe
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Un superutilisateur existe déjà")
        else:
            # Créer un superutilisateur automatiquement
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
            print("✅ Superutilisateur créé:")
            print("   👤 Nom d'utilisateur: admin")
            print("   🔑 Mot de passe: admin123")
    
    except Exception as e:
        print(f"⚠️  Erreur lors de la création du superutilisateur: {e}")
        print("💡 Créez-le manuellement avec: py manage.py createsuperuser")
    
    # Étape 6: Test de l'application
    print_step(6, "TEST DE L'APPLICATION")
    
    try:
        from django.contrib.auth import get_user_model
        from apps.alertes.models import Alerte
        
        User = get_user_model()
        users_count = User.objects.count()
        alertes_count = Alerte.objects.count()
        
        print(f"✅ Base de données fonctionnelle:")
        print(f"   👥 Utilisateurs: {users_count}")
        print(f"   🚨 Alertes: {alertes_count}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return
    
    # Résumé final
    print("\n" + "="*70)
    print("🎉 RÉPARATION TERMINÉE AVEC SUCCÈS!")
    print("="*70)
    
    print("\n✅ Problèmes résolus:")
    print("   ✅ Table authentication_customuser créée")
    print("   ✅ Toutes les migrations appliquées")
    print("   ✅ Base de données fonctionnelle")
    print("   ��� Superutilisateur disponible")
    
    print("\n🌐 Pour accéder à l'application:")
    print("   1. Démarrez le serveur: py manage.py runserver")
    print("   2. Ouvrez: http://127.0.0.1:8000/")
    print("   3. Connectez-vous avec: admin / admin123")
    
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
        print("\n✅ Réparation terminée!")
        print("Vous pouvez maintenant démarrer le serveur avec: py manage.py runserver")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
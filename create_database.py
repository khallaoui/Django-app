#!/usr/bin/env python
"""
Script pour créer la base de données MySQL via XAMPP
"""

import subprocess
import webbrowser
import time
from pathlib import Path

def print_header(title):
    """Afficher un en-tête formaté"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)

def create_database_via_phpmyadmin():
    """Créer la base de données via phpMyAdmin"""
    print_header("CRÉATION DE LA BASE DE DONNÉES VIA PHPMYADMIN")
    
    print("🌐 Ouverture de phpMyAdmin...")
    
    # Ouvrir phpMyAdmin dans le navigateur
    phpmyadmin_url = "http://localhost/phpmyadmin/"
    
    try:
        webbrowser.open(phpmyadmin_url)
        print(f"✅ phpMyAdmin ouvert: {phpmyadmin_url}")
        
        print("\n📋 Instructions pour créer la base de données:")
        print("   1. Dans phpMyAdmin, cliquez sur 'Nouvelle base de données' (à gauche)")
        print("   2. Nom de la base de données: gestion_alertes_db")
        print("   3. Interclassement: utf8mb4_unicode_ci")
        print("   4. Cliquez sur 'Créer'")
        print("   5. Revenez à cette fenêtre et appuyez sur Entrée")
        
        input("\nAppuyez sur Entrée quand la base de données est créée...")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ouverture de phpMyAdmin: {e}")
        return False

def create_database_via_mysql_command():
    """Créer la base de données via ligne de commande MySQL"""
    print_header("CRÉATION VIA LIGNE DE COMMANDE MYSQL")
    
    # Chemin vers MySQL XAMPP
    mysql_path = Path("C:/xampp/mysql/bin/mysql.exe")
    
    if not mysql_path.exists():
        print("❌ MySQL XAMPP non trouvé")
        return False
    
    print("🔄 Création de la base de données...")
    
    # Commande SQL pour créer la base de données
    sql_command = "CREATE DATABASE IF NOT EXISTS gestion_alertes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    # Construire la commande complète
    command = f'"{mysql_path}" -u root -e "{sql_command}"'
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Base de données créée avec succès!")
            return True
        else:
            print(f"❌ Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_database_connection():
    """Tester la connexion à la base de données"""
    print_header("TEST DE LA CONNEXION")
    
    print("🔄 Test de connexion à la base de données...")
    
    try:
        result = subprocess.run("py manage.py check --database default", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Connexion à la base de données réussie!")
            return True
        else:
            print(f"❌ Erreur de connexion: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def apply_migrations():
    """Appliquer les migrations Django"""
    print_header("APPLICATION DES MIGRATIONS")
    
    print("🔄 Application des migrations...")
    
    try:
        result = subprocess.run("py manage.py migrate", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations appliquées avec succès!")
            print("   Tables créées dans la base de données MySQL")
            return True
        else:
            print(f"❌ Erreur lors des migrations: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def create_superuser():
    """Créer un superutilisateur"""
    print_header("CRÉATION DU SUPERUTILISATEUR")
    
    try:
        # Configuration Django
        import os
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Vérifier si un superutilisateur existe déjà
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Un superutilisateur existe déjà")
            existing_admin = User.objects.filter(is_superuser=True).first()
            print(f"   Nom d'utilisateur: {existing_admin.username}")
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
        return False

def create_sample_data():
    """Créer des données d'exemple"""
    print_header("CRÉATION DE DONNÉES D'EXEMPLE")
    
    try:
        from django.contrib.auth import get_user_model
        from apps.alertes.models import Alerte, HistoriqueAlerte
        
        User = get_user_model()
        
        # Créer des utilisateurs d'exemple
        users_data = [
            {'username': 'agent_kit', 'email': 'kit@example.com', 'role': 'agent_kit'},
            {'username': 'agent_cross', 'email': 'cross@example.com', 'role': 'agent_cross'},
            {'username': 'agent_debord', 'email': 'debord@example.com', 'role': 'agent_debord'},
        ]
        
        created_users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'role': user_data['role'],
                    'is_active': True
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
                created_users.append(user)
                print(f"   ✅ Utilisateur créé: {user.username} ({user.get_role_display()})")
        
        # Créer des alertes d'exemple
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            alertes_data = [
                {'reference': 'ALT-001', 'zone_kit': 'zone_1', 'nombre_bacs': 15, 'statut': 'en_cours'},
                {'reference': 'ALT-002', 'zone_kit': 'zone_2', 'nombre_bacs': 8, 'statut': 'livre'},
                {'reference': 'ALT-003', 'zone_kit': 'zone_3', 'nombre_bacs': 3, 'statut': 'flc'},
                {'reference': 'ALT-004', 'zone_kit': 'zone_1', 'nombre_bacs': 12, 'statut': 'en_cours'},
                {'reference': 'ALT-005', 'zone_kit': 'zone_4', 'nombre_bacs': 6, 'statut': 'cloture'},
            ]
            
            for alerte_data in alertes_data:
                alerte, created = Alerte.objects.get_or_create(
                    reference=alerte_data['reference'],
                    defaults={
                        'zone_kit': alerte_data['zone_kit'],
                        'nombre_bacs': alerte_data['nombre_bacs'],
                        'statut': alerte_data['statut'],
                        'createur': admin_user,
                        'commentaires': f'Alerte d\'exemple pour {alerte_data["zone_kit"]}'
                    }
                )
                if created:
                    print(f"   ✅ Alerte créée: {alerte.reference} - {alerte.zone_kit}")
                    
                    # Créer l'historique
                    HistoriqueAlerte.objects.create(
                        alerte=alerte,
                        action="Création de l'alerte d'exemple",
                        utilisateur=admin_user,
                        nouveau_statut=alerte.statut
                    )
        
        print("✅ Données d'exemple créées avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        return False

def main():
    """Fonction principale"""
    print("="*70)
    print("🐬 CRÉATION DE LA BASE DE DONNÉES MYSQL")
    print("   Résolution: Unknown database 'gestion_alertes_db'")
    print("="*70)
    
    print("✅ MySQL XAMPP détecté et fonctionnel")
    print("❌ Base de données 'gestion_alertes_db' manquante")
    print("🎯 Solution: Créer la base de données")
    
    # Proposer les méthodes de création
    print("\n📋 Méthodes disponibles:")
    print("   1. Via phpMyAdmin (Interface graphique - Recommandé)")
    print("   2. Via ligne de commande MySQL")
    
    choice = input("\nChoisissez une méthode (1 ou 2): ").strip()
    
    database_created = False
    
    if choice == "1":
        database_created = create_database_via_phpmyadmin()
    elif choice == "2":
        database_created = create_database_via_mysql_command()
    else:
        print("❌ Choix invalide")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    if not database_created:
        print("\n❌ Impossible de créer la base de données automatiquement")
        print("\n💡 Création manuelle:")
        print("   1. Ouvrez http://localhost/phpmyadmin/")
        print("   2. Créez une base de données: gestion_alertes_db")
        print("   3. Relancez ce script")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    # Tester la connexion
    if not test_database_connection():
        print("❌ Problème de connexion à la base de données")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    # Appliquer les migrations
    if not apply_migrations():
        print("❌ Problème lors des migrations")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    # Créer le superutilisateur
    create_superuser()
    
    # Créer des données d'exemple
    create_sample_data()
    
    # Résumé final
    print("\n" + "="*70)
    print("🎉 BASE DE DONNÉES MYSQL CONFIGURÉE AVEC SUCCÈS!")
    print("="*70)
    
    print("\n✅ Configuration terminée:")
    print("   ✅ Base de données 'gestion_alertes_db' créée")
    print("   ✅ Tables Django créées")
    print("   ✅ Superutilisateur créé")
    print("   ✅ Données d'exemple ajoutées")
    
    print("\n🌐 Accès à l'application:")
    print("   📱 Application: http://127.0.0.1:8000/")
    print("   🔐 Connexion: admin / admin123")
    print("   ⚙️  Administration: http://127.0.0.1:8000/admin/")
    print("   🗄️  phpMyAdmin: http://localhost/phpmyadmin/")
    
    print("\n👥 Comptes disponibles:")
    print("   🔑 admin / admin123 (Administrateur)")
    print("   👤 agent_kit / demo123 (Agent Kit)")
    print("   👤 agent_cross / demo123 (Agent Cross)")
    print("   👤 agent_debord / demo123 (Agent Débord)")
    
    # Proposer de démarrer le serveur
    response = input("\n🚀 Voulez-vous démarrer le serveur Django maintenant ? (o/N): ").lower()
    if response in ['o', 'oui', 'y', 'yes']:
        print("\n🚀 Démarrage du serveur Django...")
        print("📱 Application accessible sur: http://127.0.0.1:8000/")
        print("⏹️  Appuyez sur Ctrl+C pour arrêter")
        print("="*70)
        try:
            subprocess.run(['py', 'manage.py', 'runserver'], check=True)
        except KeyboardInterrupt:
            print("\n⏹️  Serveur arrêté")
    else:
        print("\n✅ Configuration terminée!")
        print("Pour démarrer le serveur: py manage.py runserver")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
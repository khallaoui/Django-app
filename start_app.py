#!/usr/bin/env python
"""
Script de démarrage rapide pour l'application Django de gestion des alertes
Ce script automatise les étapes de configuration initiale
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Exécuter une commande et afficher le résultat"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Erreur")
            if result.stderr.strip():
                print(f"   Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def check_python_version():
    """Vérifier la version de Python"""
    print("🔍 Vérification de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Version trop ancienne (requis: 3.8+)")
        return False

def install_requirements():
    """Installer les dépendances"""
    if Path('requirements.txt').exists():
        return run_command('pip install -r requirements.txt', 'Installation des dépendances')
    else:
        print("❌ Fichier requirements.txt non trouvé")
        return False

def setup_database():
    """Configurer la base de données"""
    print("\n🗄️  Configuration de la base de données...")
    
    # Makemigrations
    if not run_command('python manage.py makemigrations', 'Création des migrations'):
        return False
    
    # Migrate
    if not run_command('python manage.py migrate', 'Application des migrations'):
        return False
    
    return True

def create_superuser():
    """Créer un superutilisateur (interactif)"""
    print("\n👤 Création d'un superutilisateur...")
    print("Vous allez être invité à créer un compte administrateur.")
    
    try:
        subprocess.run(['python', 'manage.py', 'createsuperuser'], check=True)
        print("✅ Superutilisateur créé avec succès")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de la création du superutilisateur")
        return False
    except KeyboardInterrupt:
        print("\n⚠️  Création du superutilisateur annulée")
        return False

def create_sample_data():
    """Créer des données d'exemple"""
    print("\n📊 Création de données d'exemple...")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        from apps.alertes.models import Alerte, HistoriqueAlerte
        
        User = get_user_model()
        
        # Créer des utilisateurs d'exemple
        users_data = [
            {'username': 'agent_kit_1', 'email': 'kit1@example.com', 'role': 'agent_kit'},
            {'username': 'agent_cross_1', 'email': 'cross1@example.com', 'role': 'agent_cross'},
            {'username': 'agent_debord_1', 'email': 'debord1@example.com', 'role': 'agent_debord'},
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
        if created_users:
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
                        'createur': created_users[0],
                        'commentaires': f'Alerte d\'exemple pour {alerte_data["zone_kit"]}'
                    }
                )
                if created:
                    print(f"   ✅ Alerte créée: {alerte.reference} - {alerte.zone_kit}")
                    
                    # Créer l'historique
                    HistoriqueAlerte.objects.create(
                        alerte=alerte,
                        action="Création de l'alerte d'exemple",
                        utilisateur=created_users[0],
                        nouveau_statut=alerte.statut
                    )
        
        print("✅ Données d'exemple créées avec succès")
        print("\n📝 Comptes de démonstration créés:")
        print("   - agent_kit_1 / demo123")
        print("   - agent_cross_1 / demo123")
        print("   - agent_debord_1 / demo123")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données d'exemple: {e}")
        return False

def run_checks():
    """Exécuter les vérifications"""
    print("\n🔍 Exécution des vérifications...")
    return run_command('python check_app.py', 'Vérifications de l\'application')

def start_server():
    """Démarrer le serveur de développement"""
    print("\n🚀 Démarrage du serveur de développement...")
    print("Le serveur sera accessible à l'adresse: http://127.0.0.1:8000/")
    print("Appuyez sur Ctrl+C pour arrêter le serveur")
    
    try:
        subprocess.run(['python', 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Serveur arrêté")

def main():
    """Fonction principale"""
    print("=" * 70)
    print("🚀 DÉMARRAGE RAPIDE - APPLICATION GESTION DES ALERTES")
    print("=" * 70)
    
    # Vérifications préliminaires
    if not check_python_version():
        return
    
    if not Path('manage.py').exists():
        print("❌ Fichier manage.py non trouvé. Êtes-vous dans le bon répertoire ?")
        return
    
    # Étapes de configuration
    steps = [
        ("Installation des dépendances", install_requirements),
        ("Configuration de la base de données", setup_database),
        ("Vérifications de l'application", run_checks),
    ]
    
    print("\n🔧 Configuration automatique...")
    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        if not step_func():
            print(f"\n❌ Échec à l'étape: {step_name}")
            print("Veuillez corriger les erreurs avant de continuer.")
            return
    
    # Création du superutilisateur (optionnel)
    print(f"\n{'='*50}")
    print("👤 Création d'un compte administrateur")
    print("Cette étape est optionnelle mais recommandée.")
    
    response = input("Voulez-vous créer un superutilisateur maintenant ? (o/N): ").lower()
    if response in ['o', 'oui', 'y', 'yes']:
        create_superuser()
    
    # Création de données d'exemple (optionnel)
    print(f"\n{'='*50}")
    print("📊 Données d'exemple")
    print("Cela créera des utilisateurs et alertes de démonstration.")
    
    response = input("Voulez-vous créer des données d'exemple ? (o/N): ").lower()
    if response in ['o', 'oui', 'y', 'yes']:
        create_sample_data()
    
    # Configuration terminée
    print("\n" + "=" * 70)
    print("🎉 CONFIGURATION TERMINÉE AVEC SUCCÈS!")
    print("=" * 70)
    
    print("\n📋 Résumé:")
    print("✅ Dépendances installées")
    print("✅ Base de données configurée")
    print("✅ Application vérifiée")
    
    print("\n🌐 Accès à l'application:")
    print("   - Interface web: http://127.0.0.1:8000/")
    print("   - Administration: http://127.0.0.1:8000/admin/")
    
    print("\n📚 Prochaines étapes:")
    print("   1. Démarrer le serveur: python manage.py runserver")
    print("   2. Ouvrir votre navigateur sur http://127.0.0.1:8000/")
    print("   3. Se connecter avec vos identifiants")
    
    # Proposer de démarrer le serveur
    print(f"\n{'='*50}")
    response = input("Voulez-vous démarrer le serveur maintenant ? (o/N): ").lower()
    if response in ['o', 'oui', 'y', 'yes']:
        start_server()
    else:
        print("\n✅ Configuration terminée. Vous pouvez démarrer le serveur avec:")
        print("   python manage.py runserver")

if __name__ == "__main__":
    main()
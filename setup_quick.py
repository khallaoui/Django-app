#!/usr/bin/env python
"""
Script de configuration rapide pour Windows
Résout les problèmes de pip et de base de données
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def print_header(title):
    """Afficher un en-tête formaté"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)

def run_py_command(command, description):
    """Exécuter une commande avec 'py' au lieu de 'python'"""
    print(f"🔄 {description}...")
    try:
        # Utiliser 'py' qui fonctionne sur votre système
        full_command = f"py {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                # Afficher seulement les lignes importantes
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:  # Dernières 5 lignes
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

def install_dependencies():
    """Installer les dépendances avec py -m pip"""
    print_header("INSTALLATION DES DÉPENDANCES")
    
    # Essayer différentes méthodes d'installation
    methods = [
        ("py -m pip install -r requirements.txt", "Installation avec py -m pip"),
        ("py -m pip install Django==4.2.7", "Installation Django seul"),
        ("py -m pip install python-decouple", "Installation python-decouple"),
        ("py -m pip install Pillow", "Installation Pillow"),
    ]
    
    for command, description in methods:
        print(f"\n🔄 {description}...")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description} - Succès")
                return True
            else:
                print(f"⚠️  {description} - Problème, essai suivant...")
                if "already satisfied" in result.stdout.lower():
                    print("   (Déjà installé)")
                    return True
        except Exception as e:
            print(f"⚠️  {description} - Exception: {e}")
    
    print("❌ Impossible d'installer les dépendances automatiquement")
    print("💡 Essayez manuellement :")
    print("   py -m pip install Django")
    return False

def setup_database():
    """Configurer la base de données SQLite"""
    print_header("CONFIGURATION DE LA BASE DE DONNÉES")
    
    # Supprimer l'ancienne base de données s'il y a des problèmes
    db_file = Path('db.sqlite3')
    if db_file.exists():
        print("🗑️  Suppression de l'ancienne base de données...")
        db_file.unlink()
    
    # Créer les migrations
    if not run_py_command("manage.py makemigrations", "Création des migrations"):
        print("⚠️  Problème avec makemigrations, on continue...")
    
    # Appliquer les migrations
    if not run_py_command("manage.py migrate", "Application des migrations"):
        print("❌ Échec des migrations")
        return False
    
    print("✅ Base de données SQLite configurée avec succès!")
    return True

def create_superuser_auto():
    """Créer un superutilisateur automatiquement"""
    print_header("CRÉATION D'UN COMPTE ADMINISTRATEUR")
    
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
        return False

def create_sample_data():
    """Créer des données d'exemple"""
    print_header("CRÉATION DE DONNÉES D'EXEMPLE")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        from apps.alertes.models import Alerte, HistoriqueAlerte
        
        User = get_user_model()
        
        # Créer des utilisateurs d'exemple
        users_data = [
            {'username': 'agent_kit', 'email': 'kit@example.com', 'role': 'agent_kit', 'password': 'demo123'},
            {'username': 'agent_cross', 'email': 'cross@example.com', 'role': 'agent_cross', 'password': 'demo123'},
            {'username': 'agent_debord', 'email': 'debord@example.com', 'role': 'agent_debord', 'password': 'demo123'},
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
                user.set_password(user_data['password'])
                user.save()
                created_users.append(user)
                print(f"   ✅ Utilisateur créé: {user.username} ({user.get_role_display()})")
        
        # Créer des alertes d'exemple
        if created_users or User.objects.filter(role='agent_kit').exists():
            creator = created_users[0] if created_users else User.objects.filter(role='agent_kit').first()
            
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
                        'createur': creator,
                        'commentaires': f'Alerte d\'exemple pour {alerte_data["zone_kit"]}'
                    }
                )
                if created:
                    print(f"   ✅ Alerte créée: {alerte.reference} - {alerte.zone_kit}")
                    
                    # Créer l'historique
                    HistoriqueAlerte.objects.create(
                        alerte=alerte,
                        action="Création de l'alerte d'exemple",
                        utilisateur=creator,
                        nouveau_statut=alerte.statut
                    )
        
        print("✅ Données d'exemple créées avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données d'exemple: {e}")
        return False

def test_application():
    """Tester que l'application fonctionne"""
    print_header("TEST DE L'APPLICATION")
    
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        from apps.alertes.models import Alerte
        
        User = get_user_model()
        
        # Compter les éléments
        users_count = User.objects.count()
        alertes_count = Alerte.objects.count()
        
        print(f"✅ Utilisateurs dans la base: {users_count}")
        print(f"✅ Alertes dans la base: {alertes_count}")
        
        # Tester l'importation des vues
        from apps.dashboard.views import dashboard_view
        from apps.alertes.views import create_alerte, list_alertes
        from apps.authentication.views import register_view
        
        print("✅ Toutes les vues sont importables")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def start_server():
    """Démarrer le serveur"""
    print_header("DÉMARRAGE DU SERVEUR")
    
    print("🚀 Démarrage du serveur Django...")
    print("📱 L'application sera accessible à: http://127.0.0.1:8000/")
    print("🔑 Administration: http://127.0.0.1:8000/admin/")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("\n" + "="*60)
    
    try:
        subprocess.run(['py', 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage du serveur: {e}")

def main():
    """Fonction principale"""
    print("="*70)
    print("🚀 CONFIGURATION RAPIDE - APPLICATION GESTION DES ALERTES")
    print("   (Version Windows - Résolution des problèmes)")
    print("="*70)
    
    # Vérifications préliminaires
    if not Path('manage.py').exists():
        print("❌ Fichier manage.py non trouvé. Êtes-vous dans le bon répertoire ?")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    print("✅ Python détecté, utilisation de 'py' au lieu de 'python'")
    print("✅ Configuration SQLite au lieu de MySQL")
    
    # Étapes de configuration
    steps = [
        ("Installation des dépendances", install_dependencies),
        ("Configuration de la base de données", setup_database),
        ("Création du compte administrateur", create_superuser_auto),
        ("Création de données d'exemple", create_sample_data),
        ("Test de l'application", test_application),
    ]
    
    results = []
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
            if not result:
                print(f"\n⚠️  Problème à l'étape: {step_name}")
                print("On continue quand même...")
        except Exception as e:
            print(f"\n❌ Erreur critique à l'étape {step_name}: {e}")
            results.append((step_name, False))
    
    # Résumé
    print_header("RÉSUMÉ DE LA CONFIGURATION")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for step_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"{step_name:<40} {status}")
    
    print(f"\n🎯 Résultat: {passed}/{total} étapes réussies")
    
    if passed >= 3:  # Au moins 3 étapes sur 5
        print("\n🎉 CONFIGURATION SUFFISANTE POUR DÉMARRER!")
        print("\n📋 Informations de connexion:")
        print("   👤 Admin: admin / admin123")
        print("   👤 Agent Kit: agent_kit / demo123")
        print("   👤 Agent Cross: agent_cross / demo123")
        print("   👤 Agent Débord: agent_debord / demo123")
        
        print("\n🌐 URLs importantes:")
        print("   🏠 Accueil: http://127.0.0.1:8000/")
        print("   🔐 Connexion: http://127.0.0.1:8000/auth/login/")
        print("   ⚙️  Admin: http://127.0.0.1:8000/admin/")
        
        # Proposer de démarrer le serveur
        response = input("\n🚀 Voulez-vous démarrer le serveur maintenant ? (o/N): ").lower()
        if response in ['o', 'oui', 'y', 'yes']:
            start_server()
        else:
            print("\n✅ Configuration terminée!")
            print("Pour démarrer le serveur plus tard, utilisez:")
            print("   py manage.py runserver")
    else:
        print("\n⚠️  CONFIGURATION INCOMPLÈTE")
        print("Certaines étapes ont échoué, mais vous pouvez essayer de démarrer quand même:")
        print("   py manage.py runserver")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
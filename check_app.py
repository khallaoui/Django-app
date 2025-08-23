#!/usr/bin/env python
"""
Script de vérification de l'application Django de gestion des alertes
Ce script vérifie que tous les composants sont correctement connectés
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

def check_models():
    """Vérifier les modèles"""
    print("🔍 Vérification des modèles...")
    
    try:
        from apps.authentication.models import CustomUser
        from apps.alertes.models import Alerte, HistoriqueAlerte, StockDebord
        
        print("✅ Modèle CustomUser importé avec succès")
        print("✅ Modèle Alerte importé avec succès")
        print("✅ Modèle HistoriqueAlerte importé avec succès")
        print("✅ Modèle StockDebord importé avec succès")
        
        # Vérifier les choix des modèles
        print(f"   - Rôles utilisateur: {CustomUser.ROLE_CHOICES}")
        print(f"   - Statuts alerte: {Alerte.STATUS_CHOICES}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'importation des modèles: {e}")
        return False

def check_views():
    """Vérifier les vues"""
    print("\n🔍 Vérification des vues...")
    
    try:
        from apps.authentication.views import register_view
        from apps.alertes.views import create_alerte, list_alertes, update_statut
        from apps.dashboard.views import dashboard_view
        
        print("✅ Vues d'authentification importées avec succès")
        print("✅ Vues d'alertes importées avec succès")
        print("✅ Vues de dashboard importées avec succès")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'importation des vues: {e}")
        return False

def check_forms():
    """Vérifier les formulaires"""
    print("\n🔍 Vérification des formulaires...")
    
    try:
        from apps.authentication.forms import CustomUserCreationForm
        from apps.alertes.forms import AlerteForm
        
        print("✅ Formulaires d'authentification importés avec succès")
        print("✅ Formulaires d'alertes importés avec succès")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'importation des formulaires: {e}")
        return False

def check_urls():
    """Vérifier la configuration des URLs"""
    print("\n🔍 Vérification des URLs...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Tester les URLs principales
        urls_to_test = [
            ('dashboard', 'Dashboard'),
            ('login', 'Connexion'),
            ('register', 'Inscription'),
            ('create_alerte', 'Création alerte'),
            ('list_alertes', 'Liste alertes'),
        ]
        
        for url_name, description in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ URL '{url_name}' ({description}): {url}")
            except Exception as e:
                print(f"❌ Erreur URL '{url_name}': {e}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des URLs: {e}")
        return False

def check_templates():
    """Vérifier les templates"""
    print("\n🔍 Vérification des templates...")
    
    templates_to_check = [
        'base.html',
        'registration/login.html',
        'registration/register.html',
        'dashboard/dashboard.html',
        'alertes/create_alert.html',
        'alertes/list_alerts.html',
    ]
    
    template_dir = Path('templates')
    all_exist = True
    
    for template in templates_to_check:
        template_path = template_dir / template
        if template_path.exists():
            print(f"✅ Template trouvé: {template}")
        else:
            print(f"❌ Template manquant: {template}")
            all_exist = False
    
    return all_exist

def check_static_files():
    """Vérifier les fichiers statiques"""
    print("\n🔍 Vérification des fichiers statiques...")
    
    static_files_to_check = [
        'static/css/style.css',
        'static/js/main.js',
    ]
    
    all_exist = True
    
    for static_file in static_files_to_check:
        static_path = Path(static_file)
        if static_path.exists():
            print(f"✅ Fichier statique trouvé: {static_file}")
        else:
            print(f"❌ Fichier statique manquant: {static_file}")
            all_exist = False
    
    return all_exist

def check_settings():
    """Vérifier la configuration"""
    print("\n🔍 Vérification de la configuration...")
    
    try:
        from django.conf import settings
        
        # Vérifier les applications installées
        required_apps = [
            'apps.authentication',
            'apps.alertes',
            'apps.dashboard',
        ]
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✅ Application installée: {app}")
            else:
                print(f"❌ Application manquante: {app}")
        
        # Vérifier la configuration de la base de données
        db_config = settings.DATABASES['default']
        print(f"✅ Base de données configurée: {db_config['ENGINE']}")
        print(f"   - Nom: {db_config['NAME']}")
        print(f"   - Host: {db_config['HOST']}")
        
        # Vérifier le modèle utilisateur personnalisé
        if hasattr(settings, 'AUTH_USER_MODEL'):
            print(f"✅ Modèle utilisateur personnalisé: {settings.AUTH_USER_MODEL}")
        else:
            print("❌ Modèle utilisateur personnalisé non configuré")
        
        # Vérifier les URLs de redirection
        print(f"✅ LOGIN_URL: {settings.LOGIN_URL}")
        print(f"✅ LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
        print(f"✅ LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la configuration: {e}")
        return False

def check_database_connection():
    """Vérifier la connexion à la base de données"""
    print("\n🔍 Vérification de la connexion à la base de données...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result:
            print("✅ Connexion à la base de données réussie")
            return True
        else:
            print("❌ Problème de connexion à la base de données")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        print("   Note: Assurez-vous que MySQL est démarré et que les paramètres sont corrects")
        return False

def main():
    """Fonction principale de vérification"""
    print("=" * 60)
    print("🚀 VÉRIFICATION DE L'APPLICATION DJANGO - GESTION DES ALERTES")
    print("=" * 60)
    
    checks = [
        check_settings,
        check_models,
        check_views,
        check_forms,
        check_urls,
        check_templates,
        check_static_files,
        check_database_connection,
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 SUCCÈS: Tous les tests sont passés ({passed}/{total})")
        print("\n✅ Votre application Django est correctement configurée!")
        print("\n🚀 Pour démarrer l'application:")
        print("   1. python manage.py makemigrations")
        print("   2. python manage.py migrate")
        print("   3. python manage.py createsuperuser")
        print("   4. python manage.py runserver")
    else:
        print(f"⚠️  ATTENTION: {total - passed} test(s) ont échoué ({passed}/{total})")
        print("\n🔧 Veuillez corriger les erreurs mentionnées ci-dessus")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
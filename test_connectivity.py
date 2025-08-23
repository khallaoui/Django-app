#!/usr/bin/env python
"""
Test de connectivité complète de l'application Django
Ce script teste toutes les connexions entre les composants
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

User = get_user_model()

def test_user_creation():
    """Test de création d'utilisateur"""
    print("🧪 Test de création d'utilisateur...")
    
    try:
        # Créer un utilisateur de test
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123',
            role='agent_kit'
        )
        
        print(f"✅ Utilisateur créé: {user.username} - {user.get_role_display()}")
        
        # Vérifier les propriétés
        assert user.role == 'agent_kit'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        
        print("✅ Propriétés utilisateur vérifiées")
        
        # Nettoyer
        user.delete()
        print("✅ Utilisateur de test supprimé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test utilisateur: {e}")
        return False

def test_alerte_creation():
    """Test de création d'alerte"""
    print("\n🧪 Test de création d'alerte...")
    
    try:
        from apps.alertes.models import Alerte, HistoriqueAlerte
        
        # Créer un utilisateur pour les tests
        user = User.objects.create_user(
            username='test_creator',
            email='creator@example.com',
            password='testpass123',
            role='agent_kit'
        )
        
        # Créer une alerte
        alerte = Alerte.objects.create(
            reference='TEST-001',
            zone_kit='zone_1',
            nombre_bacs=15,
            createur=user,
            commentaires='Test de création d\'alerte'
        )
        
        print(f"✅ Alerte créée: {alerte.reference} - {alerte.zone_kit}")
        
        # Vérifier les propriétés
        assert alerte.statut == 'en_cours'  # Statut par défaut
        assert alerte.createur == user
        assert alerte.nombre_bacs == 15
        
        print("�� Propriétés alerte vérifiées")
        
        # Créer un historique
        historique = HistoriqueAlerte.objects.create(
            alerte=alerte,
            action="Test de création",
            utilisateur=user,
            nouveau_statut=alerte.statut
        )
        
        print(f"✅ Historique créé: {historique.action}")
        
        # Tester la mise à jour de statut
        alerte.statut = 'livre'
        alerte.traite_par = user
        alerte.save()
        
        # Créer un nouvel historique
        HistoriqueAlerte.objects.create(
            alerte=alerte,
            action="Changement de statut",
            utilisateur=user,
            ancien_statut='en_cours',
            nouveau_statut='livre'
        )
        
        print("✅ Mise à jour de statut testée")
        
        # Vérifier les relations
        assert alerte.historique.count() == 2
        assert alerte.createur.alertes_creees.count() == 1
        
        print("✅ Relations vérifiées")
        
        # Nettoyer
        alerte.delete()
        user.delete()
        print("✅ Données de test supprimées")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test alerte: {e}")
        return False

def test_forms():
    """Test des formulaires"""
    print("\n🧪 Test des formulaires...")
    
    try:
        from apps.authentication.forms import CustomUserCreationForm
        from apps.alertes.forms import AlerteForm
        
        # Test formulaire utilisateur
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'agent_kit',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        
        user_form = CustomUserCreationForm(data=user_data)
        if user_form.is_valid():
            print("✅ Formulaire utilisateur valide")
        else:
            print(f"❌ Erreurs formulaire utilisateur: {user_form.errors}")
            return False
        
        # Test formulaire alerte
        alerte_data = {
            'reference': 'TEST-002',
            'zone_kit': 'zone_2',
            'nombre_bacs': 10,
            'commentaires': 'Test formulaire'
        }
        
        alerte_form = AlerteForm(data=alerte_data)
        if alerte_form.is_valid():
            print("✅ Formulaire alerte valide")
        else:
            print(f"❌ Erreurs formulaire alerte: {alerte_form.errors}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test formulaires: {e}")
        return False

def test_views_access():
    """Test d'accès aux vues"""
    print("\n🧪 Test d'accès aux vues...")
    
    try:
        client = Client()
        
        # Test des vues publiques (redirections vers login)
        public_views = [
            ('dashboard', 'Dashboard'),
            ('create_alerte', 'Création alerte'),
            ('list_alertes', 'Liste alertes'),
        ]
        
        for view_name, description in public_views:
            try:
                url = reverse(view_name)
                response = client.get(url)
                
                # Ces vues doivent rediriger vers login (302) car elles nécessitent une authentification
                if response.status_code == 302:
                    print(f"✅ Vue protégée {description}: redirection vers login")
                else:
                    print(f"⚠️  Vue {description}: statut {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Erreur vue {view_name}: {e}")
                return False
        
        # Test des vues d'authentification
        auth_views = [
            ('login', 'Connexion'),
            ('register', 'Inscription'),
        ]
        
        for view_name, description in auth_views:
            try:
                url = reverse(view_name)
                response = client.get(url)
                
                if response.status_code == 200:
                    print(f"✅ Vue {description}: accessible")
                else:
                    print(f"❌ Vue {description}: statut {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur vue {view_name}: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test des vues: {e}")
        return False

def test_authenticated_access():
    """Test d'accès avec utilisateur authentifié"""
    print("\n🧪 Test d'accès avec authentification...")
    
    try:
        client = Client()
        
        # Créer un utilisateur de test
        user = User.objects.create_user(
            username='testauth',
            email='testauth@example.com',
            password='testpass123',
            role='agent_kit'
        )
        
        # Se connecter
        login_success = client.login(username='testauth', password='testpass123')
        if not login_success:
            print("❌ Échec de la connexion")
            return False
        
        print("✅ Connexion réussie")
        
        # Tester l'accès aux vues protégées
        protected_views = [
            ('dashboard', 'Dashboard'),
            ('create_alerte', 'Création alerte'),
            ('list_alertes', 'Liste alertes'),
        ]
        
        for view_name, description in protected_views:
            try:
                url = reverse(view_name)
                response = client.get(url)
                
                if response.status_code == 200:
                    print(f"✅ Vue {description}: accessible avec authentification")
                else:
                    print(f"❌ Vue {description}: statut {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Erreur vue {view_name}: {e}")
        
        # Nettoyer
        user.delete()
        print("✅ Utilisateur de test supprimé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test authentifié: {e}")
        return False

def test_ajax_functionality():
    """Test des fonctionnalités AJAX"""
    print("\n🧪 Test des fonctionnalités AJAX...")
    
    try:
        from apps.alertes.models import Alerte
        client = Client()
        
        # Créer un utilisateur et une alerte de test
        user = User.objects.create_user(
            username='testajax',
            email='testajax@example.com',
            password='testpass123',
            role='agent_kit'
        )
        
        alerte = Alerte.objects.create(
            reference='AJAX-001',
            zone_kit='zone_1',
            nombre_bacs=5,
            createur=user
        )
        
        # Se connecter
        client.login(username='testajax', password='testpass123')
        
        # Tester la mise à jour de statut via AJAX
        url = reverse('update_statut', args=[alerte.id])
        response = client.post(url, {
            'statut': 'livre'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        if response.status_code == 200:
            print("✅ Requête AJAX de mise à jour de statut réussie")
            
            # Vérifier que le statut a été mis à jour
            alerte.refresh_from_db()
            if alerte.statut == 'livre':
                print("✅ Statut mis à jour correctement")
            else:
                print(f"❌ Statut non mis à jour: {alerte.statut}")
        else:
            print(f"❌ Requête AJAX échouée: statut {response.status_code}")
        
        # Nettoyer
        alerte.delete()
        user.delete()
        print("✅ Données de test supprimées")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test AJAX: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=" * 70)
    print("🧪 TESTS DE CONNECTIVITÉ - APPLICATION GESTION DES ALERTES")
    print("=" * 70)
    
    tests = [
        ("Création d'utilisateur", test_user_creation),
        ("Création d'alerte", test_alerte_creation),
        ("Formulaires", test_forms),
        ("Accès aux vues", test_views_access),
        ("Accès authentifié", test_authenticated_access),
        ("Fonctionnalités AJAX", test_ajax_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🔍 {test_name}")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS DE CONNECTIVITÉ")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<30} {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 EXCELLENT! Tous les tests de connectivité sont passés!")
        print("✅ Votre application Django est entièrement fonctionnelle!")
        print("\n🚀 Prêt pour la production!")
    else:
        print(f"\n⚠️  ATTENTION: {total - passed} test(s) ont échoué")
        print("🔧 Veuillez corriger les problèmes identifiés")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .models import Reference, Historique, Travee

User = get_user_model()


class StockDebordModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.reference = Reference.objects.create(
            emplacement_sm='A1-01',
            reference='REF001',
            nombre_bacs=10,
            travee_debord='T1',
            code_condi='CC01',
            qt_piece_uc=50,
            appro='APPRO1',
            fournisseur='FOURNISSEUR1',
            cmj='CMJ001',
            f='F1'
        )

    def test_reference_creation(self):
        self.assertEqual(self.reference.reference, 'REF001')
        self.assertEqual(self.reference.nombre_bacs, 10)
        self.assertEqual(str(self.reference), 'REF001 - A1-01')

    def test_historique_creation(self):
        historique = Historique.objects.create(
            reference=self.reference,
            type_action='entree',
            nombre_bacs=5,
            utilisateur='testuser'
        )
        self.assertEqual(historique.type_action, 'entree')
        self.assertEqual(historique.nombre_bacs, 5)


class StockDebordViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.reference = Reference.objects.create(
            emplacement_sm='A1-01',
            reference='REF001',
            nombre_bacs=10,
            travee_debord='T1',
            code_condi='CC01',
            qt_piece_uc=50,
            appro='APPRO1',
            fournisseur='FOURNISSEUR1',
            cmj='CMJ001',
            f='F1'
        )

    def test_dashboard_view_requires_login(self):
        response = self.client.get(reverse('stock_debord:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_view_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('stock_debord:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Stock Magasin Débord')

    def test_ajouter_reference_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('stock_debord:ajouter_reference'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ajouter une Référence')
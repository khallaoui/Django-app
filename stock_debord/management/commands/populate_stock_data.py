from django.core.management.base import BaseCommand
from django.utils import timezone
from stock_debord.models import Reference, Travee, Historique
import random


class Command(BaseCommand):
    help = 'Populate the database with sample stock data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample stock data...')

        # Create sample travées
        travees_data = [
            {'nom': 'T1', 'capacite': 100},
            {'nom': 'T2', 'capacite': 150},
            {'nom': 'T3', 'capacite': 120},
            {'nom': 'T4', 'capacite': 80},
            {'nom': 'T5', 'capacite': 200},
        ]

        for travee_data in travees_data:
            travee, created = Travee.objects.get_or_create(
                nom=travee_data['nom'],
                defaults={'capacite': travee_data['capacite']}
            )
            if created:
                self.stdout.write(f'Created travée: {travee.nom}')

        # Create sample references
        references_data = [
            {
                'emplacement_sm': 'A1-01-001',
                'reference': 'REF001-ABC',
                'nombre_bacs': 25,
                'travee_debord': 'T1',
                'code_condi': 'CC001',
                'qt_piece_uc': 50,
                'appro': 'APPRO-001',
                'fournisseur': 'FAURECIA',
                'cmj': 'CMJ-001',
                'f': 'F1'
            },
            {
                'emplacement_sm': 'A1-02-001',
                'reference': 'REF002-DEF',
                'nombre_bacs': 15,
                'travee_debord': 'T2',
                'code_condi': 'CC002',
                'qt_piece_uc': 30,
                'appro': 'APPRO-002',
                'fournisseur': 'VALEO',
                'cmj': 'CMJ-002',
                'f': 'F2'
            },
            {
                'emplacement_sm': 'B1-01-001',
                'reference': 'REF003-GHI',
                'nombre_bacs': 40,
                'travee_debord': 'T1',
                'code_condi': 'CC003',
                'qt_piece_uc': 75,
                'appro': 'APPRO-003',
                'fournisseur': 'BOSCH',
                'cmj': 'CMJ-003',
                'f': 'F1'
            },
            {
                'emplacement_sm': 'B2-01-001',
                'reference': 'REF004-JKL',
                'nombre_bacs': 20,
                'travee_debord': 'T3',
                'code_condi': 'CC004',
                'qt_piece_uc': 40,
                'appro': 'APPRO-004',
                'fournisseur': 'CONTINENTAL',
                'cmj': 'CMJ-004',
                'f': 'F3'
            },
            {
                'emplacement_sm': 'C1-01-001',
                'reference': 'REF005-MNO',
                'nombre_bacs': 35,
                'travee_debord': 'T2',
                'code_condi': 'CC005',
                'qt_piece_uc': 60,
                'appro': 'APPRO-005',
                'fournisseur': 'MAGNA',
                'cmj': 'CMJ-005',
                'f': 'F2'
            },
        ]

        for ref_data in references_data:
            reference, created = Reference.objects.get_or_create(
                reference=ref_data['reference'],
                defaults=ref_data
            )
            if created:
                self.stdout.write(f'Created reference: {reference.reference}')
                
                # Create initial history entry
                Historique.objects.create(
                    reference=reference,
                    type_action='entree',
                    nombre_bacs=reference.nombre_bacs,
                    utilisateur='system'
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated stock data!')
        )
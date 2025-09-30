from django.core.management.base import BaseCommand
from apps.authentication.models import CustomUser
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Crée des utilisateurs de test pour chaque rôle'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Supprime et recrée les utilisateurs de test',
        )

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'consultant',
                'email': 'consultant@stellantis.com',
                'password': 'consultant123',
                'role': 'consultant',
                'first_name': 'Jean',
                'last_name': 'Cariste',
                'phone': '0612345678',
            },
            {
                'username': 'gestionnaire',
                'email': 'gestionnaire@stellantis.com',
                'password': 'gestionnaire123',
                'role': 'gestionnaire',
                'first_name': 'Marie',
                'last_name': 'Gestion',
                'phone': '0623456789',
            },
            {
                'username': 'admin',
                'email': 'admin@stellantis.com',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'Pierre',
                'last_name': 'Admin',
                'phone': '0634567890',
                'is_staff': True,
                'is_superuser': True,
            },
        ]

        if options['reset']:
            self.stdout.write(self.style.WARNING('Suppression des utilisateurs existants...'))
            for user_data in users_data:
                try:
                    user = CustomUser.objects.get(username=user_data['username'])
                    user.delete()
                    self.stdout.write(self.style.SUCCESS(f'[OK] Utilisateur {user_data["username"]} supprime'))
                except CustomUser.DoesNotExist:
                    pass

        for user_data in users_data:
            try:
                username = user_data.pop('username')
                password = user_data.pop('password')
                
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    **user_data
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'[OK] Utilisateur cree: {username} ({user.get_role_display()})'
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        f'[WARN] L\'utilisateur {username} existe deja'
                    )
                )

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('UTILISATEURS DE TEST CREES'))
        self.stdout.write('='*60)
        self.stdout.write('\nIdentifiants de connexion:\n')
        
        self.stdout.write(self.style.HTTP_INFO('1. CONSULTANT (Opérateur / Cariste)'))
        self.stdout.write('   Username: consultant')
        self.stdout.write('   Password: consultant123')
        self.stdout.write('   Permissions: Entrées/Sorties, Consultation stock\n')
        
        self.stdout.write(self.style.HTTP_INFO('2. GESTIONNAIRE DE MAGASIN'))
        self.stdout.write('   Username: gestionnaire')
        self.stdout.write('   Password: gestionnaire123')
        self.stdout.write('   Permissions: Gestion magasin, Validation mouvements\n')
        
        self.stdout.write(self.style.HTTP_INFO('3. ADMINISTRATEUR'))
        self.stdout.write('   Username: admin')
        self.stdout.write('   Password: admin123')
        self.stdout.write('   Permissions: Gestion utilisateurs, Historique complet\n')
        
        self.stdout.write('='*60)

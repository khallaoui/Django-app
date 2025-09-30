"""
Définition des permissions par rôle pour l'application.

CONSULTANT (Opérateur / Cariste):
    - Effectuer les entrées/sorties de pièces
    - Consulter uniquement le stock
    - Pas d'accès à la gestion ou aux historiques complets

GESTIONNAIRE DE MAGASIN:
    Assure la gestion globale du magasin et contrôle les mouvements de stock 
    entre l'entrepreneur et le client.
    
    - Toutes les permissions du consultant
    - Gérer le magasin (références, zones, travées)
    - Valider et assurer les mouvements d'entrées/sorties
    - Superviser les opérations
    - Consulter les historiques de mouvements complets
    - Exporter et extraire les données de stock
    - Imprimer les rapports

ADMINISTRATEUR:
    - Toutes les permissions du gestionnaire
    - Créer des comptes utilisateurs
    - Ajouter ou supprimer des comptes
    - Consulter l'historique complet des mouvements
    - Accès aux paramètres système
"""

class UserPermissions:
    """Classe utilitaire pour vérifier les permissions utilisateur"""
    
    @staticmethod
    def can_view_stock(user):
        """Tous les utilisateurs connectés peuvent consulter le stock"""
        return user.is_authenticated
    
    @staticmethod
    def can_add_movement(user):
        """Consultant, Gestionnaire et Admin peuvent ajouter des mouvements"""
        return user.is_authenticated and user.role in ['consultant', 'gestionnaire', 'admin']
    
    @staticmethod
    def can_manage_warehouse(user):
        """Gestionnaire et Admin peuvent gérer le magasin"""
        return user.is_authenticated and user.role in ['gestionnaire', 'admin']
    
    @staticmethod
    def can_validate_movements(user):
        """Gestionnaire et Admin peuvent valider les mouvements"""
        return user.is_authenticated and user.role in ['gestionnaire', 'admin']
    
    @staticmethod
    def can_view_full_history(user):
        """Gestionnaire et Admin peuvent voir l'historique complet"""
        return user.is_authenticated and user.role in ['gestionnaire', 'admin']
    
    @staticmethod
    def can_manage_users(user):
        """Seul l'Admin peut gérer les utilisateurs"""
        return user.is_authenticated and user.role == 'admin'
    
    @staticmethod
    def can_delete_user(user):
        """Seul l'Admin peut supprimer des utilisateurs"""
        return user.is_authenticated and user.role == 'admin'
    
    @staticmethod
    def can_access_admin(user):
        """Seul l'Admin peut accéder à l'interface admin Django"""
        return user.is_authenticated and user.role == 'admin'

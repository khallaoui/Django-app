from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('consultant', 'Consultant (Opérateur / Cariste)'),
        ('gestionnaire', 'Gestionnaire de magasin'),
        ('admin', 'Administrateur'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='consultant')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    def is_consultant(self):
        return self.role == 'consultant'
    
    def is_gestionnaire(self):
        return self.role == 'gestionnaire'
    
    def is_admin(self):
        return self.role == 'admin'
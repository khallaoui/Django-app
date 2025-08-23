from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('agent_kit', 'Agent Bord Kit'),
        ('agent_cross', 'Agent Cross Dock'),
        ('agent_debord', 'Agent Débord'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent_kit')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
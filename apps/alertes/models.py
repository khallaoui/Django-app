from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Alerte(models.Model):
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('livre', 'Livré'),
        ('flc', 'FLC envoyé'),
        ('cloture', 'Clôturé'),
    ]
    
    reference = models.CharField(max_length=50, verbose_name="Référence")
    zone_kit = models.CharField(max_length=20, verbose_name="Zone de Kit")
    nombre_bacs = models.IntegerField(verbose_name="Nombre de bacs restants")
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_cloture = models.DateTimeField(null=True, blank=True)
    
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertes_creees')
    traite_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertes_traitees')
    
    commentaires = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'alertes'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Alerte {self.reference} - {self.zone_kit}"

class HistoriqueAlerte(models.Model):
    alerte = models.ForeignKey(Alerte, on_delete=models.CASCADE, related_name='historique')
    action = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_modification = models.DateTimeField(auto_now_add=True)
    ancien_statut = models.CharField(max_length=20, blank=True, null=True)
    nouveau_statut = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table = 'historique_alertes'
        ordering = ['-date_modification']

class StockDebord(models.Model):
    reference = models.CharField(max_length=50)
    emplacement = models.CharField(max_length=50)
    quantite = models.IntegerField()
    date_entree = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'stock_debord'
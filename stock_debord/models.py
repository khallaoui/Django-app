from django.db import models
from django.utils import timezone


class Reference(models.Model):
    emplacement_sm = models.CharField(max_length=20, verbose_name="Emplacement SM")
    reference = models.CharField(max_length=50, verbose_name="Référence")
    nombre_bacs = models.IntegerField(verbose_name="Nombre de Bac")
    date_entree = models.DateTimeField(default=timezone.now, verbose_name="Date d'entrée")
    travee_debord = models.CharField(max_length=10, verbose_name="Travée débord")
    code_condi = models.CharField(max_length=10, verbose_name="Code condi")
    qt_piece_uc = models.IntegerField(verbose_name="Qt pièce/UC")
    appro = models.CharField(max_length=50, verbose_name="Appro")
    fournisseur = models.CharField(max_length=100, verbose_name="Fournisseur")
    cmj = models.CharField(max_length=20, verbose_name="CMJ")
    f = models.CharField(max_length=10, verbose_name="F")

    def __str__(self):
        return f"{self.reference} - {self.emplacement_sm}"

    class Meta:
        verbose_name = "Référence"
        verbose_name_plural = "Références"


class Historique(models.Model):
    TYPE_ACTION = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
    ]

    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    type_action = models.CharField(max_length=10, choices=TYPE_ACTION)
    nombre_bacs = models.IntegerField()
    date_action = models.DateTimeField(default=timezone.now)
    utilisateur = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type_action} - {self.reference.reference}"

    class Meta:
        verbose_name = "Historique"
        verbose_name_plural = "Historiques"
        ordering = ['-date_action']


class Travee(models.Model):
    nom = models.CharField(max_length=10, unique=True)
    capacite = models.IntegerField()
    references = models.ManyToManyField(Reference, through='OccupationTravee')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Travée"
        verbose_name_plural = "Travées"


class OccupationTravee(models.Model):
    travee = models.ForeignKey(Travee, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    date_occupation = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('travee', 'reference')
        verbose_name = "Occupation Travée"
        verbose_name_plural = "Occupations Travées"
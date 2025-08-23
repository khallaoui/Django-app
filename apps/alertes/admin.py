from django.contrib import admin
from .models import Alerte, HistoriqueAlerte, StockDebord

@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = ('reference', 'zone_kit', 'nombre_bacs', 'statut', 'createur', 'date_creation')
    list_filter = ('statut', 'zone_kit', 'date_creation')
    search_fields = ('reference', 'zone_kit')
    readonly_fields = ('date_creation', 'date_cloture')

@admin.register(HistoriqueAlerte)
class HistoriqueAlerteAdmin(admin.ModelAdmin):
    list_display = ('alerte', 'action', 'utilisateur', 'date_modification')
    list_filter = ('action', 'date_modification')
    readonly_fields = ('date_modification',)

@admin.register(StockDebord)
class StockDebordAdmin(admin.ModelAdmin):
    list_display = ('reference', 'emplacement', 'quantite', 'date_entree', 'date_sortie')
    list_filter = ('date_entree', 'date_sortie')
    search_fields = ('reference', 'emplacement')
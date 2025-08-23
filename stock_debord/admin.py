from django.contrib import admin
from .models import Reference, Historique, Travee, OccupationTravee


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['reference', 'emplacement_sm', 'nombre_bacs', 'travee_debord', 'date_entree']
    list_filter = ['travee_debord', 'date_entree', 'fournisseur']
    search_fields = ['reference', 'emplacement_sm', 'fournisseur']
    ordering = ['-date_entree']


@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ['reference', 'type_action', 'nombre_bacs', 'date_action', 'utilisateur']
    list_filter = ['type_action', 'date_action']
    search_fields = ['reference__reference', 'utilisateur']
    ordering = ['-date_action']


@admin.register(Travee)
class TraveeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'capacite']
    search_fields = ['nom']


@admin.register(OccupationTravee)
class OccupationTraveeAdmin(admin.ModelAdmin):
    list_display = ['travee', 'reference', 'date_occupation']
    list_filter = ['travee', 'date_occupation']
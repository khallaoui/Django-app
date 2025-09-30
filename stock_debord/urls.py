from django.urls import path
from . import views

app_name = 'stock_debord'

urlpatterns = [
    # Main dashboard and core functionality
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('ajouter/', views.AjouterReferenceView.as_view(), name='ajouter_reference'),
    path('saisie-sortie/', views.SaisieSortieView.as_view(), name='saisie_sortie'),
    path('historique/', views.HistoriqueView.as_view(), name='historique'),
    path('exporter-excel/', views.exporter_stock_excel, name='exporter_excel'),
    path('export-historique-excel/', views.export_historique_excel, name='export_historique_excel'),
    path('extraction-mouvements/', views.extraction_mouvements, name='extraction_mouvements'),
    path('gestion-references/', views.GestionReferencesView.as_view(), name='gestion_references'),
    path('modifier-reference/<int:pk>/', views.ModifierReferenceView.as_view(), name='modifier_reference'),
    path('supprimer-reference/<int:reference_id>/', views.supprimer_reference, name='supprimer_reference'),
    path('gestion-zones/', views.GestionZonesView.as_view(), name='gestion_zones'),
    path('ajouter-zone/', views.ajouter_zone, name='ajouter_zone'),
    path('modifier-zone/', views.modifier_zone, name='modifier_zone'),
    path('supprimer-zone/<int:zone_id>/', views.supprimer_zone, name='supprimer_zone'),
    path('imprimer/', views.imprimer_stock, name='imprimer_stock'),
    
    # Navbar functionality
    path('boot-kit/', views.BootKitView.as_view(), name='boot_kit'),
    path('cross-dock/', views.CrossDockView.as_view(), name='cross_dock'),
    path('map-debord/', views.MapDebordView.as_view(), name='map_debord'),
    path('flc/', views.FLCView.as_view(), name='flc'),
    path('log-ext/', views.LogExtView.as_view(), name='log_ext'),
    path('how-to-use/', views.HowToUseView.as_view(), name='how_to_use'),
    path('pagination-demo/', views.pagination_demo, name='pagination_demo'),
]
from django.urls import path
from . import views

app_name = 'stock_debord'

urlpatterns = [
    # Main dashboard and core functionality
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('ajouter/', views.AjouterReferenceView.as_view(), name='ajouter_reference'),
    path('vider-travee/', views.ViderTraveeView.as_view(), name='vider_travee'),
    path('saisie-sortie/', views.SaisieSortieView.as_view(), name='saisie_sortie'),
    path('historique/', views.HistoriqueView.as_view(), name='historique'),
    path('exporter-excel/', views.exporter_stock_excel, name='exporter_excel'),
    path('imprimer/', views.imprimer_stock, name='imprimer_stock'),
    
    # Navbar functionality
    path('boot-kit/', views.BootKitView.as_view(), name='boot_kit'),
    path('cross-dock/', views.CrossDockView.as_view(), name='cross_dock'),
    path('map-debord/', views.MapDebordView.as_view(), name='map_debord'),
    path('flc/', views.FLCView.as_view(), name='flc'),
    path('log-ext/', views.LogExtView.as_view(), name='log_ext'),
    path('how-to-use/', views.HowToUseView.as_view(), name='how_to_use'),
]
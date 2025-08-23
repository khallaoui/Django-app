from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.alertes.models import Alerte
from django.db.models import Count

@login_required
def dashboard_view(request):
    # Statistiques des alertes
    total_alertes = Alerte.objects.count()
    alertes_en_cours = Alerte.objects.filter(statut='en_cours').count()
    alertes_livrees = Alerte.objects.filter(statut='livre').count()
    alertes_flc = Alerte.objects.filter(statut='flc').count()
    alertes_cloturees = Alerte.objects.filter(statut='cloture').count()
    
    # Alertes récentes
    alertes_recentes = Alerte.objects.all()[:10]
    
    # Statistiques par zone
    stats_zones = Alerte.objects.values('zone_kit').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    context = {
        'total_alertes': total_alertes,
        'alertes_en_cours': alertes_en_cours,
        'alertes_livrees': alertes_livrees,
        'alertes_flc': alertes_flc,
        'alertes_cloturees': alertes_cloturees,
        'alertes_recentes': alertes_recentes,
        'stats_zones': stats_zones,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
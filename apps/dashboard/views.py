from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stock_debord.models import Reference, Historique, Travee
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def dashboard_view(request):
    # Statistiques du stock
    total_references = Reference.objects.count()
    total_bacs = Reference.objects.aggregate(total=Sum('nombre_bacs'))['total'] or 0
    
    # Travées occupées
    travees_occupees = Reference.objects.exclude(travee_debord='').values('travee_debord').distinct().count()
    
    # Mouvements d'aujourd'hui
    aujourdhui = timezone.now().date()
    mouvements_aujourdhui = Historique.objects.filter(date_action__date=aujourdhui).count()
    
    # Références récentes
    references = Reference.objects.all()[:10]
    
    context = {
        'total_references': total_references,
        'total_bacs': total_bacs,
        'travees_occupees': travees_occupees,
        'mouvements_aujourdhui': mouvements_aujourdhui,
        'references': references,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def next_previous_demo_view(request):
    """Demo page for next and previous buttons tutorial"""
    return render(request, 'next_previous_demo.html')
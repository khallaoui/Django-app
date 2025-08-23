from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Alerte, HistoriqueAlerte
from .forms import AlerteForm
import json

@login_required
def create_alerte(request):
    if request.method == 'POST':
        form = AlerteForm(request.POST)
        if form.is_valid():
            alerte = form.save(commit=False)
            alerte.createur = request.user
            alerte.save()
            
            # Créer historique
            HistoriqueAlerte.objects.create(
                alerte=alerte,
                action="Création de l'alerte",
                utilisateur=request.user,
                nouveau_statut=alerte.statut
            )
            
            messages.success(request, 'Alerte créée avec succès!')
            return redirect('list_alertes')
    else:
        form = AlerteForm()
    
    return render(request, 'alertes/create_alert.html', {'form': form})

@login_required
def list_alertes(request):
    alertes = Alerte.objects.all()
    
    # Filtrage par statut si demandé
    statut = request.GET.get('statut')
    if statut:
        alertes = alertes.filter(statut=statut)
    
    return render(request, 'alertes/list_alerts.html', {'alertes': alertes})

@login_required
def update_statut(request, alerte_id):
    if request.method == 'POST':
        alerte = get_object_or_404(Alerte, id=alerte_id)
        ancien_statut = alerte.statut
        nouveau_statut = request.POST.get('statut')
        
        alerte.statut = nouveau_statut
        alerte.traite_par = request.user
        alerte.save()
        
        # Historique
        HistoriqueAlerte.objects.create(
            alerte=alerte,
            action=f"Changement de statut",
            utilisateur=request.user,
            ancien_statut=ancien_statut,
            nouveau_statut=nouveau_statut
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})
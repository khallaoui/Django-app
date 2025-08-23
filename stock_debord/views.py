from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reference, Historique, Travee
from .forms import ReferenceForm, SortieForm, ViderTraveeForm
import json
from django.db.models import Sum
from django.utils import timezone


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bacs'] = Reference.objects.aggregate(total=Sum('nombre_bacs'))['total'] or 0
        context['references'] = Reference.objects.all()[:10]
        context['total_references'] = Reference.objects.count()
        return context


class AjouterReferenceView(LoginRequiredMixin, CreateView):
    model = Reference
    form_class = ReferenceForm
    template_name = 'stock_debord/ajouter_reference.html'
    success_url = reverse_lazy('stock_debord:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Créer une entrée dans l'historique
        Historique.objects.create(
            reference=self.object,
            type_action='entree',
            nombre_bacs=self.object.nombre_bacs,
            utilisateur=self.request.user.username
        )
        messages.success(self.request, 'Référence ajoutée avec succès!')
        return response


class ViderTraveeView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/vider_travee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ViderTraveeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ViderTraveeForm(request.POST)
        if form.is_valid():
            travee = form.cleaned_data['travee']
            references = Reference.objects.filter(travee_debord=travee.nom)
            
            # Logique pour vider la travée
            for ref in references:
                Historique.objects.create(
                    reference=ref,
                    type_action='sortie',
                    nombre_bacs=ref.nombre_bacs,
                    utilisateur=request.user.username
                )
            
            references.update(travee_debord='')
            messages.success(request, f'Travée {travee.nom} vidée avec succès!')
            return redirect('stock_debord:dashboard')
        
        return render(request, self.template_name, {'form': form})


class SaisieSortieView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/saisie_sortie.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SortieForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SortieForm(request.POST)
        if form.is_valid():
            reference = form.cleaned_data['reference']
            nombre_bacs = form.cleaned_data['nombre_bacs']
            
            # Mettre à jour le stock
            if reference.nombre_bacs >= nombre_bacs:
                reference.nombre_bacs -= nombre_bacs
                reference.save()
                
                # Ajouter à l'historique
                Historique.objects.create(
                    reference=reference,
                    type_action='sortie',
                    nombre_bacs=nombre_bacs,
                    utilisateur=request.user.username
                )
                
                messages.success(request, f'Sortie de {nombre_bacs} bacs enregistrée!')
                return redirect('stock_debord:dashboard')
            else:
                messages.error(request, 'Stock insuffisant!')
        
        return render(request, self.template_name, {'form': form})


class HistoriqueView(LoginRequiredMixin, ListView):
    model = Historique
    template_name = 'stock_debord/historique.html'
    context_object_name = 'historique'
    paginate_by = 20


@login_required
def exporter_stock_excel(request):
    # Implémentation de l'export Excel
    try:
        import pandas as pd
        from django.http import HttpResponse
        
        references = Reference.objects.all()
        data = []
        
        for ref in references:
            data.append({
                'Emplacement SM': ref.emplacement_sm,
                'Référence': ref.reference,
                'Nombre de Bac': ref.nombre_bacs,
                'Date entrée': ref.date_entree,
                'Travée débord': ref.travee_debord,
                'Code condi': ref.code_condi,
                'Qt pièce/UC': ref.qt_piece_uc,
                'Appro': ref.appro,
                'Fournisseur': ref.fournisseur,
                'CMJ': ref.cmj,
                'F': ref.f
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="stock_debord.xlsx"'
        df.to_excel(response, index=False)
        return response
    except ImportError:
        messages.error(request, 'Pandas non installé. Impossible d\'exporter en Excel.')
        return redirect('stock_debord:dashboard')


@login_required
def imprimer_stock(request):
    references = Reference.objects.all()
    return render(request, 'stock_debord/imprimer_stock.html', {'references': references})


# Navbar functionality views
class BootKitView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/boot_kit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add Boot KIT specific data here
        context['kits'] = []  # Placeholder for boot kits data
        return context


class CrossDockView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/cross_dock.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add Cross DOCK specific data here
        context['cross_dock_operations'] = []  # Placeholder for cross dock operations
        return context


class MapDebordView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/map_debord.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add map data here
        context['travees'] = Travee.objects.all()
        context['references_by_travee'] = {}
        
        for travee in context['travees']:
            context['references_by_travee'][travee.nom] = Reference.objects.filter(
                travee_debord=travee.nom
            )
        
        return context


class FLCView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/flc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add FLC (Flux Logistique) specific data here
        context['flux_data'] = []  # Placeholder for logistics flow data
        return context


class LogExtView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/log_ext.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add external logs data here
        context['external_logs'] = []  # Placeholder for external logs
        return context


class HowToUseView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/how_to_use.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add documentation data here
        context['documentation_sections'] = [
            {
                'title': 'Gestion du Stock',
                'content': 'Guide pour gérer les références et les quantités en stock.'
            },
            {
                'title': 'Entrées et Sorties',
                'content': 'Comment enregistrer les mouvements de stock.'
            },
            {
                'title': 'Rapports et Exports',
                'content': 'Génération de rapports et exports Excel.'
            }
        ]
        return context
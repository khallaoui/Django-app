from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Reference, Historique, Travee
from .forms import ReferenceForm, SortieForm
import json
from django.db.models import Sum, Q
from django.utils import timezone
from apps.authentication.decorators import consultant_required, gestionnaire_required, admin_required
from apps.authentication.permissions import UserPermissions


class GestionnaireRequiredMixin(UserPassesTestMixin):
    """Mixin pour restreindre l'accès aux gestionnaires et administrateurs"""
    def test_func(self):
        return UserPermissions.can_manage_warehouse(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'Vous n\'avez pas les permissions nécessaires pour accéder à cette page.')
        return redirect('stock_debord:dashboard')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'stock_debord/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bacs'] = Reference.objects.aggregate(total=Sum('nombre_bacs'))['total'] or 0
        context['total_references'] = Reference.objects.count()
        
        # Search and filter functionality
        references_queryset = Reference.objects.all()
        
        # Search by reference
        search_reference = self.request.GET.get('search_reference')
        if search_reference and search_reference != 'None' and search_reference.strip():
            references_queryset = references_queryset.filter(
                Q(reference__icontains=search_reference) |
                Q(emplacement_sm__icontains=search_reference) |
                Q(fournisseur__icontains=search_reference)
            )
        
        # Filter by date range
        date_debut = self.request.GET.get('date_debut')
        date_fin = self.request.GET.get('date_fin')
        
        if date_debut:
            from datetime import datetime
            try:
                # Try multiple date formats (prioritize DD/MM/YYYY for European format)
                date_debut_obj = None
                date_formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']
                
                for date_format in date_formats:
                    try:
                        date_debut_obj = datetime.strptime(date_debut, date_format).date()
                        break
                    except ValueError:
                        continue
                
                if date_debut_obj:
                    # Debug: Check what we're comparing
                    print(f"DEBUG: Filtering from date: {date_debut_obj}")
                    
                    # Get all dates to debug
                    all_refs = Reference.objects.all()
                    all_dates = [ref.date_entree.date() for ref in all_refs]
                    matching_dates = [d for d in all_dates if d >= date_debut_obj]
                    
                    print(f"DEBUG: All dates in DB: {sorted(all_dates)}")
                    print(f"DEBUG: Filter date: {date_debut_obj}")
                    print(f"DEBUG: Matching dates: {sorted(matching_dates)}")
                    print(f"DEBUG: Count of matching dates: {len(matching_dates)}")
                    
                    # Try different filtering approaches
                    # Method 1: Using __date__gte
                    filtered1 = references_queryset.filter(date_entree__date__gte=date_debut_obj)
                    print(f"DEBUG: Method 1 count: {filtered1.count()}")
                    
                    # Method 2: Using __gte with datetime
                    from datetime import time
                    start_datetime = datetime.combine(date_debut_obj, time.min)
                    filtered2 = references_queryset.filter(date_entree__gte=start_datetime)
                    print(f"DEBUG: Method 2 count: {filtered2.count()}")
                    
                    # Method 3: Using __gte with timezone-aware datetime
                    from django.utils import timezone
                    start_datetime_tz = timezone.make_aware(start_datetime)
                    filtered3 = references_queryset.filter(date_entree__gte=start_datetime_tz)
                    print(f"DEBUG: Method 3 count: {filtered3.count()}")
                    
                    # Use the method that works
                    if filtered1.count() > 0:
                        references_queryset = filtered1
                        print(f"DEBUG: Using Method 1")
                    elif filtered2.count() > 0:
                        references_queryset = filtered2
                        print(f"DEBUG: Using Method 2")
                    elif filtered3.count() > 0:
                        references_queryset = filtered3
                        print(f"DEBUG: Using Method 3")
                    else:
                        print(f"DEBUG: No method worked")
                
            except Exception as e:
                pass  # Skip invalid dates
        
        if date_fin:
            from datetime import datetime
            try:
                # Try multiple date formats (prioritize DD/MM/YYYY for European format)
                date_fin_obj = None
                date_formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']
                
                for date_format in date_formats:
                    try:
                        date_fin_obj = datetime.strptime(date_fin, date_format).date()
                        break
                    except ValueError:
                        continue
                
                if date_fin_obj:
                    # Use simple and reliable date filtering
                    references_queryset = references_queryset.filter(date_entree__date__lte=date_fin_obj)
                
            except Exception as e:
                pass  # Skip invalid dates
        
        # Order and pagination
        references_queryset = references_queryset.order_by('-date_entree')
        paginator = Paginator(references_queryset, 10)  # 10 items per page to show pagination
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['references'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['search_reference'] = search_reference
        context['date_debut'] = date_debut
        context['date_fin'] = date_fin
        
        # Debug: Add some sample dates to context for debugging
        if date_debut or date_fin:
            # Get a more representative sample of dates (mix of recent and older)
            all_dates = list(Reference.objects.values_list('date_entree', flat=True).order_by('-date_entree'))
            sample_dates = all_dates[:3] + all_dates[-2:] if len(all_dates) > 5 else all_dates
            context['debug_dates'] = sample_dates
            context['debug_queryset_count'] = references_queryset.count()
            context['debug_date_debut'] = date_debut
            context['debug_date_fin'] = date_fin
            context['debug_total_references'] = Reference.objects.count()
            
            # Add more detailed debug info
            if date_debut:
                try:
                    date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d').date()
                    context['debug_date_debut_obj'] = date_debut_obj
                    context['debug_references_before_filter'] = Reference.objects.count()
                    context['debug_references_after_filter'] = references_queryset.count()
                    
                    # Show date range of all data
                    if all_dates:
                        context['debug_earliest_date'] = min(all_dates)
                        context['debug_latest_date'] = max(all_dates)
                except ValueError:
                    pass
        
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


class HistoriqueView(GestionnaireRequiredMixin, LoginRequiredMixin, ListView):
    model = Historique
    template_name = 'stock_debord/historique.html'
    context_object_name = 'historique'
    paginate_by = 50  # 50 items per page

    def get_queryset(self):
        queryset = Historique.objects.select_related('reference').all()
        
        # Filtre par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(reference__reference__icontains=search) |
                Q(utilisateur__icontains=search) |
                Q(reference__emplacement_sm__icontains=search)
            )
        
        # Filtre par type d'action
        type_action = self.request.GET.get('type_action')
        if type_action:
            queryset = queryset.filter(type_action=type_action)
        
        # Filtre par date de début
        date_debut = self.request.GET.get('date_debut')
        if date_debut:
            from datetime import datetime
            try:
                # Try multiple date formats (prioritize DD/MM/YYYY for European format)
                date_debut_obj = None
                date_formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']
                
                for date_format in date_formats:
                    try:
                        date_debut_obj = datetime.strptime(date_debut, date_format).date()
                        break
                    except ValueError:
                        continue
                
                if date_debut_obj:
                    # Debug: Check what we're comparing
                    print(f"DEBUG HISTORIQUE: Filtering from date: {date_debut_obj}")
                    
                    # Get all dates to debug
                    all_entries = Historique.objects.all()
                    all_dates = [entry.date_action.date() for entry in all_entries]
                    matching_dates = [d for d in all_dates if d >= date_debut_obj]
                    
                    print(f"DEBUG HISTORIQUE: All dates in DB: {sorted(all_dates)}")
                    print(f"DEBUG HISTORIQUE: Filter date: {date_debut_obj}")
                    print(f"DEBUG HISTORIQUE: Matching dates: {sorted(matching_dates)}")
                    print(f"DEBUG HISTORIQUE: Count of matching dates: {len(matching_dates)}")
                    
                    # Try different filtering approaches
                    # Method 1: Using __date__gte
                    filtered1 = queryset.filter(date_action__date__gte=date_debut_obj)
                    print(f"DEBUG HISTORIQUE: Method 1 count: {filtered1.count()}")
                    
                    # Method 2: Using __gte with datetime
                    from datetime import time
                    start_datetime = datetime.combine(date_debut_obj, time.min)
                    filtered2 = queryset.filter(date_action__gte=start_datetime)
                    print(f"DEBUG HISTORIQUE: Method 2 count: {filtered2.count()}")
                    
                    # Method 3: Using __gte with timezone-aware datetime
                    from django.utils import timezone
                    start_datetime_tz = timezone.make_aware(start_datetime)
                    filtered3 = queryset.filter(date_action__gte=start_datetime_tz)
                    print(f"DEBUG HISTORIQUE: Method 3 count: {filtered3.count()}")
                    
                    # Use the method that works
                    if filtered1.count() > 0:
                        queryset = filtered1
                        print(f"DEBUG HISTORIQUE: Using Method 1")
                    elif filtered2.count() > 0:
                        queryset = filtered2
                        print(f"DEBUG HISTORIQUE: Using Method 2")
                    elif filtered3.count() > 0:
                        queryset = filtered3
                        print(f"DEBUG HISTORIQUE: Using Method 3")
                    else:
                        print(f"DEBUG HISTORIQUE: No method worked")
            except Exception as e:
                pass  # Skip invalid dates
        
        # Filtre par date de fin
        date_fin = self.request.GET.get('date_fin')
        if date_fin:
            from datetime import datetime
            try:
                # Try multiple date formats (prioritize DD/MM/YYYY for European format)
                date_fin_obj = None
                date_formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']
                
                for date_format in date_formats:
                    try:
                        date_fin_obj = datetime.strptime(date_fin, date_format).date()
                        break
                    except ValueError:
                        continue
                
                if date_fin_obj:
                    queryset = queryset.filter(date_action__date__lte=date_fin_obj)
            except Exception as e:
                pass  # Skip invalid dates
        
        return queryset.order_by('-date_action')


@login_required
@gestionnaire_required
def exporter_stock_excel(request):
    # Implémentation de l'export Excel
    try:
        import pandas as pd
        from django.http import HttpResponse
        from django.utils import timezone
        
        references = Reference.objects.all()
        data = []
        
        for ref in references:
            # Convert timezone-aware datetime to naive datetime for Excel compatibility
            date_entree_naive = ref.date_entree
            if timezone.is_aware(date_entree_naive):
                date_entree_naive = timezone.make_naive(date_entree_naive)
            
            data.append({
                'Emplacement SM': ref.emplacement_sm,
                'Référence': ref.reference,
                'Nombre de Bac': ref.nombre_bacs,
                'Date entrée': date_entree_naive,
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
@gestionnaire_required
def export_historique_excel(request):
    # Export Excel de l'historique avec filtres
    try:
        import pandas as pd
        from django.http import HttpResponse
        
        # Appliquer les mêmes filtres que la vue historique
        queryset = Historique.objects.select_related('reference').all()
        
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(reference__reference__icontains=search) |
                Q(utilisateur__icontains=search) |
                Q(reference__emplacement_sm__icontains=search)
            )
        
        type_action = request.GET.get('type_action')
        if type_action:
            queryset = queryset.filter(type_action=type_action)
        
        date_debut = request.GET.get('date_debut')
        if date_debut:
            from datetime import datetime
            try:
                # Try multiple date formats (prioritize DD/MM/YYYY for European format)
                date_debut_obj = None
                date_formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']
                
                for date_format in date_formats:
                    try:
                        date_debut_obj = datetime.strptime(date_debut, date_format).date()
                        break
                    except ValueError:
                        continue
                
                if date_debut_obj:
                    queryset = queryset.filter(date_action__date__gte=date_debut_obj)
            except Exception as e:
                pass  # Skip invalid dates
        
        date_fin = request.GET.get('date_fin')
        if date_fin:
            from datetime import datetime
            try:
                # Try multiple date formats (prioritize DD/MM/YYYY for European format)
                date_fin_obj = None
                date_formats = ['%d/%m/%Y', '%d-%m/%Y', '%Y-%m-%d', '%m/%d/%Y']
                
                for date_format in date_formats:
                    try:
                        date_fin_obj = datetime.strptime(date_fin, date_format).date()
                        break
                    except ValueError:
                        continue
                
                if date_fin_obj:
                    queryset = queryset.filter(date_action__date__lte=date_fin_obj)
            except Exception as e:
                pass  # Skip invalid dates
        
        data = []
        for entry in queryset.order_by('-date_action'):
            # Convert timezone-aware datetime to naive datetime for Excel compatibility
            date_action_naive = entry.date_action
            if timezone.is_aware(date_action_naive):
                date_action_naive = timezone.make_naive(date_action_naive)
            
            data.append({
                'Date/Heure': date_action_naive.strftime('%d/%m/%Y %H:%M:%S'),
                'Type': 'Entrée' if entry.type_action == 'entree' else 'Sortie',
                'Référence': entry.reference.reference,
                'Emplacement SM': entry.reference.emplacement_sm,
                'Nombre de Bacs': entry.nombre_bacs,
                'Utilisateur': entry.utilisateur,
                'Travée Débord': entry.reference.travee_debord,
                'Fournisseur': entry.reference.fournisseur
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="historique_mouvements.xlsx"'
        df.to_excel(response, index=False)
        return response
    except ImportError:
        messages.error(request, 'Pandas non installé. Impossible d\'exporter en Excel.')
        return redirect('stock_debord:historique')


@login_required
def imprimer_stock(request):
    references = Reference.objects.all()
    return render(request, 'stock_debord/imprimer_stock.html', {'references': references})


@login_required
@gestionnaire_required
def extraction_mouvements(request):
    # Vue pour l'extraction des mouvements de stock
    mouvements = None
    mouvements_stats = None
    
    if request.method == 'GET' and request.GET.get('date_debut') and request.GET.get('date_fin'):
        # Appliquer les filtres
        queryset = Historique.objects.select_related('reference').all()
        
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        type_action = request.GET.get('type_action')
        format_export = request.GET.get('format', 'excel')
        
        # Filtres
        queryset = queryset.filter(date_action__date__gte=date_debut, date_action__date__lte=date_fin)
        
        if type_action:
            queryset = queryset.filter(type_action=type_action)
        
        # Statistiques
        mouvements_stats = {
            'total_mouvements': queryset.count(),
            'total_entrees': queryset.filter(type_action='entree').count(),
            'total_sorties': queryset.filter(type_action='sortie').count(),
            'total_bacs': queryset.aggregate(total=Sum('nombre_bacs'))['total'] or 0
        }
        
        # Si c'est un export, générer le fichier
        if request.GET.get('export'):
            if format_export == 'excel':
                return export_mouvements_excel(queryset, date_debut, date_fin)
            else:
                return export_mouvements_csv(queryset, date_debut, date_fin)
        else:
            # Sinon, afficher l'aperçu avec pagination
            paginator = Paginator(queryset.order_by('-date_action'), 50)  # 50 items per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            mouvements = page_obj
    
    context = {
        'mouvements': mouvements,
        'mouvements_stats': mouvements_stats
    }
    
    # Add pagination context if mouvements is a page object
    if hasattr(mouvements, 'has_other_pages'):
        context['page_obj'] = mouvements
        context['is_paginated'] = mouvements.has_other_pages()
    
    return render(request, 'stock_debord/extraction_mouvements.html', context)


def export_mouvements_excel(queryset, date_debut, date_fin):
    try:
        import pandas as pd
        from django.http import HttpResponse
        
        data = []
        for entry in queryset.order_by('-date_action'):
            # Convert timezone-aware datetime to naive datetime for Excel compatibility
            date_action_naive = entry.date_action
            if timezone.is_aware(date_action_naive):
                date_action_naive = timezone.make_naive(date_action_naive)
            
            data.append({
                'Date/Heure': date_action_naive.strftime('%d/%m/%Y %H:%M:%S'),
                'Type': 'Entrée' if entry.type_action == 'entree' else 'Sortie',
                'Référence': entry.reference.reference,
                'Emplacement SM': entry.reference.emplacement_sm,
                'Nombre de Bacs': entry.nombre_bacs,
                'Utilisateur': entry.utilisateur,
                'Travée Débord': entry.reference.travee_debord,
                'Fournisseur': entry.reference.fournisseur,
                'Code Condi': entry.reference.code_condi,
                'Qt pièce/UC': entry.reference.qt_piece_uc,
                'Appro': entry.reference.appro,
                'CMJ': entry.reference.cmj,
                'F': entry.reference.f
            })
        
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        filename = f"mouvements_stock_{date_debut}_to_{date_fin}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        df.to_excel(response, index=False)
        return response
    except ImportError:
        from django.http import HttpResponse
        return HttpResponse('Pandas non installé. Impossible d\'exporter en Excel.', status=500)


def export_mouvements_csv(queryset, date_debut, date_fin):
    import csv
    from django.http import HttpResponse
    from django.utils import timezone
    
    response = HttpResponse(content_type='text/csv')
    filename = f"mouvements_stock_{date_debut}_to_{date_fin}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Date/Heure', 'Type', 'Référence', 'Emplacement SM', 'Nombre de Bacs',
        'Utilisateur', 'Travée Débord', 'Fournisseur', 'Code Condi',
        'Qt pièce/UC', 'Appro', 'CMJ', 'F'
    ])
    
    for entry in queryset.order_by('-date_action'):
        # Convert timezone-aware datetime to naive datetime for CSV compatibility
        date_action_naive = entry.date_action
        if timezone.is_aware(date_action_naive):
            date_action_naive = timezone.make_naive(date_action_naive)
        
        writer.writerow([
            date_action_naive.strftime('%d/%m/%Y %H:%M:%S'),
            'Entrée' if entry.type_action == 'entree' else 'Sortie',
            entry.reference.reference,
            entry.reference.emplacement_sm,
            entry.nombre_bacs,
            entry.utilisateur,
            entry.reference.travee_debord,
            entry.reference.fournisseur,
            entry.reference.code_condi,
            entry.reference.qt_piece_uc,
            entry.reference.appro,
            entry.reference.cmj,
            entry.reference.f
        ])
    
    return response


class GestionReferencesView(GestionnaireRequiredMixin, LoginRequiredMixin, ListView):
    model = Reference
    template_name = 'stock_debord/gestion_references.html'
    context_object_name = 'references'
    paginate_by = 50  # 50 items per page

    def get_queryset(self):
        queryset = Reference.objects.all()
        
        # Filtre par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(reference__icontains=search) |
                Q(emplacement_sm__icontains=search) |
                Q(fournisseur__icontains=search)
            )
        
        # Filtre par travée
        travee = self.request.GET.get('travee')
        if travee:
            queryset = queryset.filter(travee_debord=travee)
        
        # Filtre par fournisseur
        fournisseur = self.request.GET.get('fournisseur')
        if fournisseur:
            queryset = queryset.filter(fournisseur=fournisseur)
        
        # Filtre par statut
        statut = self.request.GET.get('statut')
        if statut == 'en_stock':
            queryset = queryset.filter(nombre_bacs__gt=10)
        elif statut == 'stock_faible':
            queryset = queryset.filter(nombre_bacs__gt=0, nombre_bacs__lte=10)
        elif statut == 'rupture':
            queryset = queryset.filter(nombre_bacs=0)
        
        return queryset.order_by('-date_entree')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travees'] = Travee.objects.all()
        context['fournisseurs'] = Reference.objects.values_list('fournisseur', flat=True).distinct().exclude(fournisseur='')
        return context


@login_required
@gestionnaire_required
def supprimer_reference(request, reference_id):
    if request.method == 'POST':
        try:
            reference = get_object_or_404(Reference, id=reference_id)
            reference.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


class ModifierReferenceView(GestionnaireRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Reference
    form_class = ReferenceForm
    template_name = 'stock_debord/modifier_reference.html'
    success_url = reverse_lazy('stock_debord:gestion_references')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Référence modifiée avec succès!')
        return response


class GestionZonesView(GestionnaireRequiredMixin, LoginRequiredMixin, ListView):
    model = Travee
    template_name = 'stock_debord/gestion_zones.html'
    context_object_name = 'zones'
    paginate_by = 50  # 50 items per page

    def get_queryset(self):
        queryset = Travee.objects.all()
        
        # Filtre par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nom__icontains=search)
        
        # Filtre par statut
        statut = self.request.GET.get('statut')
        if statut == 'disponible':
            queryset = queryset.filter(references__isnull=True)
        elif statut == 'occupee':
            queryset = queryset.filter(references__isnull=False).distinct()
        elif statut == 'maintenance':
            # Ici on pourrait ajouter un champ de statut de maintenance
            pass
        
        return queryset.order_by('nom')


@login_required
@gestionnaire_required
def ajouter_zone(request):
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom')
            capacite = request.POST.get('capacite')
            
            if not nom or not capacite:
                return JsonResponse({'success': False, 'error': 'Nom et capacité requis'})
            
            Travee.objects.create(nom=nom, capacite=int(capacite))
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


@login_required
@gestionnaire_required
def modifier_zone(request):
    if request.method == 'POST':
        try:
            zone_id = request.POST.get('zone_id')
            nom = request.POST.get('nom')
            capacite = request.POST.get('capacite')
            
            if not zone_id or not nom or not capacite:
                return JsonResponse({'success': False, 'error': 'Tous les champs sont requis'})
            
            zone = get_object_or_404(Travee, id=zone_id)
            zone.nom = nom
            zone.capacite = int(capacite)
            zone.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


@login_required
@gestionnaire_required
def supprimer_zone(request, zone_id):
    if request.method == 'POST':
        try:
            zone = get_object_or_404(Travee, id=zone_id)
            zone.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


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


@login_required
def pagination_demo(request):
    """Demo page showing different pagination button styles"""
    return render(request, 'stock_debord/pagination_demo.html')
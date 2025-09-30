# ============================================================================
# EXEMPLES D'INTÉGRATION DES RÔLES DANS VOTRE APPLICATION
# ============================================================================

# ----------------------------------------------------------------------------
# 1. PROTÉGER UNE VUE BASÉE SUR FONCTION
# ----------------------------------------------------------------------------

from apps.authentication.decorators import consultant_required, gestionnaire_required, admin_required

# Vue accessible à tous les utilisateurs authentifiés (Consultant, Gestionnaire, Admin)
@consultant_required
def view_stock(request):
    """Tout le monde peut consulter le stock"""
    references = Reference.objects.all()
    return render(request, 'stock_debord/dashboard.html', {'references': references})

# Vue accessible uniquement aux Gestionnaires et Admins
@gestionnaire_required
def valider_mouvement(request, mouvement_id):
    """Seuls les gestionnaires peuvent valider les mouvements"""
    mouvement = get_object_or_404(Historique, id=mouvement_id)
    mouvement.valide = True
    mouvement.save()
    messages.success(request, 'Mouvement validé avec succès!')
    return redirect('stock_debord:historique')

# Vue accessible uniquement aux Administrateurs
@admin_required
def gestion_parametres(request):
    """Configuration système - Admin uniquement"""
    return render(request, 'parametres.html')


# ----------------------------------------------------------------------------
# 2. PROTÉGER UNE VUE BASÉE SUR CLASSE (CBV)
# ----------------------------------------------------------------------------

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Mixin personnalisé pour vérifier les rôles
class ConsultantRequiredMixin(UserPassesTestMixin):
    """Accessible aux Consultants, Gestionnaires et Admins"""
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.role in ['consultant', 'gestionnaire', 'admin']

class GestionnaireRequiredMixin(UserPassesTestMixin):
    """Accessible aux Gestionnaires et Admins uniquement"""
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.role in ['gestionnaire', 'admin']

class AdminRequiredMixin(UserPassesTestMixin):
    """Accessible aux Admins uniquement"""
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.role == 'admin'

# EXEMPLE: Modifier votre DashboardView existant
class DashboardView(ConsultantRequiredMixin, TemplateView):
    """Tous les utilisateurs peuvent voir le dashboard"""
    template_name = 'stock_debord/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ... votre code existant ...
        
        # Ajouter des informations de rôle dans le contexte
        context['user_role'] = self.request.user.get_role_display()
        context['can_validate'] = self.request.user.role in ['gestionnaire', 'admin']
        context['can_manage_users'] = self.request.user.role == 'admin'
        
        return context


# ----------------------------------------------------------------------------
# 3. VÉRIFICATIONS CONDITIONNELLES DANS LES VUES
# ----------------------------------------------------------------------------

from apps.authentication.permissions import UserPermissions

@login_required
def historique_view(request):
    """Vue avec permissions conditionnelles"""
    
    # Vérifier si l'utilisateur peut voir l'historique complet
    if UserPermissions.can_view_full_history(request.user):
        # Gestionnaire ou Admin: voir tout l'historique
        historique = Historique.objects.all()
    else:
        # Consultant: voir uniquement ses propres mouvements
        historique = Historique.objects.filter(operateur=request.user)
    
    return render(request, 'stock_debord/historique.html', {
        'historique': historique,
        'can_validate': UserPermissions.can_validate_movements(request.user)
    })


# ----------------------------------------------------------------------------
# 4. CONTRÔLE D'ACCÈS DANS LES FORMULAIRES
# ----------------------------------------------------------------------------

@login_required
def ajouter_reference(request):
    """Tous peuvent ajouter, mais avec des champs différents selon le rôle"""
    
    if request.method == 'POST':
        form = ReferenceForm(request.POST)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.cree_par = request.user  # Traçabilité
            
            # Si c'est un consultant, le mouvement doit être validé par un gestionnaire
            if request.user.role == 'consultant':
                reference.statut = 'en_attente_validation'
            else:
                reference.statut = 'valide'
            
            reference.save()
            messages.success(request, 'Référence ajoutée avec succès!')
            return redirect('stock_debord:dashboard')
    else:
        form = ReferenceForm()
    
    return render(request, 'stock_debord/ajouter_reference.html', {
        'form': form,
        'needs_validation': request.user.role == 'consultant'
    })


# ----------------------------------------------------------------------------
# 5. API/AJAX avec vérification de rôle
# ----------------------------------------------------------------------------

from django.http import JsonResponse

@login_required
def api_valider_mouvement(request, mouvement_id):
    """API pour valider un mouvement - JSON"""
    
    # Vérifier les permissions
    if not UserPermissions.can_validate_movements(request.user):
        return JsonResponse({
            'success': False,
            'error': 'Vous n\'avez pas les permissions pour valider les mouvements.'
        }, status=403)
    
    try:
        mouvement = Historique.objects.get(id=mouvement_id)
        mouvement.valide = True
        mouvement.valide_par = request.user
        mouvement.date_validation = timezone.now()
        mouvement.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Mouvement validé avec succès!'
        })
    except Historique.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Mouvement non trouvé.'
        }, status=404)


# ============================================================================
# EXEMPLES DANS LES TEMPLATES
# ============================================================================

"""
<!-- Dans stock_debord/dashboard.html -->

<!-- Afficher le rôle de l'utilisateur -->
<div class="user-badge">
    Connecté en tant que: 
    <span class="badge 
        {% if user.role == 'admin' %}bg-danger
        {% elif user.role == 'gestionnaire' %}bg-warning
        {% else %}bg-info{% endif %}">
        {{ user.get_role_display }}
    </span>
</div>

<!-- Boutons conditionnels selon le rôle -->
{% if user.is_gestionnaire %}
    <button class="btn btn-primary" onclick="validerMouvement()">
        <i class="fas fa-check"></i> Valider le mouvement
    </button>
{% endif %}

{% if user.is_admin %}
    <a href="{% url 'auth:user_list' %}" class="btn btn-danger">
        <i class="fas fa-users"></i> Gérer les utilisateurs
    </a>
{% endif %}

<!-- Menu conditionnel -->
<ul class="nav">
    <li><a href="{% url 'stock_debord:dashboard' %}">Dashboard</a></li>
    
    {% if user.is_consultant %}
        <li><a href="{% url 'stock_debord:saisie_sortie' %}">Saisie Sortie</a></li>
    {% endif %}
    
    {% if user.is_gestionnaire %}
        <li><a href="{% url 'stock_debord:validation' %}">Validation</a></li>
        <li><a href="{% url 'stock_debord:gestion_zones' %}">Gestion Zones</a></li>
    {% endif %}
    
    {% if user.is_admin %}
        <li><a href="{% url 'auth:user_list' %}">Utilisateurs</a></li>
        <li><a href="/admin/">Admin Django</a></li>
    {% endif %}
</ul>

<!-- Affichage conditionnel des colonnes dans un tableau -->
<table class="table">
    <thead>
        <tr>
            <th>Référence</th>
            <th>Stock</th>
            {% if user.is_gestionnaire %}
                <th>Validation</th>
            {% endif %}
            {% if user.is_admin %}
                <th>Actions Admin</th>
            {% endif %}
        </tr>
    </thead>
</table>
"""


# ============================================================================
# SCÉNARIOS D'UTILISATION PRATIQUES
# ============================================================================

"""
SCÉNARIO 1: Menu Navigation Conditionnel
=========================================

Consultant voit:
  - Dashboard
  - Gestion Stock
  - Saisie Sortie/Entrée
  
Gestionnaire voit en plus:
  - Validation des mouvements
  - Gestion des zones
  - Historique complet
  
Admin voit en plus:
  - Gestion des utilisateurs
  - Admin Django
  - Paramètres système


SCÉNARIO 2: Workflow de Validation
===================================

1. Consultant crée un mouvement → Statut: "En attente"
2. Gestionnaire reçoit notification → Peut valider/rejeter
3. Admin peut tout voir et modifier


SCÉNARIO 3: Restriction des Actions
====================================

Dans le tableau de stock:
  - Consultant: Voir + Ajouter sortie
  - Gestionnaire: Voir + Ajouter sortie + Modifier + Valider
  - Admin: Toutes les actions + Supprimer
"""

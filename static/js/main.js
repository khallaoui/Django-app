// JavaScript principal pour l'application de gestion des alertes

$(document).ready(function() {
    
    // Configuration CSRF pour les requêtes AJAX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    // Configuration AJAX par défaut
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Mise à jour du statut d'alerte via AJAX
    $('.btn-update-status').on('click', function() {
        const alerteId = $(this).data('alerte-id');
        const newStatus = $(this).data('status');
        const button = $(this);
        const originalText = button.html();
        
        // Messages de confirmation
        let confirmMessage = '';
        switch(newStatus) {
            case 'livre':
                confirmMessage = 'Confirmer que cette alerte est livrée ?';
                break;
            case 'flc':
                confirmMessage = 'Confirmer l\'envoi du FLC pour cette alerte ?';
                break;
            case 'cloture':
                confirmMessage = 'Êtes-vous sûr de vouloir clôturer cette alerte ?';
                break;
        }
        
        if (confirmMessage && !confirm(confirmMessage)) {
            return;
        }
        
        // Désactiver le bouton et afficher un spinner
        button.prop('disabled', true);
        button.html('<span class="spinner-border spinner-border-sm" role="status"></span> Traitement...');
        
        $.ajax({
            url: `/alertes/update-statut/${alerteId}/`,
            type: 'POST',
            data: {
                'statut': newStatus,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    // Afficher un message de succès
                    showNotification('Statut mis à jour avec succès!', 'success');
                    
                    // Recharger la page après un court délai
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                } else {
                    showNotification('Erreur lors de la mise à jour du statut', 'error');
                    button.prop('disabled', false);
                    button.html(originalText);
                }
            },
            error: function(xhr, status, error) {
                console.error('Erreur AJAX:', error);
                showNotification('Erreur de connexion', 'error');
                button.prop('disabled', false);
                button.html(originalText);
            }
        });
    });
    
    // Auto-refresh pour le dashboard (toutes les 30 secondes)
    if (window.location.pathname.includes('dashboard') || window.location.pathname === '/') {
        setInterval(function() {
            refreshDashboardMetrics();
        }, 30000);
    }
    
    // Fonction pour rafraîchir les métriques du dashboard
    function refreshDashboardMetrics() {
        $('.card-metric').each(function() {
            const card = $(this);
            $.get(window.location.pathname, function(data) {
                const newCard = $(data).find('.card-metric').eq(card.index('.card-metric'));
                if (newCard.length) {
                    card.find('.card-body').html(newCard.find('.card-body').html());
                }
            }).fail(function() {
                console.log('Erreur lors du rafraîchissement des métriques');
            });
        });
    }
    
    // Fonction pour afficher des notifications
    function showNotification(message, type = 'info') {
        const alertClass = type === 'success' ? 'alert-success' : 
                          type === 'error' ? 'alert-danger' : 
                          type === 'warning' ? 'alert-warning' : 'alert-info';
        
        const notification = $(`
            <div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(notification);
        
        // Auto-remove après 5 secondes
        setTimeout(function() {
            notification.alert('close');
        }, 5000);
    }
    
    // Validation des formulaires
    $('form').on('submit', function(e) {
        const form = $(this);
        let isValid = true;
        
        // Vérifier les champs requis
        form.find('input[required], select[required], textarea[required]').each(function() {
            const field = $(this);
            if (!field.val().trim()) {
                field.addClass('is-invalid');
                isValid = false;
            } else {
                field.removeClass('is-invalid');
            }
        });
        
        // Validation spécifique pour les nombres
        form.find('input[type="number"]').each(function() {
            const field = $(this);
            const value = parseInt(field.val());
            const min = parseInt(field.attr('min'));
            
            if (field.val() && (isNaN(value) || (min !== undefined && value < min))) {
                field.addClass('is-invalid');
                isValid = false;
            } else {
                field.removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Veuillez corriger les erreurs dans le formulaire', 'error');
        }
    });
    
    // Suppression des classes d'erreur lors de la saisie
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid');
    });
    
    // Confirmation pour les actions destructives
    $('.btn-danger, .btn-outline-danger').on('click', function(e) {
        const action = $(this).text().trim();
        if (!confirm(`Êtes-vous sûr de vouloir ${action.toLowerCase()} ?`)) {
            e.preventDefault();
        }
    });
    
    // Tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide des messages d'alerte après 5 secondes
    setTimeout(function() {
        $('.alert:not(.alert-permanent)').fadeOut('slow');
    }, 5000);
    
    // Recherche en temps réel dans les tables
    $('#searchInput').on('keyup', function() {
        const value = $(this).val().toLowerCase();
        $('.table tbody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
    
    // Tri des colonnes de table
    $('.sortable').on('click', function() {
        const table = $(this).closest('table');
        const column = $(this).index();
        const rows = table.find('tbody tr').get();
        
        rows.sort(function(a, b) {
            const A = $(a).children('td').eq(column).text().toUpperCase();
            const B = $(b).children('td').eq(column).text().toUpperCase();
            
            if (A < B) return -1;
            if (A > B) return 1;
            return 0;
        });
        
        $.each(rows, function(index, row) {
            table.children('tbody').append(row);
        });
    });
    
    // Gestion des modales
    $('.modal').on('show.bs.modal', function() {
        $('body').addClass('modal-open');
    });
    
    $('.modal').on('hidden.bs.modal', function() {
        $('body').removeClass('modal-open');
    });
    
    // Impression
    $('.btn-print').on('click', function() {
        window.print();
    });
    
    // Export CSV (fonction basique)
    $('.btn-export-csv').on('click', function() {
        const table = $('.table-alerts');
        let csv = [];
        
        // Headers
        const headers = [];
        table.find('thead th').each(function() {
            headers.push($(this).text().trim());
        });
        csv.push(headers.join(','));
        
        // Rows
        table.find('tbody tr').each(function() {
            const row = [];
            $(this).find('td').each(function() {
                row.push('"' + $(this).text().trim().replace(/"/g, '""') + '"');
            });
            csv.push(row.join(','));
        });
        
        // Download
        const csvContent = csv.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', 'alertes_export.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    // Gestion des erreurs globales AJAX
    $(document).ajaxError(function(event, xhr, settings, thrownError) {
        console.error('Erreur AJAX:', thrownError);
        if (xhr.status === 403) {
            showNotification('Accès refusé. Veuillez vous reconnecter.', 'error');
        } else if (xhr.status === 500) {
            showNotification('Erreur serveur. Veuillez réessayer plus tard.', 'error');
        }
    });
    
    // Indicateur de chargement global
    $(document).ajaxStart(function() {
        $('body').addClass('loading');
    }).ajaxStop(function() {
        $('body').removeClass('loading');
    });
    
    console.log('Application de gestion des alertes initialisée');
});

// Fonctions utilitaires globales
window.AlertesApp = {
    // Formater une date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR') + ' ' + date.toLocaleTimeString('fr-FR');
    },
    
    // Obtenir la couleur du badge selon le statut
    getStatusBadgeClass: function(status) {
        const classes = {
            'en_cours': 'bg-warning',
            'livre': 'bg-success',
            'flc': 'bg-info',
            'cloture': 'bg-secondary'
        };
        return classes[status] || 'bg-secondary';
    },
    
    // Obtenir la couleur selon le nombre de bacs
    getBacsColorClass: function(nombre) {
        if (nombre > 10) return 'bg-success';
        if (nombre > 5) return 'bg-warning';
        return 'bg-danger';
    }
};
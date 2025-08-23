from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_alerte, name='create_alerte'),
    path('list/', views.list_alertes, name='list_alertes'),
    path('update-statut/<int:alerte_id>/', views.update_statut, name='update_statut'),
]
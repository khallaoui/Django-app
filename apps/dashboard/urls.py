from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('next-previous-demo/', views.next_previous_demo_view, name='next_previous_demo'),
]
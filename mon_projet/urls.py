from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_stock_dashboard(request):
    return redirect('stock_debord:dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_stock_dashboard, name='home'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('auth/', include('apps.authentication.urls', namespace='auth')),
    path('stock-debord/', include('stock_debord.urls')),
]
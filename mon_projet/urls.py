from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('alertes/', include('apps.alertes.urls')),
    path('stock-debord/', include('stock_debord.urls')),
]
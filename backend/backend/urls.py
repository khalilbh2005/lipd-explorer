# backend/urls.py
# URLs globales du projet Django.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # Toutes les URLs /api/... sont gérées par l'app "api"
    path('api/', include('api.urls')),
]
# api/urls.py
# Définit les URLs spécifiques à l'app "api".

from django.urls import path
from . import views

# Toutes les URLs ici seront préfixées par /api/ (voir backend/urls.py)
urlpatterns = [
    # GET /api/datasets/
    path('datasets/', views.liste_datasets, name='liste_datasets'),
    
    # GET /api/datasets/ODP846/
    path('datasets/<str:nom_dataset>/', views.detail_dataset, name='detail_dataset'),
    # GET /api/datasets/<nom>/variables/<id>/  ← 🆕 NOUVELLE ROUTE
    path('datasets/<str:nom_dataset>/variables/<int:id_variable>/',
         views.data_points_variable,
         name='data_points_variable'),

]
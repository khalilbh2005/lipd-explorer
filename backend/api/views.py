# api/views.py
# Les vues sont les fonctions qui répondent aux requêtes HTTP.
# Elles utilisent le service lipd_service pour faire le boulot.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import lipd_service


# Liste des datasets disponibles dans notre application
# (Pour l'instant on n'a que celui embarqué dans PyLiPD)
DATASETS_DISPONIBLES = [
    {
        "id": "ODP846",
        "name": "ODP846.Lawrence.2006",
        "description": "Carotte sédimentaire océanique - Pacifique équatorial - 5 millions d'années",
        "archiveType": "Marine sediment",
    },
]


# ============================================================
# ENDPOINT 1 : GET /api/datasets/
# ============================================================
@api_view(['GET'])
def liste_datasets(requete):
    """
    Retourne la liste de tous les datasets disponibles.
    
    URL : GET /api/datasets/
    """
    reponse = {
        "count": len(DATASETS_DISPONIBLES),
        "results": DATASETS_DISPONIBLES,
    }
    return Response(reponse, status=status.HTTP_200_OK)


# ============================================================
# ENDPOINT 2 : GET /api/datasets/<nom>/
# ============================================================
@api_view(['GET'])
def detail_dataset(requete, nom_dataset):
    """
    Retourne les métadonnées et variables d'un dataset.
    
    URL : GET /api/datasets/ODP846/
    """
    # Étape 1 : charger le dataset
    lipd = lipd_service.charger_dataset(nom_dataset)
    
    if lipd is None:
        return Response(
            {"error": f"Dataset '{nom_dataset}' introuvable"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Étape 2 : extraire les métadonnées
    metadonnees = lipd_service.obtenir_metadonnees(lipd)
    
    # Étape 3 : extraire la liste des variables
    variables = lipd_service.obtenir_liste_variables(lipd)
    
    # Étape 4 : construire la réponse
    reponse = {
        "metadata": metadonnees,
        "variables": variables,
    }
    
    return Response(reponse, status=status.HTTP_200_OK)

# ============================================================
# ENDPOINT 3 : GET /api/datasets/<nom>/variables/<id>/
# ============================================================
@api_view(['GET'])
def data_points_variable(requete, nom_dataset, id_variable):
    """
    Retourne les data points (temps, valeur) d'une variable spécifique.
    
    URL : GET /api/datasets/ODP846/variables/0/
    """
    # Étape 1 : charger le dataset
    lipd = lipd_service.charger_dataset(nom_dataset)
    
    if lipd is None:
        return Response(
            {"error": f"Dataset '{nom_dataset}' introuvable"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Étape 2 : extraire les data points
    data = lipd_service.obtenir_data_points(lipd, id_variable)
    
    if data is None:
        return Response(
            {"error": f"Variable {id_variable} introuvable ou non numérique"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response(data, status=status.HTTP_200_OK)
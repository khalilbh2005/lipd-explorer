# api/lipd_service.py
# Service qui encapsule toute la logique PyLiPD.
# Les vues Django appellent ces fonctions, jamais PyLiPD directement.

import math
import numpy as np
from pylipd.utils.dataset import load_datasets


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def est_une_liste_de_nombres(liste):
    """
    Vérifie qu'une liste/array contient uniquement des nombres.
    Gère les types Python (int, float) ET numpy (int64, float64, etc.).
    """
    if liste is None:
        return False
    
    try:
        if len(liste) == 0:
            return False
    except TypeError:
        return False
    
    for element in liste:
        if isinstance(element, (int, float, np.number)):
            continue
        try:
            float(element)
        except (ValueError, TypeError):
            return False
    
    return True


def trouver_min(liste):
    """Retourne la valeur minimale d'une liste (ignore les NaN)."""
    minimum = None
    for valeur in liste:
        try:
            v = float(valeur)
            if math.isnan(v):
                continue
            if minimum is None or v < minimum:
                minimum = v
        except (ValueError, TypeError):
            continue
    return minimum


def trouver_max(liste):
    """Retourne la valeur maximale d'une liste (ignore les NaN)."""
    maximum = None
    for valeur in liste:
        try:
            v = float(valeur)
            if math.isnan(v):
                continue
            if maximum is None or v > maximum:
                maximum = v
        except (ValueError, TypeError):
            continue
    return maximum


def nettoyer_pour_json(valeur):
    """
    Nettoie une valeur pour qu'elle soit compatible JSON.
    Convertit NaN, Infinity, et les types numpy en types Python standards.
    """
    if valeur is None:
        return None
    
    if isinstance(valeur, dict):
        resultat = {}
        for cle, val in valeur.items():
            resultat[cle] = nettoyer_pour_json(val)
        return resultat
    
    if isinstance(valeur, (list, tuple)):
        resultat = []
        for element in valeur:
            resultat.append(nettoyer_pour_json(element))
        return resultat
    
    if isinstance(valeur, np.ndarray):
        return nettoyer_pour_json(valeur.tolist())
    
    if isinstance(valeur, np.integer):
        return int(valeur)
    
    if isinstance(valeur, np.floating):
        nombre = float(valeur)
        if math.isnan(nombre) or math.isinf(nombre):
            return None
        return nombre
    
    if isinstance(valeur, float):
        if math.isnan(valeur) or math.isinf(valeur):
            return None
        return valeur
    
    return valeur


# ============================================================
# FONCTIONS PRINCIPALES (utilisées par les vues Django)
# ============================================================

def charger_dataset(nom_dataset):
    """Charge un dataset LiPD depuis les données embarquées dans PyLiPD."""
    try:
        lipd = load_datasets(names=nom_dataset)
        return lipd
    except Exception as erreur:
        print(f"❌ Erreur de chargement : {erreur}")
        return None


def obtenir_metadonnees(lipd):
    """Extrait les métadonnées descriptives d'un dataset LiPD."""
    noms = lipd.get_all_dataset_names()
    if len(noms) == 0:
        return None
    
    nom = noms[0]
    raw = lipd.get_lipd(nom)
    
    # Géolocalisation
    geo = raw.get('geo', {})
    coords = []
    site = "Inconnu"
    
    if geo:
        geometry = geo.get('geometry', {})
        coords = geometry.get('coordinates', [])
        properties = geo.get('properties', {})
        site = properties.get('siteName', 'Inconnu')
    
    longitude = None
    latitude = None
    elevation = None
    
    if len(coords) >= 2:
        longitude = coords[0]
        latitude = coords[1]
    if len(coords) >= 3:
        elevation = coords[2]
    
    # Publication
    publications = raw.get('pub', [])
    publication = None
    
    if len(publications) > 0:
        pub = publications[0]
        auteurs = pub.get('author', [])
        
        noms_auteurs = []
        for auteur in auteurs:
            nom_auteur = auteur.get('name', '')
            if nom_auteur:
                noms_auteurs.append(nom_auteur)
        
        publication = {
            "authors": noms_auteurs,
            "year": pub.get('year'),
            "journal": pub.get('journal'),
            "title": pub.get('title'),
            "doi": pub.get('doi'),
        }
    
    paleo_data = raw.get('paleoData', [])
    chron_data = raw.get('chronData', [])
    
    metadonnees = {
        "dataSetName": raw.get('dataSetName'),
        "archiveType": raw.get('archiveType'),
        "location": {
            "siteName": site,
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation,
        },
        "publication": publication,
        "structure": {
            "paleoDataTables": len(paleo_data),
            "chronDataTables": len(chron_data),
        }
    }
    
    return nettoyer_pour_json(metadonnees)


def obtenir_liste_variables(lipd):
    """Extrait la liste des variables paléo d'un dataset LiPD."""
    df = lipd.get_timeseries_essentials()
    variables = []
    
    for index in range(len(df)):
        ligne = df.iloc[index]
        
        temps = ligne.get('time_values')
        valeurs = ligne.get('paleoData_values')
        
        temps_ok = est_une_liste_de_nombres(temps)
        valeurs_ok = est_une_liste_de_nombres(valeurs)
        
        if temps_ok and valeurs_ok:
            statut = "complete"
            nb_points = len(temps)
        elif temps_ok and not valeurs_ok:
            statut = "non-numeric"
            nb_points = len(temps)
        else:
            statut = "incomplete"
            nb_points = 0
            if temps is not None:
                try:
                    nb_points = len(temps)
                except TypeError:
                    nb_points = 0
        
        variable = {
            "id": index,
            "name": ligne.get('paleoData_variableName'),
            "units": ligne.get('paleoData_units'),
            "proxy": ligne.get('paleoData_proxy'),
            "timeAxisName": ligne.get('time_variableName'),
            "timeUnits": ligne.get('time_units'),
            "status": statut,
            "numberOfPoints": nb_points,
        }
        
        variables.append(variable)
    
    return nettoyer_pour_json(variables)


def obtenir_data_points(lipd, id_variable):
    """Récupère les points (temps, valeur) d'une variable spécifique."""
    df = lipd.get_timeseries_essentials()
    
    if id_variable < 0 or id_variable >= len(df):
        return None
    
    ligne = df.iloc[id_variable]
    
    temps = ligne.get('time_values')
    valeurs = ligne.get('paleoData_values')
    
    if not est_une_liste_de_nombres(temps):
        return None
    if not est_une_liste_de_nombres(valeurs):
        return None
    
    # Construction de la liste des points
    points = []
    nombre_points = len(temps)
    for i in range(nombre_points):
        try:
            t = float(temps[i])
            v = float(valeurs[i])
            # On ignore les paires contenant un NaN
            if math.isnan(t) or math.isnan(v):
                continue
            point = {
                "time": t,
                "value": v
            }
            points.append(point)
        except (ValueError, TypeError):
            continue
    
    reponse = {
        "variableId": id_variable,
        "variable": {
            "name": ligne.get('paleoData_variableName'),
            "units": ligne.get('paleoData_units'),
            "proxy": ligne.get('paleoData_proxy'),
        },
        "timeAxis": {
            "name": ligne.get('time_variableName'),
            "units": ligne.get('time_units'),
        },
        "stats": {
            "totalPoints": len(points),
            "timeMin": trouver_min(temps),
            "timeMax": trouver_max(temps),
            "valueMin": trouver_min(valeurs),
            "valueMax": trouver_max(valeurs),
        },
        "dataPoints": points,
    }
    
    return nettoyer_pour_json(reponse)
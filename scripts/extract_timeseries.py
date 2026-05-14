# extract_timeseries.py
# Extraction des séries temporelles paléoclimatiques avec PyLiPD
# Version pédagogique : code simple, boucles classiques, vérifications explicites

from pylipd.utils.dataset import load_datasets
import json


# ============================================================
# FONCTIONS UTILITAIRES (pour rendre le code lisible)
# ============================================================

def est_une_liste_de_nombres(liste):
    """
    Vérifie qu'une liste existe, n'est pas vide,
    et que tous ses éléments sont des nombres (int ou float).
    """
    # Cas 1 : la liste n'existe pas
    if liste is None:
        return False
    
    # Cas 2 : la liste est vide
    if len(liste) == 0:
        return False
    
    # Cas 3 : on vérifie chaque élément
    for element in liste:
        if not isinstance(element, (int, float)):
            return False
    
    return True


def trouver_min(liste):
    """Retourne la valeur minimale d'une liste de nombres."""
    minimum = liste[0]
    for valeur in liste:
        if valeur < minimum:
            minimum = valeur
    return minimum


def trouver_max(liste):
    """Retourne la valeur maximale d'une liste de nombres."""
    maximum = liste[0]
    for valeur in liste:
        if valeur > maximum:
            maximum = valeur
    return maximum


# ============================================================
# ÉTAPE 1 : CHARGEMENT DU DATASET
# ============================================================

print("📥 Chargement du dataset ODP846...")
lipd = load_datasets(names='ODP846')
print("✅ Dataset chargé\n")


# ============================================================
# ÉTAPE 2 : EXTRACTION DES SÉRIES TEMPORELLES
# ============================================================

print("🔍 Extraction des séries temporelles...")
df = lipd.get_timeseries_essentials()
print(f"📈 Nombre total de séries trouvées : {len(df)}\n")


# ============================================================
# ÉTAPE 3 : CLASSIFICATION DES SÉRIES
# ============================================================

print("=" * 70)
print("📊 CLASSIFICATION DES SÉRIES")
print("=" * 70)

# On va trier les séries en 3 catégories
series_completes = []        # temps numérique + valeurs numériques
series_non_numeriques = []   # valeurs non numériques (ex: site/hole)
series_incompletes = []      # temps ou valeurs manquantes

# Boucle classique sur toutes les lignes du DataFrame
for index in range(len(df)):
    ligne = df.iloc[index]
    
    temps = ligne.get('time_values')
    valeurs = ligne.get('paleoData_values')
    nom_variable = ligne.get('paleoData_variableName')
    
    # Test 1 : est-ce qu'il y a un axe temporel valide ?
    temps_ok = est_une_liste_de_nombres(temps)
    
    # Test 2 : est-ce qu'il y a des valeurs numériques ?
    valeurs_ok = est_une_liste_de_nombres(valeurs)
    
    # Classification
    if temps_ok and valeurs_ok:
        series_completes.append(index)
    elif temps_ok and not valeurs_ok:
        series_non_numeriques.append(index)
    else:
        series_incompletes.append(index)

# Affichage du résumé
print(f"✅ Séries complètes (numériques)    : {len(series_completes)}")
print(f"📝 Séries non numériques (textuelles): {len(series_non_numeriques)}")
print(f"⚠️  Séries incomplètes               : {len(series_incompletes)}")


# ============================================================
# ÉTAPE 4 : AFFICHAGE DES SÉRIES NON NUMÉRIQUES
# ============================================================

print("\n" + "=" * 70)
print("📝 SÉRIES NON NUMÉRIQUES (variables textuelles)")
print("=" * 70)

for index in series_non_numeriques:
    ligne = df.iloc[index]
    nom = ligne.get('paleoData_variableName', 'N/A')
    valeurs = ligne.get('paleoData_values')
    
    # On affiche les 3 premières valeurs pour comprendre
    if valeurs is not None and len(valeurs) > 0:
        premieres_valeurs = []
        for i in range(min(3, len(valeurs))):
            premieres_valeurs.append(str(valeurs[i]))
        apercu = ", ".join(premieres_valeurs)
        print(f"   • {nom:30s} → exemples : {apercu}")


# ============================================================
# ÉTAPE 5 : APERÇU DÉTAILLÉ DES SÉRIES COMPLÈTES
# ============================================================

print("\n" + "=" * 70)
print("✅ APERÇU DES SÉRIES TEMPORELLES COMPLÈTES (numériques)")
print("=" * 70)

# On limite à 5 séries pour ne pas surcharger l'affichage
nombre_a_afficher = min(5, len(series_completes))

for compteur in range(nombre_a_afficher):
    index = series_completes[compteur]
    ligne = df.iloc[index]
    
    temps = ligne['time_values']
    valeurs = ligne['paleoData_values']
    
    # Calcul des min/max avec nos fonctions
    temps_min = trouver_min(temps)
    temps_max = trouver_max(temps)
    valeur_min = trouver_min(valeurs)
    valeur_max = trouver_max(valeurs)
    
    print(f"\n🔬 Série #{compteur + 1}")
    print(f"   Variable        : {ligne.get('paleoData_variableName', 'N/A')}")
    print(f"   Unité           : {ligne.get('paleoData_units', 'N/A')}")
    print(f"   Proxy           : {ligne.get('paleoData_proxy', 'N/A')}")
    print(f"   Archive         : {ligne.get('archiveType', 'N/A')}")
    print(f"   Axe temporel    : {ligne.get('time_variableName', 'N/A')} ({ligne.get('time_units', 'N/A')})")
    print(f"   Nombre de points: {len(temps)}")
    print(f"   Période         : {temps_min:.0f} → {temps_max:.0f}")
    print(f"   Valeurs min/max : {valeur_min:.3f} / {valeur_max:.3f}")


# ============================================================
# ÉTAPE 6 : GÉNÉRATION DU JSON POUR L'API DJANGO
# ============================================================

print("\n" + "=" * 70)
print("💾 FORMAT JSON POUR L'API DJANGO → VUE.JS")
print("=" * 70)

if len(series_completes) > 0:
    # On prend la première série complète
    index_premiere = series_completes[0]
    premiere_serie = df.iloc[index_premiere]
    
    temps = premiere_serie['time_values']
    valeurs = premiere_serie['paleoData_values']
    
    # Construction des points (5 premiers pour la démo)
    points = []
    nombre_points = min(5, len(temps))
    for i in range(nombre_points):
        point = {
            "time": float(temps[i]),
            "value": float(valeurs[i])
        }
        points.append(point)
    
    # Construction de la réponse complète
    reponse_api = {
        "dataSetName": premiere_serie.get('dataSetName'),
        "archiveType": premiere_serie.get('archiveType'),
        "variable": {
            "name": premiere_serie.get('paleoData_variableName'),
            "units": premiere_serie.get('paleoData_units'),
            "proxy": premiere_serie.get('paleoData_proxy'),
        },
        "timeAxis": {
            "name": premiere_serie.get('time_variableName'),
            "units": premiere_serie.get('time_units'),
        },
        "location": {
            "latitude": premiere_serie.get('geo_meanLat'),
            "longitude": premiere_serie.get('geo_meanLon'),
        },
        "stats": {
            "totalPoints": len(temps),
            "timeMin": float(trouver_min(temps)),
            "timeMax": float(trouver_max(temps)),
            "valueMin": float(trouver_min(valeurs)),
            "valueMax": float(trouver_max(valeurs)),
        },
        "dataPoints": points
    }
    
    print("\n🎯 Réponse JSON type :")
    print(json.dumps(reponse_api, indent=2, default=str))
else:
    print("⚠️  Aucune série complète trouvée dans ce dataset.")

print("\n✅ Script terminé.")
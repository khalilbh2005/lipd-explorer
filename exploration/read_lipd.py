# read_lipd.py
# Lecture propre d'un fichier LiPD avec PyLiPD
from pylipd.utils.dataset import load_datasets

# Charge le dataset embarqué
print("📥 Chargement du dataset ODP846...")
lipd = load_datasets(names='ODP846')

# Récupère le nom du dataset
dataset_names = lipd.get_all_dataset_names()
dataset_name = dataset_names[0]
print(f"📊 Dataset : {dataset_name}\n")

# Récupère les métadonnées sous forme de dictionnaire Python
metadata = lipd.get_lipd(dataset_name)

# ===== AFFICHAGE STRUCTURÉ DES MÉTADONNÉES =====
print("=" * 70)
print("📋 MÉTADONNÉES DESCRIPTIVES")
print("=" * 70)

print(f"  Nom du dataset  : {metadata.get('dataSetName', 'N/A')}")
print(f"  Type d'archive  : {metadata.get('archiveType', 'N/A')}")

# Géolocalisation
print("\n🌍 GÉOLOCALISATION")
print("-" * 70)
geo = metadata.get('geo', {})
if geo:
    geometry = geo.get('geometry', {})
    coords = geometry.get('coordinates', [])
    properties = geo.get('properties', {})
    
    print(f"  Site          : {properties.get('siteName', 'N/A')}")
    if len(coords) >= 2:
        print(f"  Longitude     : {coords[0]}")
        print(f"  Latitude      : {coords[1]}")
    if len(coords) >= 3:
        print(f"  Élévation     : {coords[2]} m")

# Publication
print("\n📚 PUBLICATION SOURCE")
print("-" * 70)
pubs = metadata.get('pub', [])
if pubs:
    pub = pubs[0]
    authors = pub.get('author', [])
    if authors:
        author_names = [a.get('name', '') for a in authors]
        print(f"  Auteurs       : {', '.join(author_names[:3])}{'...' if len(authors) > 3 else ''}")
    print(f"  Année         : {pub.get('year', 'N/A')}")
    print(f"  Journal       : {pub.get('journal', 'N/A')}")
    title = pub.get('title', '')
    print(f"  Titre         : {title[:80]}{'...' if len(title) > 80 else ''}")
    print(f"  DOI           : {pub.get('doi', 'N/A')}")

# Nombre de variables paléo
print("\n📈 STRUCTURE DES DONNÉES")
print("-" * 70)
paleo_data = metadata.get('paleoData', [])
chron_data = metadata.get('chronData', [])
print(f"  Tables paleoData : {len(paleo_data)}")
print(f"  Tables chronData : {len(chron_data)}")

# Liste des variables paléo
if paleo_data:
    for i, pd in enumerate(paleo_data):
        measurement_tables = pd.get('measurementTable', [])
        for j, mt in enumerate(measurement_tables):
            cols = mt.get('columns', [])
            print(f"\n  📊 paleoData[{i}].measurementTable[{j}] : {len(cols)} colonnes")
            for col in cols:
                var_name = col.get('variableName', '?')
                units = col.get('units', '?')
                print(f"     - {var_name:25s} (unité: {units})")
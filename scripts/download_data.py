# download_data.py
# Charge un dataset paléoclimatique d'exemple fourni avec PyLiPD
from pylipd.utils.dataset import load_datasets

print("📥 Chargement du dataset d'exemple ODP846...")
print("   (Carotte sédimentaire océanique - Pacifique équatorial)")
print("   Référence : Lawrence et al., 2006\n")

# load_datasets() charge un dataset embarqué dans le package PyLiPD
# Aucun téléchargement nécessaire : le fichier est sur ton disque
lipd = load_datasets(names='ODP846')

# Affiche les datasets chargés
print("\n✅ Dataset chargé avec succès !")
print(f"📊 Datasets disponibles : {lipd.get_all_dataset_names()}")
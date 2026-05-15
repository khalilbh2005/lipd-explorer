# explore_raw.py
# Démonstration : un .lpd est un fichier ZIP qui contient JSON-LD + CSV
# On va l'ouvrir "à la main" pour voir sa structure interne

import zipfile
import os
import pylipd

# Localise le fichier .lpd embarqué dans le package PyLiPD installé
pylipd_dir = os.path.dirname(pylipd.__file__)
print(f"📂 Dossier d'installation de PyLiPD : {pylipd_dir}\n")

# Cherche le fichier .lpd dans le dossier data/ du package
lpd_file = None
for root, dirs, files in os.walk(pylipd_dir):
    for f in files:
        if f.endswith('.lpd'):
            lpd_file = os.path.join(root, f)
            print(f"✅ Fichier .lpd trouvé : {lpd_file}")
            break
    if lpd_file:
        break

if not lpd_file:
    print("❌ Aucun fichier .lpd trouvé dans le package PyLiPD")
    exit(1)

print(f"\n🔍 Exploration brute du fichier {os.path.basename(lpd_file)}")
print("=" * 70)

# Ouvre le .lpd comme un ZIP
with zipfile.ZipFile(lpd_file, 'r') as z:
    print("📂 Contenu interne :")
    print("-" * 70)
    for name in z.namelist():
        info = z.getinfo(name)
        size_kb = info.file_size / 1024
        print(f"  {name:50s}  ({size_kb:.2f} Ko)")
    print("-" * 70)
    
    # Lit le contenu de bagit.txt (le fichier de description du format BagIt)
    print("\n📜 Contenu de bagit.txt :")
    print("-" * 70)
    try:
        with z.open('bagit.txt') as bagit_file:
            print(bagit_file.read().decode('utf-8'))
    except KeyError:
        print("⚠️  bagit.txt non trouvé")
    
    # Trouve et affiche les premières lignes du JSON-LD
    print("📜 Aperçu de metadata.jsonld (premiers 800 caractères) :")
    print("-" * 70)
    for name in z.namelist():
        if name.endswith('.jsonld'):
            with z.open(name) as jsonld_file:
                content = jsonld_file.read().decode('utf-8')
                print(content[:800])
                print(f"\n... ({len(content)} caractères au total)")
            break
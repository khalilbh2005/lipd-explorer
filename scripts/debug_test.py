# debug_test.py
# Script de debug pur pour comprendre les types de données
import math
import numpy as np
from pylipd.utils.dataset import load_datasets

print("📥 Chargement du dataset...")
lipd = load_datasets(names='ODP846')

df = lipd.get_timeseries_essentials()
print(f"📊 Nombre de séries : {len(df)}\n")

# On regarde la première série
print("=" * 70)
print("🔍 ANALYSE DE LA SÉRIE #0")
print("=" * 70)

ligne = df.iloc[0]

# Récupération
temps = ligne.get('time_values')
valeurs = ligne.get('paleoData_values')

# Type des conteneurs
print(f"\n📋 type(temps)   = {type(temps)}")
print(f"📋 type(valeurs) = {type(valeurs)}")

# Longueurs
print(f"\n📏 len(temps)   = {len(temps) if temps is not None else 'None'}")
print(f"📏 len(valeurs) = {len(valeurs) if valeurs is not None else 'None'}")

# Type des éléments individuels
if temps is not None and len(temps) > 0:
    print(f"\n🧪 temps[0]   = {temps[0]!r}")
    print(f"🧪 type(temps[0]) = {type(temps[0])}")
    print(f"🧪 isinstance(temps[0], int) = {isinstance(temps[0], int)}")
    print(f"🧪 isinstance(temps[0], float) = {isinstance(temps[0], float)}")
    print(f"🧪 isinstance(temps[0], np.number) = {isinstance(temps[0], np.number)}")
    print(f"🧪 isinstance(temps[0], np.integer) = {isinstance(temps[0], np.integer)}")
    print(f"🧪 isinstance(temps[0], np.floating) = {isinstance(temps[0], np.floating)}")

if valeurs is not None and len(valeurs) > 0:
    print(f"\n🧪 valeurs[0] = {valeurs[0]!r}")
    print(f"🧪 type(valeurs[0]) = {type(valeurs[0])}")
    print(f"🧪 isinstance(valeurs[0], int) = {isinstance(valeurs[0], int)}")
    print(f"🧪 isinstance(valeurs[0], float) = {isinstance(valeurs[0], float)}")
    print(f"🧪 isinstance(valeurs[0], np.number) = {isinstance(valeurs[0], np.number)}")

# Test de la conversion float()
if temps is not None and len(temps) > 0:
    print(f"\n🔄 float(temps[0]) = {float(temps[0])}")
if valeurs is not None and len(valeurs) > 0:
    print(f"🔄 float(valeurs[0]) = {float(valeurs[0])}")

# Version numpy installée
print(f"\n📦 numpy version : {np.__version__}")
#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

# Sources des données : production de M. Forriez, 2016-2023

# coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# 1. OUVERTURE DES DONNÉES
# =========================

def ouvrir_fichier_csv(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        df = pd.read_csv(fichier)
    return df

# Données élections
elections = ouvrir_fichier_csv("./data/resultats-elections-presidentielles-2022-1er-tour.csv")

# =========================
# 2. SÉLECTION DES VARIABLES QUANTITATIVES
# =========================

donnees_quantitatives = elections.select_dtypes(include=[np.number])

# =========================
# 3. PARAMÈTRES STATISTIQUES
# =========================

moyennes = donnees_quantitatives.mean()
medians = donnees_quantitatives.median()
modes = donnees_quantitatives.mode().iloc[0]
ecart_type = donnees_quantitatives.std()

# écart absolu à la moyenne
ecart_absolu = (donnees_quantitatives.sub(moyennes)).abs().mean()

# étendue
etendue = donnees_quantitatives.max() - donnees_quantitatives.min()

# Arrondi à 2 décimales
parametres = pd.DataFrame({
    "Moyenne": moyennes.round(2),
    "Médiane": medians.round(2),
    "Mode": modes.round(2),
    "Écart-type": ecart_type.round(2),
    "Écart absolu moyen": ecart_absolu.round(2),
    "Étendue": etendue.round(2)
})

print("\nPARAMÈTRES STATISTIQUES :\n")
print(parametres)

# =========================
# 4. QUANTILES
# =========================

q1 = donnees_quantitatives.quantile(0.25)
q3 = donnees_quantitatives.quantile(0.75)
d1 = donnees_quantitatives.quantile(0.10)
d9 = donnees_quantitatives.quantile(0.90)

distance_interquartile = q3 - q1
distance_interdecile = d9 - d1

print("\nDISTANCE INTERQUARTILE :\n")
print(distance_interquartile.round(2))

print("\nDISTANCE INTERDÉCILE :\n")
print(distance_interdecile.round(2))

# =========================
# 5. BOÎTES À MOUSTACHES
# =========================

os.makedirs("./img", exist_ok=True)

for colonne in donnees_quantitatives.columns:
    plt.figure()
    plt.boxplot(donnees_quantitatives[colonne].dropna())
    plt.title(f"Boîte à moustaches – {colonne}")
    plt.ylabel(colonne)
    plt.savefig(f"./img/boxplot_{colonne}.png")
    plt.close()

# =========================
# 6. DONNÉES DES ÎLES
# =========================

iles = ouvrir_fichier_csv("./data/island-index.csv")

surfaces = iles["Surface (km2)"]

classes = {
    "]0,10]": 0,
    "]10,25]": 0,
    "]25,50]": 0,
    "]50,100]": 0,
    "]100,2500]": 0,
    "]2500,5000]": 0,
    "]5000,10000]": 0,
    "]10000,+∞[": 0
}

for surface in surfaces:
    if surface <= 10:
        classes["]0,10]"] += 1
    elif surface <= 25:
        classes["]10,25]"] += 1
    elif surface <= 50:
        classes["]25,50]"] += 1
    elif surface <= 100:
        classes["]50,100]"] += 1
    elif surface <= 2500:
        classes["]100,2500]"] += 1
    elif surface <= 5000:
        classes["]2500,5000]"] += 1
    elif surface <= 10000:
        classes["]5000,10000]"] += 1
    else:
        classes["]10000,+∞["] += 1

print("\nRÉPARTITION DES ÎLES PAR SURFACE :\n")
for classe, effectif in classes.items():
    print(classe, ":", effectif)

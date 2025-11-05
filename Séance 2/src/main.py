#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as fichier:
    contenu = pd.read_csv(fichier)

# Mettre dans un commentaire le numéro de la question
# Question 1

# Affichage du tableau
print(contenu)
pd.dataFrame(contenu)

# Nombre de lignes et colonnes
print("Nombre de lignes :", len(contenu))
print("Nombre de colonnes :", len(contenu.columns))

# Types de colonnes
types_colonnes = {}
for col in contenu.columns:
    types_colonnes[col] = contenu[col].dtype
print("Types de colonnes :", types_colonnes)

# Affichage des noms de colonnes
print("Noms des colonnes :", contenu.columns.tolist())

# Sélection du nombre d'inscrits
if 'Inscrits' in contenu.columns:
    inscrits = contenu['Inscrits']
    print("Inscrits :", inscrits)

# Calcul des effectifs pour les colonnes quantitatives
effectifs = []
for col in contenu.columns:
    if contenu[col].dtype in ['int64', 'float64']:
        effectifs.append((col, contenu[col].sum()))
print("Effectifs :", effectifs)

# Création du dossier images
os.makedirs('images', exist_ok=True)

# Diagrammes en barres pour inscrits et votants
for i, row in contenu.iterrows():
    departement = row['Code département']
    valeurs = [row['Inscrits'], row['Votants']]
    noms = ['Inscrits', 'Votants']
    plt.bar(noms, valeurs)
    plt.title(f'Département {departement}')
    plt.savefig(f'images/bar_{departement}.png')
    plt.clf()

# Diagrammes circulaires pour blancs, nuls, exprimés, abstention
for i, row in contenu.iterrows():
    departement = row['Code département']
    valeurs = [row['Blancs'], row['Nuls'], row['Exprimés'], row['Abstentions']]
    noms = ['Blancs', 'Nuls', 'Exprimés', 'Abstentions']
    plt.pie(valeurs, labels=noms, autopct='%1.1f%%')
    plt.title(f'Département {departement}')
    plt.savefig(f'images/pie_{departement}.png')
    plt.clf()

# Histogramme de la distribution des inscrits
plt.hist(contenu['Inscrits'], bins='sturges', density=True)
plt.title('Distribution des inscrits')
plt.xlabel('Nombre d’inscrits')
plt.ylabel('Densité')
plt.savefig('images/histogramme_inscrits.png')
plt.clf()




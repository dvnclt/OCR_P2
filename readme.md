# Système de Surveillance des Prix - Books to Scrape

## Introduction

Ce projet vise à créer un système de surveillance des prix pour le site "Books to Scrape", en élaborant une version bêta. 
Le système extrait les données des produits disponibles sur le site et les stock dans des fichiers CSV, tout en téléchargeant également les images correspondantes.


## Fonctionnalités

- Extraction des URLs des produits par catégorie
- Collecte des données des produits : titre, URL de la page produit, code UPC, prix TTC, prix HT, disponibilité, description, catégorie, notation et URL de l'image
- Écriture des données dans des fichiers CSV organisés par catégorie
- Téléchargement des images des produits dans des dossiers organisés par catégorie
- Vérification de l'intégrité des données extraites


## Installation

1. Clonez ce dépôt sur votre machine locale :
   git clone https://github.com/dvnclt/OCR-projet_2.git

2. Installer les dépendances à l'aide de pip :
   pip install -r requirements.txt
   

## Utilisation

1. Exécutez le script principal "main.py" :
   python main.py

2. Les données seront extraites, traitées et stockées (par catégorie) dans des fichiers CSV contenus dans le dossier csv_directory.
   Les images seront téléchargées dans le dossier images_directory.

## Auteur

Ce projet a été réalisé par Damien Vincelot.
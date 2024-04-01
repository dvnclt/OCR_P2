# Import des différents modules, fonctions et listes nécessaires
import requests
from bs4 import BeautifulSoup
import os
import time
from utils import collect_product_urls, collect_product_data, write_data_csv, images_download
from utils import product_link_list, product_title_list, product_page_url_list, universal_product_code_list, price_including_tax_list, price_excluding_tax_list, number_available_list, product_description_list, category_list, review_rating_list, image_url_list
from utils import count

# Débute un timer pour connaître le temps d'exécution du programme
start_time = time.time()

# Création d'une liste servant à stocker l'ensemble des urls pour chaque catégorie
category_link_list = []

# Création des dossiers pour les fichiers csv et images
csv_folder = "csv_directory"
os.makedirs(csv_folder, exist_ok=True)
image_folder = "images_directory"
os.makedirs(image_folder, exist_ok=True)

try :
    # Obtention et analyse du contenu de la page d'accueil du site dans le but de rechercher chaque urls catégorie
    response = requests.get("https://books.toscrape.com/catalogue/page-1.html")
    response.raise_for_status()  # Vérifie si la requête a réussi, sinon lève une exception
    soup = BeautifulSoup(response.content, "html.parser")
    category_link = soup.find("ul", class_="nav nav-list").find("ul").find_all("a", href=True)

    # Pour chaque urls catégorie trouvée, appelle la fonction permettant la recherche de chaque url produit
    for category_item in category_link:
        full_category_link = "https://books.toscrape.com/catalogue/" + category_item['href']
        category_link_list.append(full_category_link)
        category_csv_name = full_category_link.split('/')[-2].split('_')[0]
        collect_product_urls(full_category_link)

        # Pour chaque url produit, appelle la fonction permetant la collecte de l'ensemble des données souhaitées
        for product_item in product_link_list:
            collect_product_data(product_item)

        # Appelle la fonction de téléchargent des images
        images_download(image_folder)

        # Appelle la fonction d'écriture des fichiers csv avec les données collectées
        write_data_csv(csv_folder, category_csv_name)

        # Réinitialise chaque liste avant la création du fichier csv suivant afin de s'assurer que chaque fichier csv contiennent uniquement les données de sa catégorie
        product_link_list.clear()
        product_title_list.clear()
        product_page_url_list.clear()
        universal_product_code_list.clear()
        price_including_tax_list.clear()
        price_excluding_tax_list.clear()
        number_available_list.clear()
        product_description_list.clear()
        category_list.clear()
        review_rating_list.clear()
        image_url_list.clear()

    # Message indiquant à l'utilisateur et en fin de programme le résultat de son exécution
    if len(count) != 1000:
        print("Erreur : des produits sont manquants")
    else :
        print("Opération réussie. Vous pouvez quitter le programme")

    # Fin du timer, résultat indiqué en minutes
    end_time = time.time()
    execution_time = (end_time - start_time) / 60

    print("Temps d'exécution du programme : ", execution_time, "minutes")

# Résultat de la gestion des erreurs s'il y'en a eu
except requests.exceptions.ConnectionError:
    print("Erreur de connexion. Quittez le programme, vérifiez votre connexion réseau et relancez le programme")

except requests.exceptions.Timeout:
    print("La requête a expiré. Veuillez quitter le programme et réessayer plus tard.")

except requests.exceptions.RequestException as e:
    print("Une erreur s'est produite lors de la requête HTTP :", e)

except Exception as e:
    print("Une erreur inattendue s'est produite :", e)
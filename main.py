import requests
import time
from utils import Site, Category, CSVWriter, ImageDownloader


SESSION = requests.Session()
URL = "https://books.toscrape.com/index.html"

# Commence un timer au début de l'exécution du programme
start_time = time.time()

# Lien du site cible (BooktoScrappe)
target = Site(URL)

# Recherche l'ensemble des catégories
category_urls = target.find_category_urls()

for url in category_urls:
    """
    Pour chaque catégorie, recherche l'ensemble des pages
    Pour chaque page, recherche l'ensemble des livres
    Pour chaque livre, collecte l'ensemble des données

    Exporte les données dans un format csv dans un dossier dédié

    Télécharge les images de chaque livre
    """
    category = Category(url)
    category_name = url.split('/')[-2].split('_')[0]
    pages = category.find_all_pages()
    books = category.find_all_books()
    data = category.collect_all_data()

    csv_writer = CSVWriter(category_name, data)
    csv_writer.write_csv_files()

    image = ImageDownloader(category_name, data)
    image.download_image()

    print(f"{category_name} : Done")

end_time = time.time()
elapsed_time = end_time - start_time

print("Temps d'exécution :", elapsed_time, "secondes")

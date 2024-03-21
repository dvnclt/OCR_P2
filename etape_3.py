# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from utils import collect_product_urls, collect_product_data, write_data_csv
from utils import product_link_list

category_link_list = []

# Obtention du contenu de la page
reponse = requests.get("https://books.toscrape.com/catalogue/page-1.html")

# Analyse de la page html avec BeautifulSoup
soup = BeautifulSoup(reponse.content, "html.parser")

# Recherche de l'url de chaque catégorie
category_link = soup.find("ul", class_="nav nav-list").find("ul").find_all("a", href=True)

for category_item in category_link:
    full_category_link = "https://books.toscrape.com/catalogue/" + category_item['href']
    category_link_list.append(full_category_link)
    collect_product_urls(full_category_link)


for product_item in product_link_list:
    collect_product_data(product_item)

write_data_csv()
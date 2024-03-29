import requests
from bs4 import BeautifulSoup
import os
import time
from utils import collect_product_urls, collect_product_data, write_data_csv, images_download
from utils import product_link_list, product_title_list, product_page_url_list, universal_product_code_list, price_including_tax_list, price_excluding_tax_list, number_available_list, product_description_list, category_list, review_rating_list, image_url_list
from utils import count

start_time = time.time()

category_link_list = []

csv_folder = "csv_directory"
os.makedirs(csv_folder, exist_ok=True)
image_folder = "images_directory"
os.makedirs(image_folder, exist_ok=True)

response = requests.get("https://books.toscrape.com/catalogue/page-1.html")
soup = BeautifulSoup(response.content, "html.parser")
category_link = soup.find("ul", class_="nav nav-list").find("ul").find_all("a", href=True)

for category_item in category_link:
    full_category_link = "https://books.toscrape.com/catalogue/" + category_item['href']
    category_link_list.append(full_category_link)
    category_csv_name = full_category_link.split('/')[-2].split('_')[0]
    collect_product_urls(full_category_link)

    for product_item in product_link_list:
        collect_product_data(product_item)

    images_download(image_folder)

    write_data_csv(csv_folder, category_csv_name)

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

if len(count) != 1000:
    print("Erreur : des produits sont manquants")
else :
    print("Opération réussie. Vous pouvez quitter le programme")

end_time = time.time()
execution_time = (end_time - start_time) / 60

print("Temps d'exécution du programme : ", execution_time, "minutes")
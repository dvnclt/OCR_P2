# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
import csv
import os
import re

product_link_list = []
product_title_list = []
product_page_url_list = []
universal_product_code_list = []
price_including_tax_list = []
price_excluding_tax_list = []
number_available_list = []
product_description_list = []
category_list = []
review_rating_list = []
image_url_list = []
count = []


def collect_product_urls(full_category_link):

    category_page = [full_category_link]
    category_name = full_category_link.split('/')[-2].split('_')[0].capitalize()
    total_product_link_by_category = 0
  
    while category_page:
        current_page = category_page.pop(0)
        response = requests.get(current_page)
        soup = BeautifulSoup(response.content, "html.parser")
        product_link = soup.find_all("a", title = True)

        for product_item in product_link:
            full_product_link = product_item["href"].replace("../../../", "https://books.toscrape.com/catalogue/")
            product_link_list.append(full_product_link)
            count.append(full_product_link)
            total_product_link_by_category += 1

        next_page = soup.find("li", class_="next")
        if next_page:
            next_page_link = next_page.find("a")["href"]
            url_part = current_page.split("/")[-1]
            next_page_url = current_page.replace(url_part, next_page_link)
            category_page.append(next_page_url)

    print(f"Nombre de produits trouvés dans la catégorie {category_name}:", total_product_link_by_category)
    print("Nombre total de produits trouvés : ", len(count))

def collect_product_data(product_item):
    
    response = requests.get(product_item)

    soup = BeautifulSoup(response.content, "html.parser")

    product_title = soup.find("h1").string
    product_title_list.append(product_title)

    product_page_url = product_item
    product_page_url_list.append(product_page_url)

    universal_product_code = soup.find("td").string
    universal_product_code_list.append(universal_product_code)

    price_including_tax = soup.find("p", class_="price_color").string
    price_including_tax_list.append(price_including_tax)

    price_excluding_tax = soup.find('table', class_='table').find_all('td')[2].string
    price_excluding_tax_list.append(price_excluding_tax)

    number_available = soup.find("p", class_="instock availability").text.strip()
    number_available_list.append(number_available)

    product_description = soup.find("meta", attrs={"name": "description"}).get("content","").strip()
    product_description_list.append(product_description)

    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    category_list.append(category)

    rating = str(soup.find("div", class_="col-sm-6 product_main").find_all("p")[2])
    if "One" in rating:
        review_rating_list.append("1/5")
    elif "Two" in rating:
        review_rating_list.append("2/5")
    elif "Three" in rating:
        review_rating_list.append("3/5")
    elif "Four" in rating:
        review_rating_list.append("4/5")
    else :
        review_rating_list.append("5/5")

    image_url = "https://books.toscrape.com/" + soup.find("div", class_="item active").find("img")["src"]
    image_url_list.append(image_url.strip())

def write_data_csv(csv_folder, category_csv_name):
    csv_file_path = os.path.join(csv_folder, category_csv_name + ".csv")
    en_tete = ["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"]
    with open(csv_file_path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(en_tete)
        for i in range(len(product_title_list)):
            row = [product_title_list[i], product_page_url_list[i], universal_product_code_list[i], price_including_tax_list[i], price_excluding_tax_list[i], number_available_list[i], product_description_list[i], category_list[i], "'" + review_rating_list[i] + "'", image_url_list[i]]
            writer.writerow(row)


def images_download(image_folder):
    for image_url, title, category in zip(image_url_list, product_title_list, category_list):
        # Créer un dossier pour la catégorie si elle n'existe pas déjà
        category_folder = os.path.join(image_folder, category.lower().replace(" ", "_"))
        os.makedirs(category_folder, exist_ok=True)
        
        # Extraire le nom du fichier de l'URL de l'image
        image_filename = re.sub(r'\W+', '_', title) + ".jpg"
        image_path = os.path.join(category_folder, image_filename)
        
        # Télécharger et enregistrer l'image
        response = requests.get(image_url)
        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
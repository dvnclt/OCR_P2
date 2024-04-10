# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

# Lien de la page à scraper
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Obtention du contenu de la page depuis le module requests
response = requests.get(url)

# Analyse de la page html avec le module BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Fonction de recherche du titre du produit
def get_product_title(soup):
    product_title = soup.find("h1").string
    return product_title

# Fonction de recherche de la page du produit
def get_product_page_url (url):
    product_page_url = url
    return product_page_url

# Fonction de recherche UPC
def get_universal_product_code(soup):
    universal_product_code = soup.find("td").string
    return universal_product_code

# Fonction de recherche du Prix TTC
def get_product_price_including_tax(soup):
    product_price_including_tax = soup.find("table", class_="table table-striped").find_all("td")[3].string
    return product_price_including_tax

# Fonction de recherche du Prix HT
def get_product_price_excluding_tax(soup):
    product_price_excluding_tax = soup.find("table", class_="table table-striped").find_all('td')[2].string
    return product_price_excluding_tax

# Fonction de recherche du stock disponible
def get_product_number_available(soup):
    product_number_available = soup.find("p", class_="instock availability").text.strip()
    return product_number_available

# Fonction de recherche de la description du produit
def get_product_description(soup):
    product_description = soup.find("article", class_="product_page").find_all("p")[3].string
    return product_description

# Fonction de recherche du nom de la catégorie du produit
def get_product_category_name(soup):
    product_category_name = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    return product_category_name

# Recherche de la notation du produit
def get_product_review_rating(soup):
    product_review_rating = str(soup.find("p", class_="star-rating Three"))
    if "One" in product_review_rating:
        return ("1/5")
    elif "Two" in product_review_rating:
        return ("2/5")
    elif "Three" in product_review_rating:
        return ("3/5")
    elif "Four" in product_review_rating:
        return ("4/5")
    else :
        return ("5/5")


# Fonction de recherche de l'url de l'image du produit
def get_product_image_url (soup) :
    product_image_url = soup.find("div", class_="item active").find("img")["src"].replace("../../", "https://books.toscrape.com/")
    return product_image_url

# Fonction de recherche de l'ensemble des données pour un produit
def get_all_product_data (soup, url):
    product_title = get_product_title(soup)
    product_page_url = get_product_page_url(url)
    universal_product_code = get_universal_product_code(soup)
    product_price_including_tax = get_product_price_including_tax(soup)
    product_price_excluding_tax = get_product_price_excluding_tax(soup)
    product_number_available = get_product_number_available(soup)
    product_description = get_product_description(soup)
    product_category_name = get_product_category_name(soup)
    product_review_rating = get_product_review_rating(soup)
    product_image_url =get_product_image_url(soup)
    all_product_data = [product_title, product_page_url, universal_product_code, product_price_including_tax, product_price_excluding_tax, product_number_available, product_description, product_category_name, product_review_rating, product_image_url]
    return all_product_data

# Création et écriture des données extraites dans un fichier CSV
def write_data_in_csv_file(all_product_data):
    with open("etape_1.csv", "w") as etape_1_csv_file:
        writer = csv.writer(etape_1_csv_file, delimiter = ",")
        writer.writerow(["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"])
        writer.writerow(all_product_data)


start_time = time.time()

all_product_data = get_all_product_data(soup,url)

write_data_in_csv_file(all_product_data)

end_time = time.time()
execution_time = (end_time - start_time)

print("Temps d'exécution du programme : {:.6f} secondes".format(execution_time))
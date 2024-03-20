# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

category_products_links_list = []
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


# Lien de la page à scraper
url = "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html"

# Obtention du contenu de la page
reponse = requests.get(url)

# Analyse de la page html avec BeautifulSoup
soup = BeautifulSoup(reponse.content, "html.parser")

# Recherche de l'url de chaque produit del catégorie
category_products_links_base_url = "https://books.toscrape.com/catalogue/"
category_products_links = soup.find_all("a", title = True)

for element_product_link in category_products_links:
    href_product_link = element_product_link["href"]
    full_category_link = href_product_link.replace("../../../", category_products_links_base_url)
    category_products_links_list.append(full_category_link)

def data_collect():
    
    reponse = requests.get(category_links)

    soup = BeautifulSoup(reponse.content, "html.parser")

    product_title = soup.find("h1").string
    product_title_list.append(product_title)

    product_page_url = url
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

    star_class_name = "star-rating Three"
    review_rating = soup.find("p", class_=star_class_name)
    if "One" in star_class_name:
        review_rating_list.append("1/5")
    elif "Two" in star_class_name:
        review_rating_list.append("2/5")
    elif "Three" in star_class_name:
        review_rating_list.append("3/5")
    elif "Four" in star_class_name:
        review_rating_list.append("4/5")
    else :
        review_rating_list.append("5/5")

    image_base_url = "https://books.toscrape.com/"
    image_url = urljoin(image_base_url, soup.find("div", class_="item active").find("img")["src"])
    image_url_list.append(image_url.strip())

def data_csv():
        en_tete = ["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"]
        with open("etape_2.csv", "w") as etape_2_csv_file:
            writer = csv.writer(etape_2_csv_file, delimiter=",")
            writer.writerow(en_tete)
            for i in range(len(product_title_list)):
                row = [product_title_list[i], product_page_url_list[i], universal_product_code_list[i], price_including_tax_list[i], price_excluding_tax_list[i], number_available_list[i], product_description_list[i], category_list[i], review_rating_list[i], image_url_list[i]]
                writer.writerow(row)

for category_links in category_products_links_list:
    data_collect()
    data_csv()
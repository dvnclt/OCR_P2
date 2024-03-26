# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# Lien de la page à scraper
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Obtention du contenu de la page depuis le module requests
response = requests.get(url)
page = response.content

# Analyse de la page html avec le module BeautifulSoup
soup = BeautifulSoup(page, "html.parser")

# Recherche Title
product_title_list = []
product_title = soup.find("h1").string
product_title_list.append(product_title)

# Recherche Product page url
product_page_url_list = []
product_page_url = url
product_page_url_list.append(product_page_url)

# Recherche UPC
universal_product_code_list = []
universal_product_code = soup.find("td").string
universal_product_code_list.append(universal_product_code)

# Recherche Price Including Tax
price_including_tax_list = []
price_including_tax = soup.find("p", class_="price_color").string
price_including_tax_list.append(price_including_tax)

# Recherche Price Excluding Tax
price_excluding_tax_list = []
price_excluding_tax = soup.find('table', class_='table').find_all('td')[2].string
price_excluding_tax_list.append(price_excluding_tax)

# Recherche Number available
number_available_list = []
number_available = soup.find("p", class_="instock availability").text.strip()
number_available_list.append(number_available)

# Recherche Product description
product_description_list = []
product_description = soup.find("meta", attrs={"name": "description"}).get("content","").strip()
product_description_list.append(product_description)

# Recherche Category
category_list = []
category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
category_list.append(category)

# Recherche Review Rating
review_rating_list = []
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


# Recherche Lien image
image_url_list = []
image_base_url = "https://books.toscrape.com/"
image_url = urljoin(image_base_url, soup.find("div", class_="item active").find("img")["src"])
image_url_list.append(image_url.strip())

# Création et écriture des données extraites dans un fichier CSV
en_tete = ["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"]
with open("etape_1.csv", "w") as etape_1_csv_file:
    writer = csv.writer(etape_1_csv_file, delimiter=",")
    writer.writerow(en_tete)
    for element in zip (product_title_list, product_page_url_list, universal_product_code_list, price_including_tax_list, price_excluding_tax_list, number_available_list, product_description_list, category_list, review_rating_list, image_url_list):
        writer.writerow([product_title, product_page_url, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating_list, image_url])
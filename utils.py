# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

category_link_list = []
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
product_data_list = product_title_list, product_page_url_list, universal_product_code_list, price_including_tax_list, price_excluding_tax_list, number_available_list, product_description_list, category_list,review_rating_list, image_url_list

def collect_product_urls(full_category_link):

    reponse = requests.get(full_category_link)

    soup = BeautifulSoup(reponse.content, "html.parser")
    product_link = soup.find_all("a", title = True)

    print("Nombre de liens de produit trouvés dans la catégorie donnée:", len(product_link))

    for product_item in product_link:
        full_product_link = product_item["href"].replace("../../../", "https://books.toscrape.com/catalogue/")
        product_link_list.append(full_product_link)

    print("Nombre total de liens de produit ajoutés à la liste 'product_link_list'", len(product_link_list))

def collect_product_data(product_item):
    
    reponse = requests.get(product_item)

    soup = BeautifulSoup(reponse.content, "html.parser")

    product_title = soup.find("h1").string
    product_title_list.append(product_title)
    print("Nombre total de titres ajoutés à la liste", len(product_title_list))

    product_page_url = product_item
    product_page_url_list.append(product_page_url)
    print("Nombre total de liens produits ajoutés à la liste", len(product_page_url_list))

    universal_product_code = soup.find("td").string
    universal_product_code_list.append(universal_product_code)
    print("Nombre total d'UPC ajoutés à la liste", len(universal_product_code_list))

    price_including_tax = soup.find("p", class_="price_color").string
    price_including_tax_list.append(price_including_tax)
    print("Nombre total de price including tax ajoutés à la liste", len(price_including_tax_list))

    price_excluding_tax = soup.find('table', class_='table').find_all('td')[2].string
    price_excluding_tax_list.append(price_excluding_tax)
    print("Nombre total de price excluding tax à la liste", len(price_excluding_tax_list))

    number_available = soup.find("p", class_="instock availability").text.strip()
    number_available_list.append(number_available)
    print("Nombre total de number available ajoutés à la liste", len(number_available_list))

    product_description = soup.find("meta", attrs={"name": "description"}).get("content","").strip()
    product_description_list.append(product_description)
    print("Nombre total de descriptions ajoutées à la liste", len(product_description_list))

    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    category_list.append(category)
    print("Nombre total de catégories ajoutées à la liste", len(category_list))

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
    print("Nombre total de reviews ajoutées à la liste", len(review_rating_list))

    image_base_url = "https://books.toscrape.com/"
    image_url = urljoin(image_base_url, soup.find("div", class_="item active").find("img")["src"])
    image_url_list.append(image_url.strip())
    print("Nombre total de liens d'image ajoutés à la liste", len(image_url_list))

def write_data_csv():
    en_tete = ["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"]
    with open("etape_3.csv", "w") as etape_3_csv_file:
        writer = csv.writer(etape_3_csv_file, delimiter=",")
        writer.writerow(en_tete)
        for i in range(len(product_title_list)):
            row = [product_title_list[i], product_page_url_list[i], universal_product_code_list[i], price_including_tax_list[i], price_excluding_tax_list[i], number_available_list[i], product_description_list[i], category_list[i], "'" + review_rating_list[i] + "'", image_url_list[i]]
            writer.writerow(row)
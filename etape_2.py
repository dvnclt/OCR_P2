# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
import csv
import time

session = requests.Session()

# Lien de la page catégorie à scraper
url = "https://books.toscrape.com/catalogue/category/books/default_15/index.html"




def get_current_page_product_urls(soup):
    # Fonction de recherche des urls produits pour une catégorie donnée

    category_product_url_list = []

    soup_category_product_url = soup.find_all("a", title = True)

    for item in soup_category_product_url:
        href_category_product_url = item["href"]
        category_product_url = href_category_product_url.replace(
            "../../../","https://books.toscrape.com/catalogue/")
        category_product_url_list.append(category_product_url)

    return category_product_url_list


def get_next_page_url(soup):

    next_page_link = soup.find("li", class_="next")
    if next_page_link:
        href_next_page_url = next_page_link.find("a")["href"]
        next_page_url = url.replace("index.html", href_next_page_url)
        return next_page_url
    else :
        return None
    

def get_all_products_page_urls(url):

    category_products_urls_list = []
    
    while url:
        response = session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        category_products_urls_list.extend(get_current_page_product_urls(soup))
        url = get_next_page_url(soup)

    return category_products_urls_list


def get_all_product_data(url):
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_title = soup.find("h1").string
    
    product_page_url = url
    
    universal_product_code = soup.find("td").string
    
    product_price_including_tax = soup.find("table", class_="table table-striped").find_all("td")[3].string
    
    product_price_excluding_tax = soup.find("table", class_="table table-striped").find_all('td')[2].string
    
    product_number_available = soup.find("p", class_="instock availability").text.strip()
    
    product_description = soup.find("article", class_="product_page").find_all("p")[3].string
    
    product_category_name = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    
    product_review_rating = str(soup.find("div", class_="col-sm-6 product_main").find_all("p")[2])
    if "One" in product_review_rating:
        product_review_rating = "1/5"
    elif "Two" in product_review_rating:
        product_review_rating = "2/5"
    elif "Three" in product_review_rating:
        product_review_rating = "3/5"
    elif "Four" in product_review_rating:
        product_review_rating = "4/5"
    else:
        product_review_rating = "5/5"
    
    product_image_url = soup.find("div", class_="item active").find("img")["src"].replace("../../", "https://books.toscrape.com/")
    
    return [product_title, product_page_url, universal_product_code, product_price_including_tax, product_price_excluding_tax, product_number_available, product_description, product_category_name, product_review_rating, product_image_url]


def write_csv_file(category_products_urls_list):
    
    with open("etape_2.csv", "w") as etape_2_csv_file:
        writer = csv.writer(etape_2_csv_file, delimiter = ",")
        writer.writerow(["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"])

        for item in category_products_urls_list:
            product_data = get_all_product_data(item)
            writer.writerow(product_data)


start_time = time.time()

category_products_urls_list = get_all_products_page_urls(url)

write_csv_file(category_products_urls_list)

end_time = time.time()
execution_time = (end_time - start_time)

print("Temps d'exécution du programme : {:.2f} secondes".format(execution_time))
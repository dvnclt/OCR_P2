import requests
from bs4 import BeautifulSoup
import os
import csv
import re


session = requests.Session()



def get_all_page_urls(category_url):

    page_urls_list = []
    current_url = category_url

    while True:
        response = session.get(current_url)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération de {current_url}")
            break

        page_urls_list.append(current_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        next_page_link = soup.find('li', class_='next')
        if next_page_link:
            href_next_page_url = next_page_link.find("a")["href"]
            next_page_url = category_url.replace("index.html", href_next_page_url)
        else:
            break

        current_url = next_page_url

    return page_urls_list



def get_all_products_urls(page_urls_list):

    product_urls_list = []

    for page_url in page_urls_list:
        response = session.get(page_url)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération de {page_url}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        product_links_list = soup.find_all("a", title = True)
        for product_link in product_links_list:
            href_product_url = product_link["href"]
            product_url = href_product_url.replace(
            "../../../","https://books.toscrape.com/catalogue/")
            product_urls_list.append(product_url)

    return product_urls_list



def get_all_product_data(product_urls_list):

    all_product_data = []

    for product_url in product_urls_list:
        response = session.get(product_url)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération de {product_url}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        product_title = soup.find("h1").string
        product_page_url = product_url
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
        elif "Five" in product_review_rating:
            product_review_rating = "5/5"
        else:
            product_review_rating = "N/A"

        product_image_url = soup.find("div", class_="item active").find("img")["src"].replace("../../", "https://books.toscrape.com/")

        all_product_data.append([product_title, product_page_url, universal_product_code, product_price_including_tax, product_price_excluding_tax, product_number_available, product_description, product_category_name, product_review_rating, product_image_url])


    return all_product_data



def write_csv_files(product_urls_list, category_name):
        
    folder_name = "csv_directory"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    csv_file_path = os.path.join(folder_name, category_name + ".csv")
        
    with open(csv_file_path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"])
        
        for product_url in product_urls_list:
            product_data = get_all_product_data([product_url])
            for data in product_data:
                writer.writerow(data)



def get_images_jpg(category_name, product_data):

    main_folder = "images_directory"
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    category_folder = os.path.join(main_folder, category_name.replace(" ", "_"))
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    for data in product_data:
        image_url = data[-1]
        product_title = data[0]
        file_name = re.sub(r'\W+', '_', product_title)
        image_name = file_name + ".jpg"
        image_path = os.path.join(category_folder, image_name)

        response = session.get(image_url)
        with open(image_path, "wb") as image_file:
            image_file.write(response.content)

import requests
from bs4 import BeautifulSoup
import os
import csv
import re

SESSION = requests.Session()


class Site:
    # Recherche l'url de chaque catégorie du site
    def __init__(self, url):
        self.url = url
        self.urls_list = []

    def find_category_urls(self):
        response = SESSION.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        category_url = soup.find("ul", class_="nav nav-list").find("li").find_all("a", href=True)

        for url in category_url[1:]:
            category_url = "https://books.toscrape.com/" + url['href']
            self.urls_list.append(category_url)

        return self.urls_list


class Category():
    # Recherche l'url de chaque produit contenu dans une catégorie donnée
    def __init__(self, url):
        self.url = url
        self.page_list = []
        self.books_list = []
        self.book_data = []

    def find_all_pages(self):
        while True:
            response = SESSION.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            self.page_list.append(self.url)

            next_page = soup.find('li', class_='next')
            if next_page:
                target = next_page.find("a")["href"]
                url_parts = self.url.split('/')
                url_parts[-1] = target
                next_page_url = '/'.join(url_parts)
            else:
                break

            self.url = next_page_url

        return self.page_list

    def find_all_books(self):
        for url in self.page_list:
            response = SESSION.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            books_list = soup.find_all("a", title=True)

            for book in books_list:
                target = book["href"]
                book_url = target.replace("../../../", "https://books.toscrape.com/catalogue/")
                self.books_list.append(book_url)

        return self.books_list

    def collect_all_data(self):
        for url in self.books_list:
            book = Book(url)
            data = book.collect_book_data()
            self.book_data.append(data)

        return self.book_data


class Book:
    # Collecte et transforme les informations d'un produit donné
    def __init__(self, url):
        self.url = url

    def collect_book_data(self):
        response = SESSION.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("h1").string
        page_url = self.url
        universal_product_code = soup.find("td").string
        price_including_tax = soup.find("table", class_="table table-striped").find_all("td")[3].string
        price_excluding_tax = soup.find("table", class_="table table-striped").find_all('td')[2].string
        number_available = soup.find("p", class_="instock availability").text.strip()
        description = soup.find("article", class_="product_page").find_all("p")[3].string
        category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
        review_rating = str(soup.find("div", class_="col-sm-6 product_main").find_all("p")[2])
        if "One" in review_rating:
            review_rating = "1/5"
        elif "Two" in review_rating:
            review_rating = "2/5"
        elif "Three" in review_rating:
            review_rating = "3/5"
        elif "Four" in review_rating:
            review_rating = "4/5"
        elif "Five" in review_rating:
            review_rating = "5/5"
        else:
            review_rating = "N/A"
        image_url = soup.find("div", class_="item active").find("img")["src"].replace("../../", "https://books.toscrape.com/")

        return title, page_url, universal_product_code, price_including_tax, price_excluding_tax, number_available, description, category, review_rating, image_url


class CSVWriter:
    def __init__(self, category_name, book_data):
        self.category_name = category_name
        self.book_data = book_data

    def write_csv_files(self):
        #  Exporte les données extraites dans un fichier CSV
        folder_name = "csv_directory"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        csv_file_path = os.path.join(folder_name, self.category_name + ".csv")

        with open(csv_file_path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(["Title", "Product page URL", "UPC", "Price incl. Tax", "Price excl. Tax", "Number available", "Product Description", "Category", "Review Rating", "Product image url"])

            for data in self.book_data:
                writer.writerow(data)


class ImageDownloader:
    # Télécharge l'image d'un produit donné
    def __init__(self, category_name, book_data):
        self.category_name = category_name
        self.book_data = book_data

    def download_image(self):
        main_folder = "images_directory"
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        category_folder = os.path.join(main_folder, self.category_name.replace(" ", "_"))
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        for data in self.book_data:
            image_url = data[-1]
            product_title = data[0]
            file_name = re.sub(r'\W+', '_', product_title)
            image_name = file_name + ".jpg"
            image_path = os.path.join(category_folder, image_name)

            response = SESSION.get(image_url)
            with open(image_path, "wb") as image_file:
                image_file.write(response.content)

import requests
from bs4 import BeautifulSoup
import time
from utils import *

session = requests.Session()

url = "https://books.toscrape.com/index.html"

start_time = time.time()

try :
    response = session.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    category_urls_list = []

    category_link = soup.find("ul", class_="nav nav-list").find("li").find_all("a", href=True)


    for item in category_link[1:]:
        category_url = "https://books.toscrape.com/" + item['href']
        category_urls_list.append(category_url)

        category_name = category_url.split('/')[-2].split('_')[0]

        page_urls = get_all_page_urls(category_url)

        products_urls = get_all_products_urls(page_urls)
        
        write_csv_files(products_urls, category_name)

        get_images_jpg(category_name, get_all_product_data(products_urls))
        
        print(f"Catégorie {category_name} : done")

    end_time = time.time()
    execution_time = (end_time - start_time) / 60

    print("Programme terminé. Temps d'exécution du programme : {:.2f} minutes".format(execution_time))

except requests.exceptions.ConnectionError:
    print("Erreur de connexion. Quittez le programme, vérifiez votre connexion réseau et relancez le programme")

except requests.exceptions.Timeout:
    print("La requête a expiré. Veuillez quitter le programme et réessayer plus tard.")

except requests.exceptions.RequestException as e:
    print("Une erreur s'est produite lors de la requête HTTP :", e)

except Exception as e:
    print("Une erreur inattendue s'est produite :", e)
# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Lien de la page à scraper
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Obtention du contenu de la page
reponse = requests.get(url)
page = reponse.content

# Analyse de la page html avec BeautifulSoup
soup = BeautifulSoup(page, "html.parser")

# Recherche Title
product_title = soup.find("h1").string

print(f"Title : '{product_title}'")

# Recherche Product page url
product_page_url = url
print(f"Page product URL : '{product_page_url}'")

# Recherche UPC
universal_product_code = soup.find("td").string
print(f"Universal product code : '{universal_product_code}'")

# Recherche Price Including Tax
price_including_tax = soup.find("p", class_="price_color").string
print(f"Price including tax : '{price_including_tax}'")

# Recherche Price Excluding Tax
price_excluding_tax = soup.find('table', class_='table').find_all('td')[2].string
print(f"Price excluding tax : '{price_excluding_tax}'")

# Recherche Number available
number_available = soup.find("p", class_="instock availability").text.strip()
print(f"Number available : '{number_available}'")

# Recherche Product description
product_description = soup.find("meta", attrs={"name": "description"}).get("content","").strip()
print(f"Product Description : '{product_description}'")

# Recherche Category
category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
print(f"Category : '{category}'")

# Recherche Review Rating
star_class_name = "star-rating Three"
review_rating = soup.find("p", class_=star_class_name).text
if "One" in star_class_name:
    print("Review Rating : 1/5")
elif "Two" in star_class_name:
    print("Review Rating : 2/5")
elif "Three" in star_class_name:
    print("Review Rating : 3/5")
elif "Four" in star_class_name:
    print("Review Rating : 4/5")
else :
    print("Review Rating : 5/5")

# Recherche Lien image
base_url = "https://books.toscrape.com/"
image_url = urljoin(base_url, soup.find("div", class_="item active").find("img")["src"])
print(f"Lien de l'image : '{image_url}'")
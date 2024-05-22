import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

url = "https://www.amazon.in/s?k=smart+phones&crid=1329JZRJUDO0O&sprefix=smart+phones%2Caps%2C254&ref=nb_sb_noss_2"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

product_links = []
for link in soup.find_all('a', href=True):
    product_links.append(link['href'])

data = []
for link in product_links:
    product_url = urljoin(url, link)
    try:
        response = requests.get(product_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error requesting {product_url}: {e}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    name_element = soup.select_one('h1.product-title')
    if name_element is not None:
        name = name_element.get_text(strip=True)
    else:
        name = ''
    price_element = soup.select_one('p.product-price')
    if price_element is not None:
        price = price_element.get_text(strip=True)
    else:
        price = ''
    rating_element = soup.select_one('span.product-rating')
    if rating_element is not None:
        rating = rating_element.get_text(strip=True)
    else:
        rating = ''

    product_info = {
        'Name': name,
        'Price': price,
        'Rating': rating
    }
    data.append(product_info)

with open('products.csv', 'a', newline='') as csvfile:
    fieldnames = ['Name', 'Price', 'Rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if csvfile.tell() == 0:  # Only write header if file is empty
        writer.writeheader()

    for product in data:
        writer.writerow(product)
print('Data has been successfully scraped and saved to products.csv')

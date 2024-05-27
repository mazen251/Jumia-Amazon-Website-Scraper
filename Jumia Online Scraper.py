import csv
import requests
from bs4 import BeautifulSoup
import importlib
import urllib.parse

try:
    importlib.import_module('lxml')
except ImportError:
    import subprocess

    subprocess.call(['pip', 'install', 'lxml'])

def get_data(pageNo):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # URL-encode the search query
    encoded_query = urllib.parse.quote_plus(product)

    source = requests.get(f'https://www.jumia.com.eg/catalog/?q={encoded_query}&page={pageNo}', headers=headers).text

    soup = BeautifulSoup(source, 'lxml')

    containers = soup.find_all('article', class_='prd _fb col c-prd')

    for container in containers:
        product_info = []

        product_info.append(pageNo)

        name = container.find('h3', class_='name').text
        product_info.append(name)

        price = container.find('div', class_='prc').text
        product_info.append(price)

        img = container.find('div', class_='img-c').img['data-src']
        product_info.append(img)

        if container.find('div', class_='old'):
            old_price = container.find('div', class_='old').text
        else:
            old_price = "null"
        product_info.append(old_price)

        if container.find('div', class_='rev'):
            ratings = container.find('div', class_='rev').text
        else:
            ratings = "null"
        product_info.append(ratings)

        link = container.find('a', class_='core')['href']
        product_info.append("https://www.jumia.com.eg" + link)

        products.append(product_info)

products = []

product = input("Enter Product Name: ")
no_pages = None

while True:
    try:
        no_pages = int(input("Enter the number of pages to scrape: "))
        if no_pages > 0:
            break
        else:
            print("Please enter a positive number of pages.")
    except ValueError:
        print("Invalid input. Please enter a number.")

file_name = 'jumia.csv'

try:
    for i in range(1, no_pages + 1):
        get_data(i)
except Exception as e:
    print("An error occurred while scraping. Please select a smaller number of pages.")
    print(f"Error message: {str(e)}")

with open(file_name, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        ['Page Number', 'Product Name', 'Price after the sale', 'Price before the sale', 'Rating', 'Image', 'Link'])

    for r in range(len(products)):
        writer.writerow([products[r][0], products[r][1], products[r][2], products[r][4],
                         products[r][5], products[r][3], products[r][6]])

print("Scraping complete. Results saved to jumia.csv.")


max_price = float(input("Enter the maximum price you are willing to pay: "))

matching_items = []

with open(file_name, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        item_price = float(row[2].replace('EGP', '').replace(',', '').strip())
        if item_price <= max_price:
            matching_items.append((row[1], row[2], row[6]))

matching_file_name = 'matching_items.csv'

with open(matching_file_name, 'w', encoding='utf-8', newline='') as matching_file:
    writer = csv.writer(matching_file)
    writer.writerow(['Product Name', 'Price after the sale', 'Link'])

    for item in matching_items:
        writer.writerow([item[0], item[1], item[2]])

print("Matching items copied to matching_items.csv.")

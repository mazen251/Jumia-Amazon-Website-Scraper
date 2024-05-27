import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def download_amazon_html(product, num_pages):
    base_url = 'https://www.amazon.eg/s?k={}&language=en_AE&page={}'
    max_retries = 3

    options = Options()
    options.add_argument('--headless')
    service = Service('webdriver')
    driver = webdriver.Chrome(service=service, options=options)

    for page in range(1, num_pages + 1):
        url = base_url.format(product.replace(' ', '+'), page)
        retry_count = 0
        flag = False

        while not flag and retry_count < max_retries:
            try:
                driver.get(url)
                time.sleep(2)

                if driver.find_elements(By.CSS_SELECTOR, '.s-result-item'):
                    html_content = driver.page_source
                    save_html(html_content, f'page{page}.html')
                    print(f'Downloaded page {page} for {product}')
                    flag = True
                else:
                    print(f'Error downloading page {page} for {product}. Retrying...')
                    retry_count += 1
                    time.sleep(2)

            except Exception as e:
                print(f'Error downloading page {page} for {product}. Retrying...')
                retry_count += 1
                time.sleep(2)

        if not flag:
            print(f'Skipping page {page} for {product}')

    driver.quit()

def save_html(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)

product = input('Enter a product: ')
num_pages = int(input('Enter the number of pages to download: '))

download_amazon_html(product, num_pages)


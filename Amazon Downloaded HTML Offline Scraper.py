import json
import glob
from bs4 import BeautifulSoup

html_files = glob.glob('page*.html')

if not html_files:
    print("No HTML files found.")
else:
    for file_path in html_files:

        page_number = file_path.replace('page', '').replace('.html', '')

        with open(file_path, 'r', encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'html.parser')

        divs = soup.find_all('div', class_='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')

        data = []
        for div in divs:
            image = ''
            name = ''
            rating = ''
            price = ''
            old_price = ''

            img = div.find('img', class_='s-image')
            if img:
                image = img.get('src', '')
            else:
                image = 'N/A'

            span_title = div.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            if span_title:
                name = span_title.text.strip()
            else:
                name = 'N/A'

            span_rating = div.find('span', class_='a-icon-alt')
            if span_rating:
                rating = span_rating.text.strip()
            else:
                rating = 'N/A'

            span_price = div.find('span', class_='a-price-whole')
            if span_price:
                price = span_price.text.strip().rstrip('.')
            else:
                price = 'N/A'

            # Find all span elements with class="a-text-price"
            span_old_prices = div.find_all('span', class_='a-text-price')
            old_prices = []
            for span_old_price in span_old_prices:
                old_prices.append(span_old_price.text.strip())

            # Select the first old price or set it as "N/A" if none found
            if old_prices:
                old_price = old_prices[0]
            else:
                old_price = 'N/A'

            # Remove non-breaking spaces and trailing dot from old price
            old_price = old_price.replace('\u00a0', '').rstrip('.')

            data.append({
                'Image': image.strip(),
                'name': name.strip(),
                'rating': rating.strip(),
                'price': price.strip(),
                'old_price': old_price.strip(),
                'page_number': page_number.strip()
            })

        output_file = f"data_{file_path}.json"
        with open(output_file, 'w') as file:
            json.dump(data, file)

    print("Processing finished.")

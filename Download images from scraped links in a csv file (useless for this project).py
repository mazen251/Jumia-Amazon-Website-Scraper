import os
import requests
from urllib.parse import urlparse

if not os.path.exists("images"):
    os.makedirs("images")

with open("F-16.csv", "r") as file:
    lines = file.readlines()

for index, line in enumerate(lines, start=1):
    image_url = line.strip()

    if not image_url or not image_url.startswith('http'):
        print(f"Skipped line {index}: Invalid URL")
        continue

    try:
        image_name = f"image_{index}.jpg"

        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        image_path = os.path.join("images", image_name)
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Downloaded image {index}: {image_name}")
    except Exception as e:
        print(f"Error downloading image {index}: {str(e)}")

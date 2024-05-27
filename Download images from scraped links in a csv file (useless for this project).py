import os
import requests
from urllib.parse import urlparse

# Create a folder named "images" if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Open the CSV file and read the URLs
with open("F-16.csv", "r") as file:
    lines = file.readlines()

# Iterate over each line in the CSV file
for index, line in enumerate(lines, start=1):
    # Remove leading/trailing whitespace and newline characters
    image_url = line.strip()

    if not image_url or not image_url.startswith('http'):
        print(f"Skipped line {index}: Invalid URL")
        continue

    try:
        # Generate a sequential image name based on the index
        image_name = f"image_{index}.jpg"

        # Send a GET request to download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Save the image in the "images" folder
        image_path = os.path.join("images", image_name)
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Downloaded image {index}: {image_name}")
    except Exception as e:
        print(f"Error downloading image {index}: {str(e)}")

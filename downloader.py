# 3rd party libraries
import requests
from PIL import Image
from tqdm import tqdm

# standard libraries
from io import BytesIO
import os
import time

# local libraries
from utils import load_json

SCRAPER_CONFIG = "data/scraper_config.json"


def download_images(urls: list[str], folder: str) -> None:
    """Make a GET request and save .jpeg to disk

    Args:
        urls (list[str]): list of images's url
        folder (str): destination
    """
    for i, url in tqdm(enumerate(urls, 1)):

        response = requests.get(url=url)
        img = Image.open(BytesIO(response.content))
        if img.mode != 'RGB':
            img = img.convert('RGB')

        destination = folder+f'/img_{i}.jpeg'
        img.save(destination)

        time.sleep(0.5)


def main():

    scraper_config = load_json(filename=SCRAPER_CONFIG)

    for b_style in scraper_config['bonsai_styles']:

        folder = f'data/Bonsai_dataset/{b_style}'

        if os.path.exists(path=folder):
            print(folder, 'already exists')
        else:
            os.mkdir(path=folder)

        paths_file = f'data/Bonsai_urls/{b_style}_paths.json'
        images_paths = load_json(filename=paths_file)
        print(b_style.upper())
        download_images(urls=images_paths, folder=folder)


if __name__ == "__main__":
    main()

# standard libraries
import asyncio
from pathlib import Path

# local libraries
from scraper import scraper
from downloader import downloader

IMAGES_URLS_FOLDER = Path('data/Images_urls')
SCRAPER_CONFIG = 'data/scraper_config.json'
IMAGES_FOLDER = Path('data/Images')

def main():
    scraper(config=SCRAPER_CONFIG)
    asyncio.run(downloader(config=SCRAPER_CONFIG,
               images_folder=IMAGES_FOLDER,
               images_urls_folder=IMAGES_URLS_FOLDER))
    
    
if __name__ == '__main__':
    main()
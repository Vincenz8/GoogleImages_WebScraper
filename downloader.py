# 3rd party libraries
import requests
from PIL import Image

# standard libraries
from io import BytesIO
import os

# local libraries
from utils import load_config

SCRAPER_CONFIG = "data/scraper_config.json"


def main():
    
    scraper_config = load_config(filename=SCRAPER_CONFIG)
    
    url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSunq993IxkGtcE22VAdH3fHJcj51IKVVvWTw&usqp=CAU'
    response = requests.get(url=url)
    img = Image.open(BytesIO(response.content))
    img.save("img.jpeg")
    
if __name__ == "__main__":
    main()
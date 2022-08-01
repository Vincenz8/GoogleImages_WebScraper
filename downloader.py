# 3rd party libraries
from httpx import AsyncClient
import httpx
from PIL import Image

# standard libraries
from io import BytesIO
from pathlib import Path
import asyncio
import os

# local libraries
from utils import load_json

async def get_img(url: str, client:AsyncClient, destination: str) -> None:
    """Make a GET request for an image and save to disk in JPEG format

    Args:
        url (str): image's url
        client (_type_): AsyncClient from httpx library
        destination (str): filepath

    """
    resp = await client.get(url)

    with Image.open(BytesIO(resp.content)) as img:
        if img.mode != 'RGB':
            return img.convert('RGB')
        img.save(fp=destination)


async def downloader(config:str, images_folder:Path, images_urls_folder:Path):
    s_config = load_json(filename=config)
    for name in s_config['images_names']:
        
        # creating folder for each category
        category_folder = images_folder.joinpath(name)
        if not category_folder.exists():
            os.mkdir(category_folder)

        urls = images_urls_folder.joinpath(f'{name}_urls.json')
        urls = load_json(filename=urls)
        async with AsyncClient() as client:
            tasks = []
            for i, url in enumerate(urls):
                img_destination = images_folder.joinpath(f'{name}/img_{i}.jpeg')
                tasks.append(asyncio.ensure_future(get_img(url=url, 
                                                           client=client, 
                                                           destination=img_destination)))

            await asyncio.gather(*tasks)

    

# 3rd party libraries
from httpx import AsyncClient
import httpx
from PIL import Image
from tqdm import tqdm

# standard libraries
from io import BytesIO
from pathlib import Path
import asyncio


# local libraries
from utils import load_json

BONSAI_URLS = Path("data/Bonsai_urls")


async def get_img(url: str, client):

    resp = await client.get(url)

    img = Image.open(BytesIO(resp.content))
    img.load()

    if img.mode != 'RGB':
        return img.convert('RGB')

    return img


async def main_test():
    
    # raccogliere tutti i link assieme poi svolgere l'asinc di conseguenza devo matchare fino ad un tot in una cartella
    async with AsyncClient() as client:

        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_img(url, client)))

        images = await asyncio.gather(*tasks)


if __name__ == '__main__':

    asyncio.run(main_test())

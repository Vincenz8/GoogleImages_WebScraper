# 3rd party libraries
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tqdm import tqdm

# standard libraries
import time

# local libraries
from utils import load_json, to_json


def fetch_urls(limit: int,
                driver: Chrome,
                driver_wait: WebDriverWait,
                thumb_class: str,
                img_class: str) -> list[str]:
    """Fetch images from Google page

    Args:
        limit (int): number of images to fetch
        driver (Chrome): Google Chrome web driver
        driver_wait (WebDriverWait): Webdriver wait object
        thumb_class (str): HTML CLASS of thumbnails displayed in the Google page
        img_class (str): HTML CLASS of actual images after clicking on thumbnails

    Returns:
        list[str]: set of urls fetched
    """
    start_thumb = 0
    fetched_urls = 0
    img_urls = set()

    while fetched_urls < limit:

        # getting all thumbnails
        thumbnails = driver.find_elements(by='class name', value=thumb_class)

        for thumbnail in tqdm(thumbnails[start_thumb:]):

            if fetched_urls >= limit:
                break

            else:

                try:
                    driver_wait.until(ec.element_to_be_clickable(
                        thumbnail)).click()  # getting full size image

                except Exception as e:
                    print('Img error, skipping to the next one')
                    continue

                img = driver.find_element(by='class name', value=img_class)
                img_url = img.get_attribute(name='src')

                if img_url.startswith('https'):
                    img_urls.add(img_url)
                    fetched_urls += 1

                time.sleep(1)

        # check if all urls were fetched, if not scroll windows
        if fetched_urls >= limit:
            print(f'All urls fetched!')
            break
        else:
            start_thumb = len(thumbnails)
            n_img_left = limit - fetched_urls
            print(f'{n_img_left} urls left')
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")

    return list(img_urls)


def scraper(config:str):
    """Save images's urls to Json file for each type of images contained in the configuration file

    Args:
        config (str): configuration filepath
    """
    scraper_config = load_json(filename=config)
    
    chrome_driver = Service(executable_path="data/chromedriver")
    driver = webdriver.Chrome(service=chrome_driver)
    wait_time = WebDriverWait(driver, 20)
    driver.maximize_window()
    
    for name in scraper_config['images_names']:

        url = f"https://www.google.com/search?q={name}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiHnMa83YT5AhWCXvEDHTM-AaoQ_AUoAXoECAEQAw&biw=1366&bih=668"
        driver.get(url=url)

        # wait for clicking reject cookie button
        if name == scraper_config['images_names'][0]:
            reject_cookie_button = (
                By.XPATH, scraper_config['cookie_button_xpath'])
            wait_time.until(ec.element_to_be_clickable(
                mark=reject_cookie_button)).click()

        # fetching all urls
        func_param = {'limit': scraper_config['n_images'],
                      'thumb_class': scraper_config['thumb_class'],
                      'img_class': scraper_config['img_class'],
                      'driver': driver,
                      'driver_wait': wait_time
                      }
        img_urls = fetch_urls(**func_param)

        urls = f'data/Images_urls/{name}_urls.json'
        to_json(obj=img_urls, filename=urls)

    driver.quit()



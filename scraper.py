# 3rd party libraries
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


SCRAPER_CONFIG = "data/scraper_config.json"

def fetching_urls(thumbnails:list[WebElement], limit: int) -> list[str]:
    # TODO
    ...

def main():
    chrome_driver = Service(executable_path="data/chromedriver")
    driver = webdriver.Chrome(service=chrome_driver)
    scraper_config = load_json(filename=SCRAPER_CONFIG)
    driver.maximize_window()
    wait_time = WebDriverWait(driver, 20)
    
    for b_style in scraper_config["bonsai_styles"]:
        
        url = f"https://www.google.com/search?q={b_style}+bonsai&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiHnMa83YT5AhWCXvEDHTM-AaoQ_AUoAXoECAEQAw&biw=1366&bih=668"
        driver.get(url=url)
        
        # wait for clicking reject cookie button
        if b_style == scraper_config['bonsai_styles'][0]:
            reject_cookie_button = (By.XPATH, scraper_config['cookie_button_xpath'])
            wait_time.until(ec.element_to_be_clickable(mark=reject_cookie_button)).click()
        
        start_thumb = 0
        fetched_images = 0
        img_paths = set()
        
        print(b_style.upper())
        while fetched_images < scraper_config['n_images']:
            
            # getting all thumbnails
            thumbnails = driver.find_elements(by='class name', value=scraper_config['thumb_class'])
            
            for thumbnail in tqdm(thumbnails[start_thumb:]):
                
                if fetched_images >= scraper_config['n_images']:
                    print(f'All {scraper_config["n_images"]} urls fetched!')
                    break  
                
                else:
                
                    try:
                        wait_time.until(ec.element_to_be_clickable(thumbnail)).click() # getting full size image
                        
                    except Exception as e:
                        print('Img error, skipping to the next one')
                        continue
                    
                    img = driver.find_element(by='class name', value=scraper_config["img_class"])
                    img_path = img.get_attribute(name='src')
                    
                    if img_path.startswith('https'):
                        img_paths.add(img_path)
                        fetched_images += 1
                        
                    time.sleep(1)
                
            # check if all urls were fetched, if not scroll windows  
            if fetched_images >= scraper_config['n_images']:
                print(f'All {scraper_config["n_images"]} {b_style} urls fetched!')
                break    
            else:
                start_thumb = len(thumbnails)
                n_img_left = scraper_config['n_images'] - fetched_images
                print(f'{n_img_left} urls left')
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            
                  
        paths = f'data/Bonsai_urls/{b_style}_paths.json'
        to_json(obj=list(img_paths), filename=paths)
        
    print('All urls fetched')        
    driver.quit()
    
    
if __name__ == '__main__':
    main()

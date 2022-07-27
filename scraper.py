# 3rd party libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from tqdm import tqdm

# standard libraries
import time
import pprint as pp

# local libraries
from utils import load_json, to_json


SCRAPER_CONFIG = "data/scraper_config.json"


def main():
    chrome_driver = Service(executable_path="data/chromedriver")
    driver = webdriver.Chrome(service=chrome_driver)
    scraper_config = load_json(filename=SCRAPER_CONFIG)
    driver.maximize_window()
    
    for b_style in scraper_config["bonsai_styles"]:
        
        url = f"https://www.google.com/search?q={b_style}+bonsai&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiHnMa83YT5AhWCXvEDHTM-AaoQ_AUoAXoECAEQAw&biw=1366&bih=668"
        driver.get(url=url)
        
        # wait for clicking reject cookie button
        if b_style!=scraper_config['bonsai_styles'][0]:
            xpath_button = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button/span'
            reject_cookie_button = (By.XPATH, xpath_button)
            wait_time = WebDriverWait(driver, 20)
            wait_time.until(ec.element_to_be_clickable(mark=reject_cookie_button)).click()
        
        start_thumb = 0
        fetched_images = 0
        img_paths = set()
        
        print(b_style.upper())
        while fetched_images < scraper_config['n_images']:
            
            thumbnails = driver.find_elements(by='class name', value=scraper_config['thumb_class'])
            
            for thumbnail in tqdm(thumbnails[start_thumb:]):
                
                try:
                    wait_time.until(ec.element_to_be_clickable(thumbnail)).click()
                    
                except :
                    print('errore img')
                    continue
                # thumbnail.click()
                img = driver.find_element(by='class name', value=scraper_config["img_class"])
                img_path = img.get_attribute(name='src')
                
                if img_path.startswith('https'):
                    img_paths.add(img_path)
                    
                time.sleep(1)
                
            fetched_images = len(img_paths) 
              
            if fetched_images >= scraper_config['n_images']:
                print(f'All {scraper_config["n_images"]} urls fetched!')
                break    
            else:
                start_thumb = len(thumbnails)
                n_img_left = scraper_config['n_images'] - fetched_images
                print(f'{n_img_left} urls left')
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            
                  
        paths = f'data/Bonsai_urls/{b_style}_paths.json'
        to_json(obj=list(img_paths), filename=paths)
            
    driver.quit()
    
    
if __name__ == '__main__':
    main()

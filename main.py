# 3rd party libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# standard libraries
import time
import pprint as pp

# local libraries
from utils import load_config


SCRAPER_CONFIG = "data/scraper_config.json"


def main():
    chrome_driver = Service(executable_path="data/chromedriver")
    driver = webdriver.Chrome(service=chrome_driver)
    scraper_config = load_config(filename=SCRAPER_CONFIG)
    driver.maximize_window()
    
    for b_style in scraper_config["bonsai_styles"]:
        url = f"https://www.google.com/search?q={b_style}+bonsai&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiHnMa83YT5AhWCXvEDHTM-AaoQ_AUoAXoECAEQAw&biw=1366&bih=668"
        driver.get(url=url)
        images = driver.find_elements(by="class name", value='rg_i.Q4LuWd')
        img_paths = set()
        
        for img in images:
            img.click()
            # almost working
            # img_path = driver.find_element(by="css selector", value='img.n3VNCb.KAlRDb').get_attribute(name='src')
            # img_paths.add(img_path)
            time.sleep(1) 
        pp.pprint(img_paths)   
            
    driver.quit()
    
    
if __name__ == '__main__':
    main()

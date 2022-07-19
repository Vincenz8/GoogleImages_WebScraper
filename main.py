# 3rd party libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# local libraries
from utils import load_config

SCRAPER_CONFIG = "data/scraper_config.json"


def main():
    chrome_driver = Service(executable_path="data/chromedriver")
    driver = webdriver.Chrome(service=chrome_driver)
    scraper_config = load_config(filename=SCRAPER_CONFIG)

    for b_style in scraper_config["bonsai_styles"]:
        url = f"https://www.google.com/search?q={b_style}+bonsai&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiHnMa83YT5AhWCXvEDHTM-AaoQ_AUoAXoECAEQAw&biw=1366&bih=668"
        driver.get(url=url)
         # agree cookies
        xpath_accept_button = '//*[@id="L2AGLb"]/div'
        driver.find_element(by="xpath", value=xpath_accept_button).click()
        driver.implicitly_wait(time_to_wait=50)
        break
    


if __name__ == '__main__':
    main()

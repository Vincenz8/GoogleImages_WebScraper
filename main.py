# 3rd party libraries
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# local libraries
from utils import load_config

SCRAPER_CONFIG = "data/scraper_config.json"


def main():
    gecko_driver = Service(executable_path="data/geckodriver")
    driver = webdriver.Firefox(service=gecko_driver)
    scraper_config = load_config(filename=SCRAPER_CONFIG)

    for b_style in scraper_config["bonsai_styles"]:
        driver.get(url=f"https://duckduckgo.com/?t=ffab&q={b_style}+bonsai&iax=images&ia=images")
        driver.implicitly_wait(time_to_wait=3)

    driver.quit()


if __name__ == '__main__':
    main()

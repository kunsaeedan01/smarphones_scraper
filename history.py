import requests
import lxml
import os
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

smartphones = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

url = "https://shop.kz/smartfony/"
chrome_driver_path='chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('accept-language=ru-RU')

driver = Chrome(executable_path=chrome_driver_path)
driver.get(url)

pages_num = driver.find_element_by_xpath('//*[@id="bx_eshop_wrap"]/div[1]/div/div/div/div/div[2]/div/div[2]/div[4]/div/ul/li[6]/a/span').text


for j in range(1, int(pages_num)):
    next = driver.find_element_by_class_name('bx-pag-next')
    next.click()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    names = soup.find_all(class_='bx_catalog_item_title_text')
    articuls = soup.find_all(class_='bx_catalog_item_XML_articul')
    memory = soup.find_all('span', attrs={"data-prop-title" : "386"})
    prices = soup.find_all(class_='bx-more-prices')
    for i in range(len(names)):
        try:
            price = prices[i].text.split('Цена в интернет-магазине', 1)[1].split('Цены указаны с учетом НДС')[0].replace(" ", "").replace('₸', "").split('Ценатоваранедели')[0]
        except IndexError:
            price = "Out of stock"
        dict = {
            "name": str(names[i].text.encode('utf-8').decode('utf-8')),
            "articul": str(articuls[i].text.replace("Артикул: ", "").replace('\t', '').replace('\n', '')),
            "price": str(price.replace('\n', '')),
            "memory-size": str(memory[i].find_next().text.encode('utf-8').decode('utf-8'))
        }
        smartphones.append(dict)



with open("smartphones.json", mode="a", encoding='ascii') as file:
    data = json.load(file)
    json.dump(smartphones, file, indent=4)
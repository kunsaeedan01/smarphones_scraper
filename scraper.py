import requests
import time
from urllib.parse import urljoin
import lxml
import json
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

url = 'https://shop.kz/smartfony'
smartphones = []
names = []
articuls = []
memory_sizes = []
prices = []
response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

scr_names = soup.find_all(class_='bx_catalog_item_title_text')
scr_articuls = soup.find_all(class_='bx_catalog_item_XML_articul')
scr_memories = soup.find_all('span', attrs={"data-prop-title" : "386"})
scr_prices = soup.find_all(class_='bx-more-prices')

for i in range(len(scr_names)):
    names.append(scr_names[i].text)
    articuls.append(scr_articuls[i].text.replace("Артикул: ", "").replace('\t', '').replace('\n', ''))
    memory_sizes.append(str(scr_memories[i].find_next().text))
    try :
        price = scr_prices[i].text.split('Цена в интернет-магазине', 1)[1].split('Цены указаны с учетом НДС')[0].replace(" ", "").replace('₸', "").split('Ценатоваранедели')[0]
    except IndexError :
        price = "Out of stock"
    price = str(price.replace('\n', ''))
    prices.append(price)


active = soup.find(class_='bx-pagination-container row')
next = soup.find(class_='bx-pag-next').find('a').get('href')
while next:
    url = 'https://shop.kz' + next
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    scr_names = soup.find_all(class_='bx_catalog_item_title_text')
    scr_articuls = soup.find_all(class_='bx_catalog_item_XML_articul')
    scr_memories = soup.find_all('span', attrs={"data-prop-title" : "386"})
    scr_prices = soup.find_all(class_='bx-more-prices')

    for i in range(len(scr_names)) :
        names.append(scr_names[i].text)
        articuls.append(scr_articuls[i].text.replace("Артикул: ", "").replace('\t', '').replace('\n', ''))
        memory_sizes.append(str(scr_memories[i].find_next().text))
        try :
            price = \
            scr_prices[i].text.split('Цена в интернет-магазине', 1)[1].split('Цены указаны с учетом НДС')[0].replace(
                " ", "").replace('₸', "").split('Ценатоваранедели')[0]
        except IndexError :
            price = "Out of stock"
        price = str(price.replace('\n', ''))
        prices.append(price)
    try:
        next = soup.find(class_='bx-pag-next').find('a').get('href')
    except AttributeError:
        break

for i in range(len(names)):
    dict = {
        "name": names[i],
        "articul": articuls[i],
        "price": prices[i],
        "memory-size": memory_sizes[i]
    }
    smartphones.append(dict)

with open("smartphones.json", mode="a") as file:
    json.dump(smartphones, file, indent=4)









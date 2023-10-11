import os
import requests
import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}


def get_review_links():
    for n in range(1, 6):
        if not os.path.isdir(f"mark{n}"):
            os.mkdir(f"mark{n}")
        for i in range(2, 52):
            f = open(f"mark{n}/mark{n}.txt", 'a', encoding='utf-8')
            response = requests.get(
                f"https://otzovik.com/reviews/online_fashion_shop_wildberries_ru/{str(i)}/?ratio={str(n)}",
                headers=headers, timeout=100)
            soup = BeautifulSoup(response.text, 'html.parser')
            if "С Вашего IP-адреса было много обращений к сайту Отзовик." in str(soup):
                print('Problems')
                time.sleep(3600)
            else:
                for link in soup.find_all('a', class_='review-title'):
                    print(f"{link.get('href')}")
                    f.write(f"https://otzovik.com{link.get('href')} ")
                    print(i)
            f.close()
            time.sleep(45)


def load_review():
    for n in range(1, 6):
        f = open(f"mark{n}/mark{n}.txt", "r", encoding='utf-8')
        if not os.path.isdir(f"dataset/{n}"):
            os.mkdir(f"dataset/{n}")
        links = f.read()
        links = links.split()
        f.close()
        for k in range(0, 1000):
            url = str(links[k])
            response = requests.get(url, headers=headers, timeout=100)
            soup = BeautifulSoup(response.text, 'html.parser')
            if "С Вашего IP-адреса было много обращений к сайту Отзовик." in str(soup):
                print('Problems')
                time.sleep(3600)
            else:
                print(f"Обработка:{links[k]} номер:{k}")
                a = soup.find('div', itemprop='description').text
                print(a)
                file = open(f"dataset/{n}/{k:04}.txt", "w", encoding='utf-8')
                file.write(str(a))
                file.close()
                time.sleep(45)


get_review_links()
load_review()

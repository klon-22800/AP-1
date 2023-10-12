import os
import time

import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def get_review_links(count: int) -> int:
    for n in range(1, 6):
        if not os.path.isdir(f"mark{n}"):
            os.mkdir(f"mark{n}")
        for i in range(2, count / 20 + 2):
            f = open(os.path.join(f"mark{n}", f"mark{n}.txt"), "a", encoding="utf-8")
            response = requests.get(
                f"https://otzovik.com/reviews/online_fashion_shop_wildberries_ru/{str(i)}/?ratio={str(n)}",
                headers=headers,
                timeout=100,
            )
            soup = BeautifulSoup(response.text, "html.parser")
            if "С Вашего IP-адреса было много обращений к сайту Отзовик." in str(soup):
                print("Problems")
                time.sleep(3600)
            else:
                for link in soup.find_all("a", class_="review-title"):
                    print(f"{link.get('href')}")
                    f.write(f"https://otzovik.com{link.get('href')}")
                    print(i)
            f.close()
            time.sleep(45)
    return count


def load_review(count: int, start: int = 0) -> None:
    for n in range(1, 6):
        f = open(os.path.join(f"mark{n}", f"mark{n}.txt"), "r", encoding="utf-8")
        if not os.path.isdir(os.path.join(f"dataset", f"{n}")):
            os.mkdir(os.path.join(f"dataset", f"{n}"))
        links = f.read()
        links = links.split()
        f.close()
        for k in range(start, count):
            url = str(links[k])
            response = requests.get(url, headers=headers, timeout=100)
            soup = BeautifulSoup(response.text, "html.parser")
            if "С Вашего IP-адреса было много обращений к сайту Отзовик." in str(soup):
                print("Problems")
                time.sleep(3600)
            else:
                print(f"Обработка:{links[k]} номер:{k}")
                a = soup.find("div", itemprop="description").text
                print(a)
                file = open(
                    os.path.join("dataset", f"{n}", f"{k:04}.txt"),
                    "w",
                    encoding="utf-8",
                )
                file.write(str(a))
                file.close()
                time.sleep(45)


def main() -> None:
    load_review(get_review_links(1000, 0))

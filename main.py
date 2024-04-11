from types import NoneType

from bs4 import BeautifulSoup
import requests
import datetime
import csv
from fake_useragent import UserAgent


def collect_data():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    page = 1
    product_counter = 0
    while True:
        url = f'https://www.mvideo.ru/promo/uletnaya-likvidaciya-skidki-do-50-mark211053242/f/discount=50-0/page={page}'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        products = soup.find_all('div', class_='fl-product-tile')
        product_numbers = int(soup.find('span', class_='fl-text c-plp-heading__count').text.strip())
        if product_numbers > product_counter:
            product_counter += len(products)
            page += 1
        else:
            break

        for product in products:
            name = product.find('a', class_='fl-product-tile-title__link sel-product-tile-title').text.strip()
            current_price = int(
                str(product.find('span', class_='fl-product-tile-price__current').text.strip()).replace(' ', '')[:-2])
            price = int(
                str(product.find('span', class_='fl-product-tile-price__sale').text.strip()).replace(' ', '')[:-2])
            rating = float(product.find('span', class_='fl-product-tile-rating__stars-value').text.strip())
            try:
                gift_points = int(
                    str(product.find('span', class_='u-color-red wrapper-text__rouble').text.strip()).replace(' ', '')[
                    1:])
            except AttributeError:
                gift_points = 0

            add_data(name=name, current_price=current_price, price=price, rating=rating, gift_points=gift_points)


def create_csv_table():
    d = datetime.datetime.now()
    with open(f'{d.day}-{d.month}-{d.year}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Name',
                'Current_price',
                'Price',
                'Rating',
                'Gift_points'
            )
        )


def add_data(name, current_price, price, rating, gift_points):
    d = datetime.datetime.now()
    with open(f'{d.day}-{d.month}-{d.year}.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                name,
                current_price,
                price,
                rating,
                gift_points
            )
        )


def main():
    create_csv_table()
    collect_data()


if __name__ == '__main__':
    main()

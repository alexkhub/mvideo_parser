# Mvideo parser
___
![PyPI - Version](https://img.shields.io/pypi/v/beautifulsoup4?label=bs4&labelColor=green)
![PyPI - Version](https://img.shields.io/pypi/v/requests?label=requests&labelColor=green)
![PyPI - Version](https://img.shields.io/pypi/v/lxml?label=lxml&labelColor=green)
![PyPI - Version](https://img.shields.io/pypi/v/fake-useragent?label=fake-useragent&labelColor=green)

**mvideo parser**- a program that collects data on products with a discount above 50% and records the data in a csv table.

## Install packages
```
pip install -r requirements.txt
```

### Page parsing 

```python 
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
```

### Create csv table 
```python 
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
```

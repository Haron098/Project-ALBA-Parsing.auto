from bs4 import BeautifulSoup as bs
import requests
import csv
BASE_URL = 'https://www.mashina.kg/search/all/'


def get_html(url):
    response = requests.get(url)
    return response.text


def get_soup(html):
    soup = bs(html, 'lxml')
    return soup


def get_data(soup):
    catalog = soup.find('div', class_='search-results-table')
    cars = catalog.find_all('div', class_='list-item list-label')
    for auto in cars:
        try:
            name = auto.find('h2', class_='name').text.strip()
        except AttributeError:
            name = ''
        try:
            price = auto.find('div', class_='block price').text.strip().split('\t\n')
            price = [i.strip() for i in price][:-1]
            price = '\t\n'.join([i for i in price if i])
        except AttributeError:
            price = ''
        try:
            images = auto.find_all('img', class_='lazy-image')
            images = '\t\n'.join([img.get('data-src') for img in images])
        except AttributeError:
            images = ''
        try:
            info = auto.find('div', class_='block info-wrapper item-info-wrapper').text.strip().split('\n')
            info = [i.strip() for i in info]
            info = '\t\n'.join([i for i in info if i])
        except AttributeError:
            info = ''
        write_csv({
            'name': name,
            'price': price,
            'info': info,
            'images': images,
        })


def write_csv(data):
    with open('auto.csv', 'a') as file:
        names = ['name', 'price', 'info', 'images']
        writer = csv.DictWriter(file, delimiter=',', fieldnames=names)
        writer.writerow(data)


def get_page():
    html = get_html(BASE_URL)
    soup = get_soup(html)
    pagination = soup.find('ul', class_='pagination').find_all('a', class_='page-link')
    pagination = [i.get('data-page') for i in pagination if i.get('data-page')]
    page = int(pagination[-1])
    return page
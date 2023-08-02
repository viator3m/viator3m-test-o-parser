from bs4 import BeautifulSoup
from django.conf import settings as conf
from django.db import transaction
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from api.v1.serializers.parser import ProductSerializer
from parser.models import Parsing
from parser_project.celery import app

arguments = [
    'headless',
    '--disable-blink-features=AutomationControlled',
    ('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'),
    '--no-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--start-maximized',
]


class Browser:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        for argument in arguments:
            self.options.add_argument(argument)
        self.options.binary_location = '/usr/bin/firefox'

    def get_page(self, page=conf.START_URL):
        browser = webdriver.Firefox(options=self.options)
        browser.get(page)
        wait = WebDriverWait(browser, timeout=5)
        try:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#ozonTagManagerApp')
            ))
        except TimeoutException:
            print('The page could not load')
        html = browser.page_source
        browser.quit()
        return BeautifulSoup(html, features='html.parser')

    def get_products(self, page=conf.START_URL):
        page = self.get_page(page)
        search_result = page.find(
            'div',
            {'class': 'widget-search-result-container'}
        )
        items = next(search_result.children)
        return [item for item in items.contents if item.name == 'div']

    def get_products_dict(self, amount, page=conf.START_URL):
        items = self.get_products(page)
        result = []
        for item in items:
            title = item.find('span', {'class': 'tsBody500Medium'}).text
            price = item.find('span', {'class': 'tsHeadline500Medium'}).text
            price = int(price.replace('\u2009', '').replace('₽', ''))
            link = 'https://ozon.ru' + item.find('a')['href']
            result.append({
                'title': title,
                'price': price,
                'link': link
            })
        return result[:amount]


@transaction.atomic
def save_to_db(data):
    parser = Parsing.objects.create()
    for item in data:
        item['parser'] = parser.id
    serializer = ProductSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@app.task(bind=True)
def parsing(self, amount):
    browser = Browser()
    items = browser.get_products_dict(amount=amount)
    if len(items) < amount:
        items += browser.get_products_dict(
            amount=amount - len(items),
            page=conf.START_URL + '?page=2'
        )
    save_to_db(items)
    return 'Parsing completed successfully'

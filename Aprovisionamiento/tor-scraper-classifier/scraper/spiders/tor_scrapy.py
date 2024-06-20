# -*- coding: utf-8 -*-
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# tor_scrapy.py - Lógica principal del scraper

import scrapy
from scrapy.exceptions import IgnoreRequest
from scraper.items import ScraperItem
from scraper.middlewares import FilterBannedWordsMiddleware

class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    allowed_domains = []
    custom_settings = {
        'BANNED_WORDS': []
    }

    def __init__(self, *args, **kwargs):
        super(ScraperSpider, self).__init__(*args, **kwargs)
        # Inicializar el middleware de palabras prohibidas
        self.banned_words_middleware = FilterBannedWordsMiddleware(self.load_banned_words())

    def load_banned_words(self):
        banned_words = []
        with open('/home/vagrant/Desktop/tor-scraper-classifier/config/banned_words.txt', 'r') as file:
            banned_words = [line.strip() for line in file]
        return banned_words

    def start_requests(self):
        # Leer las URLs desde el archivo harvest_results.txt
        with open('/home/vagrant/Desktop/tor-scraper-classifier/results/harvest_results.txt', 'r') as f:
            urls = [url.strip() for url in f.readlines()]

        # Iterar sobre las URLs y generar una solicitud para cada una
        for url in urls:
            full_url = f'http://{url}'
            self.logger.info(f'URL extraída del harvesting: {full_url}')
            yield scrapy.Request(url=full_url, callback=self.parse_item, meta={'url': full_url})

    def parse_item(self, response):
        url = response.meta['url']
        content = response.body.decode(response.encoding)
        self.logger.info(f'URL procesada: {url}')
        self.logger.debug(f'Contenido de la respuesta: {content}')

        # Verificar si la URL o el contenido contienen palabras prohibidas usando el middleware
        try:
            self.banned_words_middleware.process_response(None, response, self)
        except IgnoreRequest:
            self.logger.warning(f'Palabra prohibida encontrada en: {url}. Ignorando la solicitud...')
            return
        except TimeoutError:
            self.logger.warning(f'La solicitud a {response.url} ha fallado por timeout.')

        item = ScraperItem()
        item['url'] = url
        item['content'] = content

        yield item
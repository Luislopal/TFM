# -*- coding: utf-8 -*-
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# middlewares.py - Definir los middlewares necesarios para intervenir en las solicitudes

import logging
from scrapy.exceptions import IgnoreRequest

class FilterBannedWordsMiddleware:
    def __init__(self, banned_words):
        self.logger = logging.getLogger(__name__)
        self.banned_words = banned_words

    @classmethod
    def from_crawler(cls, crawler):
        banned_words = crawler.settings.getlist('BANNED_WORDS')
        return cls(banned_words)

    def process_response(self, request, response, spider):
        for word in self.banned_words:
            if word in response.text:
                self.logger.warning(f'Palabra prohibida encontrada: {word}')
                raise IgnoreRequest(f"Palabra prohibida encontrada: {word}")
        return response

class HaproxyRotatingProxyMiddleware:
    def process_request(self, request, spider):
        proxy_host = spider.settings.get('HTTP_PROXY')
        request.meta['proxy'] = f'{proxy_host}'
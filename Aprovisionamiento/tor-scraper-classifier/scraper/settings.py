# -*- coding: utf-8 -*-
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# settings.py - Archivo de configuración de Scrapy (proyecto scraper)

import re

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configuración de los middlewares utilizados
DOWNLOADER_MIDDLEWARES = {
    # Middleware del proxy
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 751,
    'scraper.middlewares.HaproxyRotatingProxyMiddleware': 752,
    # Middleware de las banned_words
    'scraper.middlewares.FilterBannedWordsMiddleware': 753,
}

# Proxy configuration
PROXY_ENABLED = True
PROXY_HOST = 'localhost'
PROXY_PORT = 3128

if PROXY_ENABLED:
    HTTP_PROXY = f'http://{PROXY_HOST}:{PROXY_PORT}'
    HTTPS_PROXY = f'http://{PROXY_HOST}:{PROXY_PORT}'

# Configuración para palabras prohibidas
BANNED_WORD_FILENAME = "/home/vagrant/Desktop/tor-scraper-classifier/config/banned_words.txt"
BANNED_WORDS = [line.strip() for line in open(BANNED_WORD_FILENAME) if line.strip() != ""]
BANNED_WORDS_REGEX_STR = ""
start = True

for word in BANNED_WORDS:
    if not start:
        BANNED_WORDS_REGEX_STR += '|'
    BANNED_WORDS_REGEX_STR += '\\b' + ('%s' % word) + '\\b'
    start = False

BANNED_WORDS_REGEX = re.compile(BANNED_WORDS_REGEX_STR, re.IGNORECASE)
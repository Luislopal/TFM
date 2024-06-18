# -*- coding: utf-8 -*-
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# items.py - Definición del modelo de los objetos scrapeados

import scrapy

class ScraperItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
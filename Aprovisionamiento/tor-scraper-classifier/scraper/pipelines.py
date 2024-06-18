# -*- coding: utf-8 -*-
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# pipelines.py - Procesar elementos (items) extraídos por el spider (scraper)

class ScraperPipeline(object):
    def process_item(self, item, spider):
        return item
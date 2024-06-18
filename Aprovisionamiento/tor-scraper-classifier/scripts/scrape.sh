#!/bin/bash
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# scrape.sh - Lógica necesaria para iniciar el proceso de scraping


sudo chmod -R +x /home/vagrant/Desktop/tor-scraper-classifier/results
sudo chmod -R +x /home/vagrant/Desktop/tor-scraper-classifier/config

cd /home/vagrant/Desktop/tor-scraper-classifier

# Ejecución del scraper configurado en el directorio ../scraper
scrapy crawl scraper -a test=no -o /home/vagrant/Desktop/tor-scraper-classifier/results/scraper_results.json
#!/bin/bash
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# misp_start.sh - Lógica necesaria para desplegar una instancia de MISP


echo -e "\e[1;30;107mInicio de los servicios Tor, Privoxy y Haproxy\e[0m"

#sudo systemctl start tor (Los privoxys van por las instancias creadas en start_tor)
sudo systemctl start privoxy1
sudo systemctl start privoxy2
sudo systemctl start haproxy

echo -e "\e[1;30;107mServicios iniciados correctamente\e[0m"

#############################################################################################################################################################################

echo "\nEstados de los servicios arrancados."
sudo systemctl status privoxy1
sleep 3
sudo systemctl status privoxy2
sleep 3
sudo systemctl status haproxy
sleep 3

echo -e "\e[1;30;107mInicio de las instacias de Tor\e[0m"
/home/vagrant/Desktop/tor-scraper-classifier/scripts/start_tor.sh

echo "\nComprobación correcto funcionamiento de los servicios Privoxy"
echo "curl con la opción --socks5-hostname por la direción http://localhost:9051"
curl --socks5-hostname http://localhost:9051 http://paavlaytlfsqyvkg3yqj7hflfg5jw2jdg2fgkza5ruf6lplwseeqtvyd.onion/
echo "curl con la opción --socks5-hostname por la direción http://localhost:9052"
curl --socks5-hostname http://localhost:9052 http://paavlaytlfsqyvkg3yqj7hflfg5jw2jdg2fgkza5ruf6lplwseeqtvyd.onion/
echo "curl con la opción --proxy por la direción http://localhost:3129"
curl --proxy http://localhost:3129 http://paavlaytlfsqyvkg3yqj7hflfg5jw2jdg2fgkza5ruf6lplwseeqtvyd.onion/
echo "curl con la opción --proxy por la direción http://localhost:3130"
curl --proxy http://localhost:3130 http://paavlaytlfsqyvkg3yqj7hflfg5jw2jdg2fgkza5ruf6lplwseeqtvyd.onion/

echo -e "\e[1;30;107mInicio de la recopilación de URLs .onion\e[0m"
sudo chmod -R +x /home/vagrant/Desktop/tor-scraper-classifier/scripts
/home/vagrant/Desktop/tor-scraper-classifier/scripts/harvest.sh
sleep 5

echo -e "\e[1;30;107mInicio del proceso de Scraping\e[0m"
sudo chmod -R +x /home/vagrant/Desktop/tor-scraper-classifier/scraper
/home/vagrant/Desktop/tor-scraper-classifier/scripts/scrape.sh

#############################################################################################################################################################################

echo -e "\e[1;30;107mDespliegue de una instancia de MISP (Docker)\e[0m" 
/home/vagrant/Desktop/tor-scraper-classifier/scripts/start_misp.sh

#############################################################################################################################################################################

# Adición del módulo IA para meter resultados categorizados a MISP (Necesario introducir API de MISP tras despliegue y ejecución manual)
echo -e "\e[1;30;107mInicio del proceso de Categorización\e[0m"
sudo chmod -R +x /home/vagrant/Desktop/tor-scraper-classifier/ia-classifier
/home/vagrant/Desktop/tor-scraper-classifier/scripts/start_classification.sh

echo -e "\e[1;30;107mIniciar MANUALMENTE el proceso de Inteligencia Artificial para cargar los resultados categorizados en MISP\e[0m"
echo -e "\e[1;30;107mSe ejecuta con el comando - sudo python3 /home/vagrant/Desktop/tor-scraper-classifier/ia-classifier/ollama_sinSR.py\e[0m"
echo -e "\e[1;30;107mTambién se puede ejecutar con el comando - sudo python3 /home/vagrant/Desktop/tor-scraper-classifier/ia-classifier/ollama_conSR.py\e[0m"


#!/bin/sh
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# start_tor.sh - Lógica necesaria para darrancar las instancias de TOR


base_socks_port=9050
base_http_port=3128 # Asignamos el 3128 del HAProxy, y se darán los valores sucesivos
base_control_port=8118

mkdir "/home/vagrant/Desktop/tor-scraper-classifier/config/data"
mkdir "/home/vagrant/Desktop/tor-scraper-classifier/config/var"

for i in 1 2
do
    socks_port=$((base_socks_port+i))
    control_port=$((base_control_port+i))
    http_port=$((base_http_port+i))
    if [ ! -d "/home/vagrant/Desktop/tor-scraper-classifier/config/data/tor$i" ]; then
        echo "Creating directory data/tor$i"
        mkdir "/home/vagrant/Desktop/tor-scraper-classifier/config/data/tor$i"
    fi
    echo "Running: tor --RunAsDaemon 1  --PidFile /home/vagrant/Desktop/tor-scraper-classifier/config/var/tor$i/tor$i.pid --SocksPort $socks_port --DataDirectory /home/vagrant/Desktop/tor-scraper-classifier/config/var/tor$1"
    echo "Control port: $control_port y http_port: $http_port y socks_port $socks_port"
    tor --RunAsDaemon 1  --PidFile /home/vagrant/Desktop/tor-scraper-classifier/config/var/tor$i/tor$i.pid --SocksPort $socks_port --DataDirectory /home/vagrant/Desktop/tor-scraper-classifier/config/var/tor$i
done





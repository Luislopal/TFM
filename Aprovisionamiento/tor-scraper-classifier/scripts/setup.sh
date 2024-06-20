#!/bin/bash
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# setup.sh - Lógica necesaria para realizar la configuración inicial del escenario


echo -e "\e[1;30;107mActualización de paquetes, sin interacción con el usuario\e[0m"
sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

echo -e "\e[1;30;107m****Instalación de las dependencias necesarias para el proyecto****\e[0m"

echo -e "\e[1;30;107m***Instalación de Python3 y pip***\e[0m"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-pip

echo -e "\e[1;30;107m***Instalación de Tor***\e[0m"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install tor torbrowser-launcher

echo -e "\e[1;30;107m***Instalación de Haproxy***\e[0m"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install haproxy

echo -e "\e[1;30;107m***Instalación de Privoxy***\e[0m"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install privoxy

echo -e "\e[1;30;107m***Instalación de Docker***\e[0m"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install docker.io

echo -e "\e[1;30;107m***Instalación dependencias de Scrapy***\e[0m"
pip install scrapy

sudo pip uninstall pyOpenSSL cryptography -y
pip install cryptography==36.0.0 pyOpenSSL==21.0.0

#############################################################################################################################################################################

echo -e "\e[1;30;107mConfiguración de ficheros básica necesaria para el funcionamiento del proyecto\e[0m"
echo -e "\e[1;30;107mConfiguración de la red Tor\e[0m"

# Abrir el archivo de configuración de Tor
TORRC_FILE="/etc/tor/torrc"
# Comprobar si el fichero y las líneas a añadir ya existen
if [ ! -f /etc/tor/torrc ]; then
  echo "Error: torrc not found"
  exit 1
fi
if grep -q "SOCKSPort 9050" /etc/tor/torrc && grep -q "DNSPort 53" /etc/tor/torrc; then
  echo "Ya existen las líneas, no se han realizado cambios"
  exit 0
fi

# Añadir las líneas en caso de que no existan
echo "SOCKSPort 9050" >> "$TORRC_FILE"
echo "DNSPort 53" >> "$TORRC_FILE"

echo -e "\e[1;30;107mLineas añadidas al fichero "$TORRC_FILE"\e[0m"
sleep 3

#############################################################################################################################################################################

echo -e "\e[1;30;107mConfiguración de HAProxy\e[0m"
HACONFIG_FILE="/etc/haproxy/haproxy.cfg"

echo -e "
frontend rotatingproxies
  log global
    bind 127.0.0.1:3128
    default_backend privoxy
backend privoxy
  log global
    server privoxy1 127.0.0.1:3129 check id 1
    server privoxy2 127.0.0.1:3130 check id 2
    balance roundrobin
" >> "$HACONFIG_FILE"

echo -e "\e[1;30;107mLineas añadidas al fichero "$HACONFIG_FILE"\e[0m"

#############################################################################################################################################################################

echo -e "\e[1;30;107mConfiguración de /etc/proxy\e[0m"

cat <<EOL > "/etc/proxy"
export TOR_PROXY_PORT=3129
export TOR_PROXY_HOST=localhost
export http_proxy=http://localhost:3129
export https_proxy=https://localhost:3129
export SOCKS_PROXY=localhost:9050
HIDDEN_SERVICE_PROXY_HOST=127.0.0.1
HIDDEN_SERVICE_PROXY_PORT=9090
EOL

echo -e "\e[1;30;107mConfiguración de /etc/proxy completada\e[0m"

#############################################################################################################################################################################

echo -e "\e[1;30;107mConfiguraciones de Privoxy\e[0m"

cd /etc/privoxy/
# Copiar los archivos de configuración originales
cp default.action default.action.orig
cp default.filter default.filter.orig
# Crear o modificar los archivos default.action y default.filter (dejarlos vacíos)
touch default.action
touch default.filter

sudo chmod -R +x /home/vagrant/Desktop/tor-scraper-classifier/scripts
/home/vagrant/Desktop/tor-scraper-classifier/scripts/privoxy_config.sh

echo -e "\e[1;30;107m                                                                  \e[0m"
echo -e "\e[1;30;107m *** LOS ERRORES PREVIOS SE SOLUCIONAN EN EL SIGUIENTE REINICIO ... ***\e[0m"
echo -e "\e[1;30;107m                                                                  \e[0m"
echo -e "\e[1;30;107mConfiguraciones de Privoxy completadas\e[0m" 
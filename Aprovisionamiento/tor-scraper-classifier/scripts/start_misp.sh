#!/bin/sh
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# start_misp.sh - Lógica necesaria para desplegar una instancia de MISP


echo -e "\e[1;30;107mDespliegue de una instancia de MISP (Docker)\e[0m"

echo -e "\e[1;30;107m***Instalación librería requests***\e[0m"
pip install requests

echo -e "\e[1;30;107m***Instalación librería pymisp***\e[0m"
pip install pymisp

sudo docker pull harvarditsecurity/misp
sudo mkdir -p /var/lib/docker/misp-db
sudo docker run --rm -v /var/lib/docker/misp-db:/var/lib/mysql harvarditsecurity/misp /init-db
sudo docker run -d -p 443:443 -p 80:80 -p 3306:3306 -p 6666:6666 -v /var/lib/docker/misp-db:/var/lib/mysql harvarditsecurity/misp

echo -e "\e[1;30;107mMISP instalado exitosamente\e[0m"

#Go to: https://localhost (or your "MISP_FQDN" setting)
#Login: admin@admin.test
#Password: admin
#Hay que cambiarla nada más arrancar
#Dentro de Event Actions > Automation (Arriba se puede ver la clave a sustituir en el código)


# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# Automatización de la configuración de MISP (Opción alternativa al despliegue Dockerizado)

# Instalar MariaDB y PHP
sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
sudo debconf-set-selections <<< 'mariadb-server-10.5 mysql-server/root_password password misp'
sudo debconf-set-selections <<< 'mariadb-server-10.5 mysql-server/root_password_again password misp'
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y php php-cli php-common php-gd php-curl php-mysql php-mbstring php-xml php-zip php-soap php-gmp php-intl apache2 apache2-dev libapache2-mod-php php-pear

# Iniciar MariaDB
sudo systemctl start mariadb

# Descargar y descomprimir MISP (master branch)
cd /home/vagrant/Desktop/tor-scraper-classifier/config/misp/
wget -q https://github.com/MISP/MISP/archive/refs/heads/master.tar.gz -O misp-master.tar.gz
tar -xvf misp-master.tar.gz

# Crear base de datos y actualizar config.php
PASSWORD="misp"
sudo mysql -u root -p"$PASSWORD" <<MYSQL_SCRIPT
CREATE DATABASE IF NOT EXISTS misp CHARACTER SET utf8 COLLATE utf8_bin;
GRANT ALL PRIVILEGES ON misp.* TO 'mispuser'@'localhost' IDENTIFIED BY '$PASSWORD';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

cd MISP-2.4/
sudo cp app/Config/bootstrap.default.php app/Config/bootstrap.php
sudo cp app/Config/database.default.php app/Config/database.php

sudo sed -i "s|'host' => 'localhost',|'host' => 'localhost',|g" app/Config/database.php
sudo sed -i "s|'login' => 'misp',|'login' => 'mispuser',|g" app/Config/database.php
sudo sed -i "s|'password' => '',|'password' => '$PASSWORD',|g" app/Config/database.php

#Probando si esto funciona para meter los headers en el script
sudo a2enmod headers

# Configurar Apache
sudo mkdir -p /etc/apache2/sites-available/
sudo cp debian/misp.apache2.conf /etc/apache2/sites-available/misp.conf
#No están funcionando estas lineas, si las pongo desde la mv si que van
#sudo sed -i "s|DocumentRoot /var/www/html|DocumentRoot /home/vagrant/Desktop/tor-scraper-classifier/config/misp/MISP-2.4/app/webroot|g" /etc/apache2/sites-available/misp.conf
#sudo sed -i "s|<Directory /var/www/html>|<Directory /home/vagrant/Desktop/tor-scraper-classifier/config/misp/MISP-2.4/app/webroot>|g" /etc/apache2/sites-available/misp.conf
# Reemplazar DocumentRoot y Directory en misp.conf de manera alternativa
sudo perl -0777 -i -pe 's|DocumentRoot /usr/share/misp/app/webroot|DocumentRoot /home/vagrant/Desktop/tor-scraper-classifier/config/misp/MISP-2.4/app/webroot|g; s|<Directory /usr/share/misp/app/webroot>|<Directory /home/vagrant/Desktop/tor-scraper-classifier/config/misp/MISP-2.4/app/webroot>|g' /etc/apache2/sites-available/misp.conf


# Actualizar la ruta del Include en misp.conf
sudo sed -i 's@Include debian/misp.apache2.conf@Include /etc/apache2/sites-available/misp.conf@' /etc/apache2/sites-available/misp.conf

# Habilitar el sitio y reiniciar Apache
sudo a2ensite misp.conf
sudo a2enmod rewrite
sudo systemctl restart apache2
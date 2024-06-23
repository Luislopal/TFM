Para iniciar sesión en la máquina las credenciales son las siguientes:

   Usuario: vagrant
   Contraseña: vagrant

# El proyecto está distribuido en 5 carpetas o directorios diferentes, dentro de Aprovisionamiento: 

    * config: Archivos necesarios en el resto de módulos
    * ia-classifier: Módulo de categorización, utilizando inteligencia artificial (IA) y el servicio Ollama junto al LLM llama-3
    * results: Resultados obtenidos durante la ejecución
    * scraper: Módulo de Scraping, con los ficheros necesarios para la ejecución de Scrapy
    * scripts: Scripts necesarios para la ejecución del proyecto

# Además, también cuenta con un Vagrantfile para el despliegue y aprovisionamiento de la máquina inicial (inicio del proyeco)

Para poder realizar el despliegue correcto del proyecto, será necesario tener instaladas las herramientas: Vagrant y VirtualBox.

Tras realizar la instalación de las herramientas anteriores, el proyecto completo se puede desplegar con los comandos: 
    
    * vagrant up: hasta el módulo de categorización.

Una vez finaliza el despliegue de MISP, tras haber extraído los enlaces ".onion" y su contenido, finaliza el proceso y es necesario realizar los siguientes pasos de forma manual:

  * Ir a la dirección URL: https://localhost desde el navegador deseado.
  * Iniciar sesión con las siguientes credenciales:
      Login: admin@admin.test
      Password: admin
  * Modificar la contraseña nada más iniciar sesión
  * Dentro de MISP, ir al Menú Event Actions > Automation (Arriba se puede ver la clave a sustituir en el código)
  * Sustituir la 'api_key' en la línea indicada dentro del fichero 'ollama.py'
    
Tras realizar estos pasos, el módulo de categorización podrá interactuar correctamente con MISP, añadiendo los resultados y sus criticidades. Para ello, hay que introducir uno de los comandos:

        * sudo python3 /home/vagrant/Desktop/tor-scraper-classifier/ia-classifier/ollama_conSR.py
        * sudo python3 /home/vagrant/Desktop/tor-scraper-classifier/ia-classifier/ollama_sinSR.py

Y se podrán visualizar en la interfaz web de MISP los resultados, según se vaya completando el proceso de categorización.

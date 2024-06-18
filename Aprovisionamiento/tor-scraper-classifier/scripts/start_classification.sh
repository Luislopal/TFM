#!/bin/sh
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# start_classification.sh - Lógica necesaria para arrancar el modelo LLM


# Descarga del servicio ollama
curl https://ollama.ai/install.sh | sh

# Inicio del servicio de Ollama en segundo plano
nohup ollama serve &
# Pausa para asegurarse de que el servicio Ollama tiene tiempo suficiente para iniciarse
sleep 5

# Inicio del servicio de Ollama con sudo
sudo service ollama start
# Pausa adicional para asegurarse de que el servicio se ha iniciado correctamente
sleep 3

# Inicio del modelo llama3
ollama run llama3

# Inicio de la ejecución del script para realizar consultas al modelo (podría modificarse por 'ollama_conSR.py' sin problemas)
# Finalmente, este comando queda para la inserción MANUAL por parte del usuario
# sudo python3 /home/vagrant/Desktop/tor-scraper-classifier/ia-classifier/ollama_sinSR.py
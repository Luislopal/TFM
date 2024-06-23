# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# ollama_conSR.py - Lógica para realizar las peticiones al modelo LLM y clasificar los resultados en MISP


import sys
import os
import urllib3
sys.path.append('/home/vagrant/.local/lib/python3.11/site-packages')

from pymisp import PyMISP
import requests
import json
from datetime import datetime

# URL del endpoint de la API para generar respuestas
llm_url = "http://localhost:11434/api/generate"

# Configuración de MISP (*******MODIFICAR DATOS EN LA SEGUNDA LÍNEA*******)
misp_url = "https://localhost"
misp_api_key = "tu-api-key"
misp_verify_cert = False

# Suprimir la advertencia de solicitud HTTPS no verificada
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inicializa PyMISP
misp = PyMISP(misp_url, misp_api_key, ssl=misp_verify_cert, debug=False)

# Ruta al archivo JSON que contiene la lista de URLs y contenido (QUITAR EL TEST PARA EJECUCIÓN COMPLETA)
file_path = "/home/vagrant/Desktop/tor-scraper-classifier/results/scraper_results.json"

# Contexto general proporcionado al modelo LLM
contexto = '''
Clasificar el contenido de la url proporcionada entre las criticidades siguientes (o sin riesgo si no corresponde a ninguna).
Riesgo Crítico: Volcados de bases de datos o Doxing (recopilación de información).
Riesgo Alto: Venta de detalles de tarjetas de pago, Publicación de enlaces entre empleados y contenido ilícito, Publicación de documentos de fraude fiscal, IPs europeas objetivo de hackers pro-rusia, Dominios comprometidos o Cuentas de usuario comprometidas con credenciales.
Riesgo Medio: Publicación del código fuente propietario, Publicación de guías para abrir cuentas fraudulentas, Publicación de plantillas para hacerse pasar por una cuenta de cliente o Cuentas de usuario comprometidas sin credenciales.
Riesgo Bajo: Búsqueda inexperta en la web oscura, IPs filtradas.
Sin Riesgo: Cualquier otra página que no cumpla con ninguno de los indicadores de compromiso (IOCs) anteriores.
SOLO quiero la criticidad, sin justificación ni acentos, EN 2 PALABRAS del contenido de la URL
'''

# Función para enviar una petición y recibir la respuesta
def send_request(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(llm_url, headers=headers, data=json.dumps(data))
    return response.json()

# Cargar los datos de las URLs y su contenido desde el archivo JSON
def cargar_datos(ruta):
    with open(ruta, "r") as file:
        data = json.load(file)
    return data

# Función para determinar el threat level id basado en la criticidad
def determinar_threat_level_id(criticidad):
    criticidad = criticidad.lower().replace(".", "").strip()
    if criticidad == "riesgo critico":
        return 1
    elif criticidad == "riesgo alto":
        return 1
    elif criticidad == "riesgo medio":
        return 2
    elif criticidad == "riesgo bajo":
        return 3
    elif criticidad == "sin riesgo":
        return 4
    
# Función para determinar el tag basado en la criticidad
def determinar_tag(criticidad):
    criticidad = criticidad.lower().replace(".", "").strip()
    if criticidad == "riesgo critico":
        return {"name": "Riesgo Crítico", "colour": "#ff00ff"}
    elif criticidad == "riesgo alto":
        return {"name": "Riesgo Alto", "colour": "#ff0000"}
    elif criticidad == "riesgo medio":
        return {"name": "Riesgo Medio", "colour": "#ffff00"}
    elif criticidad == "riesgo bajo":
        return {"name": "Riesgo Bajo", "colour": "#00ff00"}
    elif criticidad == "sin riesgo":
        return {"name": "Sin Riesgo", "colour": "#000000"}

# Función para crear un evento en MISP y añadirle un tag
def crear_evento_misp(url, contenido, criticidad):
    threat_level_id = determinar_threat_level_id(criticidad)
    tag_info = determinar_tag(criticidad)
    tag = tag_info["name"]
    colour = tag_info.get("colour", "#ffffff")  # Establecer un color por defecto si no está definido
    evento = {
        "info": f"URL: {url}",
        "distribution": 0,
        "threat_level_id": threat_level_id,
        "analysis": 2,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "Tag": [
            {"name": tag, "colour": colour}
        ],
        "Attribute": [
            {
                "type": "url",
                "category": "Network activity",
                "value": url,
                "to_ids": False
            },
            { 
                "type": "text",
                "category": "Other",
                "value": contenido,
                "to_ids": False
            }
        ]
    }
    response = misp.add_event(evento)
    if response:
        print(f"Evento creado exitosamente para la URL: {url} con el tag '{tag}'")
    else:
        print(f"Error al crear evento para la URL: {url}")

# Función para clasificar las páginas web y subir a MISP cada resultado
def clasificar_y_subir_paginas_web(urls, contenidos):
    buffer = []
    resultados = []

    for i, (url, contenido) in enumerate(zip(urls, contenidos)):
        # Enviar las URLs y su contenido
        prompt = f"{contexto}\nContenido de la URL: {contenido[:2000]}"
        response = send_request(prompt)
        print(response)
        # Obtener la etiqueta de riesgo predicha
        predicted_label = response.get("response", "Sin Riesgo").strip()
        resultado = {"url": url, "contenido": contenido, "criticidad_predicha": predicted_label}
        resultados.append(resultado)
        buffer.append(resultado)
        if (i + 1) % 1 == 0:
            for entry in buffer:
                crear_evento_misp(entry["url"], entry["contenido"], entry["criticidad_predicha"])
            buffer = []
    
    # Subir cualquier resultado restante en el buffer
    for entry in buffer:
        crear_evento_misp(entry["url"], entry["contenido"], entry["criticidad_predicha"])
    return resultados
    
# Cargar las URLs y su contenido desde el archivo JSON
data = cargar_datos(file_path)
urls = [d["url"] for d in data]
contenidos = [d["content"] for d in data]

# Clasificar las nuevas páginas web utilizando la API
resultados = clasificar_y_subir_paginas_web(urls, contenidos)

# Nombre del archivo de salida
output_file = "/home/vagrant/Desktop/tor-scraper-classifier/results/classification_results.json"

# Salida de resultados y escritura de estos en el archivo obtenido como salida
with open(output_file, "w") as file:
    for r in resultados:
        print(f"URL: {r['url']}, Criticidad predicha: {r['criticidad_predicha']}")
        json.dump({"url": r["url"], "contenido": r["contenido"], "criticidad_predicha": r["criticidad_predicha"]}, file)
        file.write("\n")

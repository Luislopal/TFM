import sys
import os
import urllib3
sys.path.append('/home/vagrant/.local/lib/python3.11/site-packages')

from pymisp import PyMISP
import requests
import json
from datetime import datetime

# Configuración de MISP (*******MODIFICAR DATOS EN LA SEGUNDA LÍNEA*******)
misp_url = "https://localhost"
misp_api_key = "f9SI2B8OkqNjdHuT9qLfvZGmHaPMn6XGyN9Q48zP"
misp_verify_cert = False

# Suprimir la advertencia de solicitud HTTPS no verificada
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inicializa PyMISP
misp = PyMISP(misp_url, misp_api_key, ssl=misp_verify_cert, debug=False)

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
    else:
        return None

# Función para crear un evento en MISP y añadirle un tag
def crear_evento_y_añadir_tag(url, contenido, criticidad):
    threat_level_id = 1  # Por simplicidad, se puede ajustar según sea necesario
    tag_info = determinar_tag(criticidad)
    tag = tag_info["name"]
    colour = tag_info.get("colour", "#ffffff")  # Establecer un color por defecto si no está definido

    # Crear el evento con el tag directamente
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

# Datos de prueba
url = "http://example.com"
contenido = "Este es un contenido de prueba."
criticidad = "Riesgo Alto"

# Crear el evento y añadir el tag
crear_evento_y_añadir_tag(url, contenido, criticidad)

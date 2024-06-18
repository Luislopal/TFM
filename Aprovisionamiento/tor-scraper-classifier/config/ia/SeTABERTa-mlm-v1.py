# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# Intento de utilizar un modelo LLM de Hugging Face


import json
import requests

# URL de la API de inferencia de Hugging Face para el modelo mdeberta-v3-base-squad2
API_URL = "https://api-inference.huggingface.co/models/mdeberta-v3-base-squad2"

# Token de autenticación para la API de Hugging Face
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
        }

# Ruta al archivo JSON que contiene la lista de URLs y contenido
file_path = "/home/vagrant/Desktop/tor-scraper-classifier/results/scraper_results_test.json"

# Lista de criticidades
#criticidades = ["Crítica", "Alta", "Media", "Baja", "Sin Riesgo"]

# Lista de indicadores de compromiso
contexto = '''
Clasificar el contenido de la url proporcionada entre las criticidades siguientes (o sin riesgo si no corresponde a ninguna).
Riesgo Crítico: Volcados de bases de datos o Doxing (recopilación de información).
Riesgo Alto: Venta de detalles de tarjetas de pago, Publicación de enlaces entre empleados y contenido ilícito, Publicación de documentos de fraude fiscal, Ips europeas objetivo de hackers pro-rusia, Dominios comprometidos o Cuentas de usuario comprometidas con credenciales
Riesgo Medio: Publicación del código fuente propietario, Publicación de guías para abrir cuentas fraudulentas, Publicación de plantillas para hacerse pasar por una cuenta de cliente o Cuentas de usuario comprometidas sin credenciales.
Riesgo Bajo: Búsqueda inexperta en la web oscura, IPs filtradas
Sin Riesgo: Cualquier otra página que no cumpla con ninguno de los indicadores de compromiso (IOCs) anteriores
SOLO quiero la criticidad, sin justificación y EN 2 PALABRAS del contenido de la URL
'''

# Cargar los datos de las URLs y su contenido desde el archivo JSON
def cargar_datos(ruta):
    with open(ruta, "r") as file:
        data = json.load(file)
    return data

# Función para realizar la consulta al modelo de clasificación de páginas web
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Función para clasificar las páginas web utilizando el modelo de clasificación
def clasificar_paginas_web(urls, contenido, contexto):
    resultados = []
    for url, content in zip(urls, contenido):
        # Concatenar la URL, el contenido y el contexto
        entrada_modelo = f"{url} {content} {contexto}"
        
        # Realizar la consulta al modelo de clasificación
        output = query({"inputs": entrada_modelo})
        print(output)
        # Obtener la etiqueta de riesgo predicha
        predicted_label = output.get("answer", "Sin Riesgo")
        resultados.append({"url": url, "criticidad_predicha": predicted_label})
    return resultados

# Cargar las URLs y su contenido desde el archivo JSON
data = cargar_datos(file_path)
urls = [d["url"] for d in data]
contenido = [d["content"] for d in data]

# Clasificar las nuevas páginas web utilizando la API de inferencia
resultados = clasificar_paginas_web(urls, contenido, contexto)

# Nombre del archivo de salida
output_file = "/home/vagrant/Desktop/tor-scraper-classifier/results/classification_results.json"

# Salida de resultados y escritura en el archivo
with open(output_file, "w") as file:
    for r in resultados:
        print(f"URL: {r['url']}, Criticidad predicha: {r['criticidad_predicha']}")
        # Escribir los resultados en el archivo de salida
        json.dump({"url": r["url"], "content": contenido, "criticidad_predicha": r["criticidad_predicha"]}, file)
        file.write("\n")

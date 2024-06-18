# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# ollama.py - Lógica para realizar las peticiones al modelo LLM y clasificar los resultados


import requests
import json

# URL del endpoint de la API para generar respuestas
url = "http://localhost:11434/api/generate"

# Ruta al archivo JSON que contiene la lista de URLs y contenido (QUITAR EL TEST PARA EJECUCIÓN COMPLETA)
file_path = "/home/vagrant/Desktop/tor-scraper-classifier/results/scraper_results_test.json"

# Contexto general proporcionado al modelo LLM
contexto = '''
Clasificar el contenido de la url proporcionada entre las criticidades siguientes (o sin riesgo si no corresponde a ninguna).
Riesgo Crítico: Volcados de bases de datos o Doxing (recopilación de información).
Riesgo Alto: Venta de detalles de tarjetas de pago, Publicación de enlaces entre empleados y contenido ilícito, Publicación de documentos de fraude fiscal, Ips europeas objetivo de hackers pro-rusia, Dominios comprometidos o Cuentas de usuario comprometidas con credenciales
Riesgo Medio: Publicación del código fuente propietario, Publicación de guías para abrir cuentas fraudulentas, Publicación de plantillas para hacerse pasar por una cuenta de cliente o Cuentas de usuario comprometidas sin credenciales.
Riesgo Bajo: Búsqueda inexperta en la web oscura, IPs filtradas
Sin Riesgo: Cualquier otra página que no cumpla con ninguno de los indicadores de compromiso (IOCs) anteriores
SOLO quiero la criticidad, sin justificación y EN 2 PALABRAS del contenido de la URL
'''

# Función para enviar una petición y recibir la respuesta
def send_request(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Cargar los datos de las URLs y su contenido desde el archivo JSON
def cargar_datos(ruta):
    with open(ruta, "r") as file:
        data = json.load(file)
    return data

# Función para clasificar las páginas web utilizando el modelo de clasificación
def clasificar_paginas_web(urls, contenidos):
    resultados = []
    #send_request({"prompt": contexto}) Esto es si quisiera mandar solo una vez el contexto al empezar (Igual ahorro procesamiento pero no se si funcionará)
    for url, contenido in zip(urls, contenidos):
        # Enviar las URLs y su contenido
        prompt = f"{contexto}\nContenido de la URL: {contenido[:2000]}"
        response = send_request(prompt)
        print(response)
        # Obtener la etiqueta de riesgo predicha
        predicted_label = response.get("response", "Sin Riesgo").strip()
        resultados.append({"url": url, "contenido": contenido, "criticidad_predicha": predicted_label})
    return resultados
    
# Cargar las URLs y su contenido desde el archivo JSON
data = cargar_datos(file_path)
urls = [d["url"] for d in data]
contenidos = [d["content"] for d in data]

# Clasificar las nuevas páginas web utilizando la API
resultados = clasificar_paginas_web(urls, contenidos)

# Nombre del archivo de salida
output_file = "/home/vagrant/Desktop/tor-scraper-classifier/results/classification_results.json"

# Salida de resultados y escritura de estos en el archivo obtenido como salida
with open(output_file, "w") as file:
    for r in resultados:
        print(f"URL: {r['url']}, Criticidad predicha: {r['criticidad_predicha']}")
        json.dump({"url": r["url"],"contenido": r["contenido"],"criticidad_predicha": r["criticidad_predicha"]}, file)
        file.write("\n")

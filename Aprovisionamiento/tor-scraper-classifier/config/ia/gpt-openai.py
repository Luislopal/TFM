# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# Intento de realizar consultas a la API de OpenAI


import json
from openai import OpenAI

#EN GPT SE PAGA POR TOKEN, POR LO QUE NO ES UNA OPCIÓN VIABLE PARA METERLE TODOS ESTOS TOKENS
# Ruta al archivo JSON que contiene la lista de URLs y contenido
file_path = "/home/vagrant/Desktop/tor-scraper-classifier/results/scraper_results_test.json"

# Lista de criticidades
#criticidades = ["Crítica", "Alta", "Media", "Baja", "Sin Riesgo"]

# Contexto para la clasificación
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

def query_openai(context, content):
    # Realizar la llamada a la API de OpenAI para clasificar el contenido
    client = OpenAI(
        api_key = 'sk-proj-wqMB60bPB3ejZZQvkcwVT3BlbkFJpYFsOfFgoJSLybnzW2Lg'
    )
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": context}, {"role": "user", "content": content}],
        stream=True
    )

    # Recorrer el flujo de salida y recopilar los fragmentos de texto
    classification = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            classification += chunk.choices[0].delta.content

    return classification

# Función para clasificar las páginas web utilizando el modelo de clasificación
def clasificar_paginas_web(urls, contenido, contexto):
    resultados = []
    for url, content in zip(urls, contenido):
        # Realizar la consulta al modelo de clasificación
        predicted_label = query_openai(contexto, content)
        print(f"URL: {url}, Criticidad predicha: {predicted_label}")
        resultados.append({"url": url, "criticidad_predicha": predicted_label})
    return resultados

# Cargar las URLs y su contenido desde el archivo JSON
data = cargar_datos(file_path)
urls = [d["url"] for d in data]
contenido = [d["content"] for d in data]

# Clasificar las nuevas páginas web utilizando la API de OpenAI
resultados = clasificar_paginas_web(urls, contenido, contexto)

# Nombre del archivo de salida
output_file = "/home/vagrant/Desktop/tor-scraper-classifier/results/classification_results.json"

# Salida de resultados y escritura en el archivo
with open(output_file, "w") as file:
    json.dump(resultados, file, indent=4)

print("Clasificación completada y guardada en el archivo:", output_file)

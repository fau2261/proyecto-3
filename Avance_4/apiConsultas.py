import requests
import pickle
import os
from persona import Persona

# Función para guardar los datos en el archivo coordenadasCasas.dat
def guardarCoordenadas(listaCoordenadas):
    with open("./archivosJuego/coordenadasCasas.dat", 'wb') as archivo:
        pickle.dump(listaCoordenadas, archivo)

# Función para leer los datos del archivo coordenadasCasas.dat
def cargarCoordenadas():
    if os.path.exists("./archivosJuego/coordenadasCasas.dat") and os.path.getsize("./archivosJuego/coordenadasCasas.dat") > 0:
        with open("./archivosJuego/coordenadasCasas.dat", 'rb') as archivo:
            return pickle.load(archivo)
    else:
        return []

# Función para consultar los habitantes de una casa
def consultarPersonasCasa(casa):
    # Verificar si el archivo coordenadasCasas.dat está lleno
    datosCoordenadas = cargarCoordenadas()
    if datosCoordenadas:
        return datosCoordenadas
    
    # Si el archivo está vacío, consultar la API y guardar los datos
    respuestaHabitantes = requests.get(f'https://geneacity.life/API/getHousesResidents/?houseId={casa["id"]}')
    respuestaJson = respuestaHabitantes.json()
    
    residentes = respuestaJson["residents"]
    listaPersonas = []
    for residente in residentes:
        objPersona = Persona(residente["id"], residente["name"], residente["gender"], residente["marital_status"], residente["father"], residente["mother"])
        listaPersonas.append(objPersona)
    
    guardarCoordenadas(listaPersonas)
    return listaPersonas

# Función para consultar las coordenadas de las casas en el mapa
def consultarCasasMapa():
    # Verificar si el archivo coordenadasCasas.dat está lleno
    datosCoordenadas = cargarCoordenadas()
    if datosCoordenadas:
        return datosCoordenadas  # Asume que las coordenadas ya fueron consultadas y guardadas

    coordenadasCasas = []

    for y in range(400, 10400, 800):  # Recorre las coordenadas en y y establece un rango de 400 a 10400 (final del mapa) con un incremento de 800
        for x in range(400, 10400, 800):  # Recorre coordenadas en x y repite el rango anterior
            respuestaApi = requests.get(f'https://geneacity.life/API/getHouses/?x={x}&y={y}')  # Realiza la consulta al API (sobre ubicacion de casas)
            if respuestaApi.status_code == 200:  # Si la respuesta es correcta
                if respuestaApi.json()["status"] == 1:  # Si el status es 1, es porque hay una casa y entra en el bucle
                    for casa in respuestaApi.json()["houses"]:  # Recorre las casas
                        coordenadasCasas.append((int(casa["x"]), int(casa["y"])))  # Agrega las coordenadas de la casa a la lista
                        personasCasa = consultarPersonasCasa(casa)  # Llama a la función para consultar los habitantes de la casa
            else:
                print(respuestaApi.status_code)

    guardarCoordenadas(coordenadasCasas)  # Guarda las coordenadas de las casas
    return coordenadasCasas  # Retorna la lista de coordenadas de las casas

# Función para consultar información de una persona por su ID
def consultarInfoPersona(id):
    respuestaApi = requests.get(f"https://geneacity.life/API/getInhabitantInformation/?id={id}")
    infoPersona = respuestaApi.json()["inhabitant"]
    return infoPersona

# Función para seleccionar un jugador a través de la API
def seleccionarJugadorAPI(id):
    respuestaApi = requests.get(f"https://geneacity.life/API/selectAvailableInhabitant/?id={id}")
    estadoRespuesta = respuestaApi.json()["status"]
    return estadoRespuesta

import requests
import pickle
import os
import json
from persona import Persona, personas

with open('./archivosJuego/infoJuego.json', 'r') as archivo:
            # Cargar el contenido del archivo JSON en un diccionario
            datosJuego = json.load(archivo)

def crearObjJugador():
    if datosJuego["id"] != None:
        #Obtener el id del jugador
        idJugador = datosJuego["id"]

        infoJugador = consultarInfoPersona(idJugador)
        objJugador = Persona(infoJugador["id"], infoJugador["name"], infoJugador["gender"], infoJugador["marital_status"], infoJugador["father"], infoJugador["mother"], infoJugador["age"])
        personas.append(objJugador)
        
        return objJugador

def encontrarObjetoPersona(id):
    for persona in personas:
        if str(persona.id) == str(id):
            return persona
            
    return False

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

# Función para consultar los habitantes de una casa
def consultarPersonasCasa(casaId):
    respuestaHabitantes = requests.get(f'https://geneacity.life/API/getHousesResidents/?houseId={casaId}')
    respuestaJson = respuestaHabitantes.json()

    if respuestaJson['status'] == 1:
        residentes = respuestaJson["residents"]
        listaPersonas = []
        for residente in residentes:
            objPersona = encontrarObjetoPersona(residente["id"])
            if objPersona == False:
                infoPersona = consultarInfoPersona(residente["id"])
                
                objPersona = Persona(residente["id"], residente["name"], residente["gender"], residente["marital_status"], residente["father"], residente["mother"], infoPersona["age"])
            listaPersonas.append(objPersona)
        return listaPersonas
    return False

# Función para consultar las coordenadas de las casas en el mapa
def consultarCasasMapa():
    coordenadasCasas = []
    
    crearObjJugador()

    for y in range(400, 10400, 800):  # Recorre las coordenadas en y y establece un rango de 400 a 10400 (final del mapa) con un incremento de 800
        for x in range(400, 10400, 800):  # Recorre coordenadas en x y repite el rango anterior
            respuestaApi = requests.get(f'https://geneacity.life/API/getHouses/?x={x}&y={y}')  # Realiza la consulta al API (sobre ubicacion de casas)
            if respuestaApi.status_code == 200:  # Si la respuesta es correcta
                if respuestaApi.json()["status"] == 1:  # Si el status es 1, es porque hay una casa y entra en el bucle
                    for casa in respuestaApi.json()["houses"]:  # Recorre las casas
                        coordenadasCasas.append({'id': casa['id'] ,'x': int(casa["x"]), 'y': int(casa["y"])})  # Agrega las coordenadas de la casa a la lista
                        
                        print(f'CASA {casa['id']} : {casa["x"]} {casa["y"]}')
                        personasCasa = consultarPersonasCasa(casa['id'])  # Llama a la función para consultar los habitantes de la casa
            else:
                print(respuestaApi.status_code)

    #guardarCoordenadas(coordenadasCasas)  # Guarda las coordenadas de las casas
    return coordenadasCasas  # Retorna la lista de coordenadas de las casas

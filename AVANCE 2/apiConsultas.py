import requests
from persona import Persona

def consultarPersonasCasa(casa):
    #Imprima la información de los habitantes de la casa
    respuestaHabitantes = requests.get(f'https://geneacity.life/API/getHousesResidents/?houseId={casa["id"]}')
    respuestaJson = respuestaHabitantes.json()

    residentes = respuestaJson["residents"]
    #For each
    for residente in residentes:
        """print(residente["id"], residente["name"], residente["gender"], residente["marital_status"], residente["father"], residente["mother"])"""
        objPersona = Persona(residente["id"], residente["name"], residente["gender"], residente["marital_status"], residente["father"], residente["mother"])
        

def consultarCasasMapa():
    contCuadrante = 0
    coordenadasCasas = []

    for y in range(400, 10400, 800): #Recorre las coordenadas en y y establece un rango de 400 a 10400 (final del mapa) con un incremento de 800
        for x in range(400, 10400, 800): #recorre coordenadas en x y repite el rango anterio
            respuestaApi = requests.get(f'https://geneacity.life/API/getHouses/?x={x}&y={y}') #Realiza la consulta al API (sobre ubicacion de casas)
            if respuestaApi.status_code == 200: #Si la respuesta es correcta
                if respuestaApi.json()["status"] == 1: #si el status es 1, es porque hay una casa y entra en el bucle
                    for casa in respuestaApi.json()["houses"]: #recorre las casas
                        coordenadasCasas.append((int(casa["x"]), int(casa["y"]))) #agrega las coordenadas de la casa a la lista

                        consultarPersonasCasa(casa) #llama a la funcion para consultar los habitantes de la casa
            else:
                print(respuestaApi.status_code) 
            contCuadrante += 1

    return coordenadasCasas #retorna la lista de coordenadas de las casas

consultarCasasMapa() #llama a la funcion, para que se ejecute
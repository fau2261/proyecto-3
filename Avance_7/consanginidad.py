import json
from apiConsultas import *
from persona import personas
import pygame

#Obtener puntaje jugador
def leerDatosJuego():
    global datosJuego, puntaje_judador, idJugador
    with open('./archivosJuego/infoJuego.json', 'r') as archivo:
        # Cargar el contenido del archivo JSON en un diccionario
        datosJuego = json.load(archivo)

        puntaje_judador = datosJuego["puntaje"]
        idJugador = datosJuego["id"]

leerDatosJuego()

def guardarDatosJuego(datos):
    with open('./archivosJuego/infoJuego.json', 'w') as archivo:
        json.dump(datos, archivo)

#Encontrar el objeto de una persona mediante su id
def encontrarObjetoPersona(id):
    if personas == []:
        consultarCasasMapa()

    for persona in personas:
        if str(persona.id) == str(id):
            return persona
            
    return False

# Rango 1
def esMiPadre(idPersona):
    global puntaje_judador
    
    idPersona = str(idPersona)
    
    if jugador.padre == idPersona or jugador.madre == idPersona:
        puntaje_judador += 5
        return True
    else:
        return False


def esMiHijo(idPersona):
    global puntaje_judador

    persona = encontrarObjetoPersona(idPersona)
    
    if persona.padre == idJugador or persona.madre == idJugador:
        puntaje_judador += 5
        return True
    else:
        return False


# RANGO 2
def esMiAbuelo(idPersona):
    global puntaje_judador

    idPersona = str(idPersona)
    
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idPersona) or (madre and str(madre.id) == idPersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # vereficar 
    if (padre and (str(padre.padre) == idPersona or str(padre.madre) == idPersona)) or \
       (madre and (str(madre.padre) == idPersona or str(madre.madre) == idPersona)):
        puntaje_judador += 10
        return True
    else:
        return False


def esMiNieto(idPersona):
    global puntaje_judador

    idPersona = str(idPersona)
    
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idPersona) or (madre and str(madre.id) == idPersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser nieto
        return False
    
    # Buscar a los hijos del jugador
    hijos = []
    for persona in personas:
        if str(persona.padre) == str(jugador.id) or str(persona.madre) == str(jugador.id):
            hijos.append(persona)
    
    # Verificar si la persona es nieto
    for hijo in hijos:
        if str(hijo.id) == idPersona:
            puntaje_judador += 10
            return True
    
    return False

def esMiHermano(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser hermano
        return False
    
    # Buscar a los hijos del jugador
    hermanos = []
    for persona in personas:
        if (str(persona.padre) == str(jugador.padre) or str(persona.madre) == str(jugador.madre)) and str(persona.id) != str(jugador.id):
            hermanos.append(persona)
    
    # Verificar si la persona es hermano
    for hermano in hermanos:
        if str(hermano.id) == idpersona:
            puntaje_judador +=10
            return True
    
    return False

# GRADO 3   (+15)
def esMiTio(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser tio
        return False
    
    # Buscar a los hermanos del padre
    hermanosPadre = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanosPadre.append(persona)
    
    # Buscar a los hermanos de la madre
    hermanosMadre = []
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanosMadre.append(persona)
    
    # Verificar si la persona es tio
    for hermano in hermanosPadre:
        if str(hermano.id) == idpersona:
            puntaje_judador +=15
            return True
    
    for hermano in hermanosMadre:
        if str(hermano.id) == idpersona:
            puntaje_judador +=15
            return True
    
    return False

def esMiSobrino(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            if str(hijo.id) == idpersona:
                puntaje_judador += 15
                return True
    return False

def esMiBisabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontrarObjetoPersona(padre.padre)
        abuelaPadre = encontrarObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontrarObjetoPersona(madre.padre)
        abuelaMadre = encontrarObjetoPersona(madre.madre)
        if abueloMadre:
            abuelos.append(abueloMadre)
        if abuelaMadre:
            abuelos.append(abuelaMadre)
    
    # Verificar si la persona es abuelo
    for abuelo in abuelos:
        if str(abuelo.id) == idpersona:
            puntaje_judador += 15
            return True
    
    return False

def esMiBisnieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser nieto
        return False
    
    # Buscar a los hijos del jugador
    hijos = []
    for persona in personas:
        if str(persona.padre) == str(jugador.id) or str(persona.madre) == str(jugador.id):
            hijos.append(persona)
    
    # Verificar si la persona es nieto
    for hijo in hijos:
        nietos = []
        for persona in personas:
            if str(persona.padre) == str(hijo.id):
                nietos.append(persona)
        for nieto in nietos:
            if str(nieto.id) == idpersona:
                puntaje_judador += 15
                return True
         
    return False


# GRADO 4 (+20)

def esMiTataraabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontrarObjetoPersona(padre.padre)
        abuelaPadre = encontrarObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontrarObjetoPersona(madre.padre)
        abuelaMadre = encontrarObjetoPersona(madre.madre)
        if abueloMadre:
            abuelos.append(abueloMadre)
        if abuelaMadre:
            abuelos.append(abuelaMadre)
    
    # Verificar si la persona es abuelo
    for abuelo in abuelos:
        bisabuelo = []
        for persona in personas:
            if str(persona.padre) == str(abuelo.id):
                bisabuelo.append(persona)
        for bis in bisabuelo:
            if str(bis.id) == idpersona:
                puntaje_judador += 20
                return True
    return False

def esMiTataranieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser nieto
        return False
    
    # Buscar a los hijos del jugador
    hijos = []
    for persona in personas:
        if str(persona.padre) == str(jugador.id) or str(persona.madre) == str(jugador.id):
            hijos.append(persona)
    
    # Verificar si la persona es nieto
    for hijo in hijos:
        nietos = []
        for persona in personas:
            if str(persona.padre) == str(hijo.id):
                nietos.append(persona)
        for nieto in nietos:
            bisnietos = []
            for persona in personas:
                if str(persona.padre) == str(nieto.id):
                    bisnietos.append(persona)
            for bisnieto in bisnietos:
                if str(bisnieto.id) == idpersona:
                    puntaje_judador += 20
                    return True
    return False


def esMiTioAbuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser tio
        return False
    
    # Buscar a los hermanos del padre
    hermanosPadre = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanosPadre.append(persona)
    
    # Buscar a los hermanos de la madre
    hermanosMadre = []
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanosMadre.append(persona)
    
    # Verificar si la persona es tio
    for hermano in hermanosPadre:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            if str(hijo.id) == idpersona:
                puntaje_judador += 20
                return True
    
    for hermano in hermanosMadre:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            if str(hijo.id) == idpersona:
                puntaje_judador += 20
                return True
    
    return False

def esMiPrimo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            nietos_hijo = []
            for persona in personas:
                if str(persona.padre) == str(hijo.id):
                    nietos_hijo.append(persona)
            for nieto in nietos_hijo:
                if str(nieto.id) == idpersona:

                 puntaje_judador += 20
                return True
    return False

def esMiSobrinoNieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            nietos_hijo = []
            for persona in personas:
                if str(persona.padre) == str(hijo.id):
                    nietos_hijo.append(persona)
            for nieto in nietos_hijo:
                bisnietos_nieto = []
                for persona in personas:
                    if str(persona.padre) == str(nieto.id):
                        bisnietos_nieto.append(persona)
                for bisnieto in bisnietos_nieto:
                    if str(bisnieto.id) == idpersona:
                     puntaje_judador += 20
                    return True
    return False


def esMiTrastataraAbuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontrarObjetoPersona(padre.padre)
        abuelaPadre = encontrarObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontrarObjetoPersona(madre.padre)
        abuelaMadre = encontrarObjetoPersona(madre.madre)
        if abueloMadre:
            abuelos.append(abueloMadre)
        if abuelaMadre:
            abuelos.append(abuelaMadre)
    
    # Verificar si la persona es abuelo
    for abuelo in abuelos:
        bisabuelo = []
        for persona in personas:
            if str(persona.padre) == str(abuelo.id):
                bisabuelo.append(persona)
        for bis in bisabuelo:
            trastatarabuelo = []
            for persona in personas:
                if str(persona.padre) == str(bis.id):
                    trastatarabuelo.append(persona)
            for trastarabuelo in trastatarabuelo:
                if str(trastarabuelo.id) == idpersona:
                    puntaje_judador += 25
                    return True
    return False

def esMiTrastaranieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser nieto
        return False
    
    # Buscar a los hijos del jugador
    hijos = []
    for persona in personas:
        if str(persona.padre) == str(jugador.id) or str(persona.madre) == str(jugador.id):
            hijos.append(persona)
    
    # Verificar si la persona es nieto
    for hijo in hijos:
        nietos = []
        for persona in personas:
            if str(persona.padre) == str(hijo.id):
                nietos.append(persona)
        for nieto in nietos:
            bisnietos = []
            for persona in personas:
                if str(persona.padre) == str(nieto.id):
                    bisnietos.append(persona)
            for bisnieto in bisnietos:
                trastataranietos = []
                for persona in personas:
                    if str(persona.padre) == str(bisnieto.id):
                        trastataranietos.append(persona)
                for trastaranieto in trastataranietos:
                    if str(trastaranieto.id) == idpersona:
                        puntaje_judador += 25
                        return True
    return False

def esMiTioBisabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser tio
        return False
    
    # Buscar a los hermanos del padre
    hermanosPadre = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanosPadre.append(persona)
    
    # Buscar a los hermanos de la madre
    hermanosMadre = []
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanosMadre.append(persona)
    
    # Verificar si la persona es tio
    for hermano in hermanosPadre:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            if str(hijo.id) == idpersona:
                return True
    
    for hermano in hermanosMadre:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            if str(hijo.id) == idpersona:
                puntaje_judador += 25
                return True
    
    return False

def esMiTioSegundo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            nietos_hijo = []
            for persona in personas:
                if str(persona.padre) == str(hijo.id):
                    nietos_hijo.append(persona)
            for nieto in nietos_hijo:
                if str(nieto.id) == idpersona:
                    puntaje_judador += 25
                    return True
    return False

def esMiSobrinoSegundo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            nietos_hijo = []
            for persona in personas:
                if str(persona.padre) == str(hijo.id):
                    nietos_hijo.append(persona)
            for nieto in nietos_hijo:
                if str(nieto.id) == idpersona:
                    puntaje_judador += 25
                    return True
    return False

def esMiSobrinoBisnieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            nietos_hijo = []
            for persona in personas:
                if str(persona.padre) == str(hijo.id):
                    nietos_hijo.append(persona)
            for nieto in nietos_hijo:
                bisnietos_nieto = []
                for persona in personas:
                    if str(persona.padre) == str(nieto.id):
                        bisnietos_nieto.append(persona)
                for bisnieto in bisnietos_nieto:
                    if str(bisnieto.id) == idpersona:
                        puntaje_judador += 25
                        return True
    return False

# grado 6 (+30) (pentabuelo, pentanieto, tio tataraabuelo, tio tataranieto,  tio tercero, sobrino tercero , )

def esMiPentabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontrarObjetoPersona(padre.padre)
        abuelaPadre = encontrarObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontrarObjetoPersona(madre.padre)
        abuelaMadre = encontrarObjetoPersona(madre.madre)
        if abueloMadre:
            abuelos.append(abueloMadre)
        if abuelaMadre:
            abuelos.append(abuelaMadre)
    
    # Verificar si la persona es abuelo
    for abuelo in abuelos:
        bisabuelo = []
        for persona in personas:
            if str(persona.padre) == str(abuelo.id):
                bisabuelo.append(persona)
        for bis in bisabuelo:
            trastatarabuelo = []
            for persona in personas:
                if str(persona.padre) == str(bis.id):
                    trastatarabuelo.append(persona)
            for trastarabuelo in trastatarabuelo:
                pentabuelo = []
                for persona in personas:
                    if str(persona.padre) == str(trastarabuelo.id):
                        pentabuelo.append(persona)
                for pentab in pentabuelo:
                    if str(pentab.id) == idpersona:
                        puntaje_judador += 30
                        return True
    return False

def esMiPentanieto(idpersona):
    global puntaje_judador


    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser nieto
        return False
    
    # Buscar a los hijos del jugador
    hijos = []
    for persona in personas:
        if str(persona.padre) == str(jugador.id) or str(persona.madre) == str(jugador.id):
            hijos.append(persona)
    
    # Verificar si la persona es nieto
    for hijo in hijos:
        nietos = []
        for persona in personas:
            if str(persona.padre) == str(hijo.id):
                nietos.append(persona)
        for nieto in nietos:
            bisnietos = []
            for persona in personas:
                if str(persona.padre) == str(nieto.id):
                    bisnietos.append(persona)
            for bisnieto in bisnietos:
                trastataranietos = []
                for persona in personas:
                    if str(persona.padre) == str(bisnieto.id):
                        trastataranietos.append(persona)
                for trastaranieto in trastataranietos:
                    pentanietos = []
                    for persona in personas:
                        if str(persona.padre) == str(trastaranieto.id):
                            pentanietos.append(persona)
                    for pentanieto in pentanietos:
                        if str(pentanieto.id) == idpersona:
                            puntaje_judador += 30
                            return True
    return False

def esMiTioTataraabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser tio
        return False
    
    # Buscar a los hermanos del padre
    hermanosPadre = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanosPadre.append(persona)
    
    # Buscar a los hermanos de la madre
    hermanosMadre = []
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanosMadre.append(persona)
    
    # Verificar si la persona es tio
    for hermano in hermanosPadre:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            if str(hijo.id) == idpersona:
                return True
    
    for hermano in hermanosMadre:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            if str(hijo.id) == idpersona:
                puntaje_judador += 30
                return True
    
    return False

def esMiTioTataranieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontrarObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontrarObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser nieto
        return False
    
    # Buscar a los hijos del jugador
    hijos = []
    for persona in personas:
        if str(persona.padre) == str(jugador.id) or str(persona.madre) == str(jugador.id):
            hijos.append(persona)
    
    # Verificar si la persona es nieto
    for hijo in hijos:
        nietos = []
        for persona in personas:
            if str(persona.padre) == str(hijo.id):
                nietos.append(persona)
        for nieto in nietos:
            bisnietos = []
            for persona in personas:
                if str(persona.padre) == str(nieto.id):
                    bisnietos.append(persona)
            for bisnieto in bisnietos:
                trastataranietos = []
                for persona in personas:
                    if str(persona.padre) == str(bisnieto.id):
                        trastataranietos.append(persona)
                for trastaranieto in trastataranietos:
                    pentanietos = []
                    for persona in personas:
                        if str(persona.padre) == str(trastaranieto.id):
                            pentanietos.append(persona)
                    for pentanieto in pentanietos:
                        if str(pentanieto.id) == idpersona:
                            puntaje_judador += 30
                            return True
    return False

def esMiTioTercero(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            nietos_hijo = []
            for persona in personas:
                if str(persona.padre) == str(hijo.id):
                    nietos_hijo.append(persona)
            for nieto in nietos_hijo:
                bisnietos_nieto = []
                for persona in personas:
                    if str(persona.padre) == str(nieto.id):
                        bisnietos_nieto.append(persona)
                for bisnieto in bisnietos_nieto:
                    trastataranietos = []
                    for persona in personas:
                        if str(persona.padre) == str(bisnieto.id):
                            trastataranietos.append(persona)
                    for trastaranieto in trastataranietos:
                        if str(trastaranieto.id) == idpersona:
                            puntaje_judador += 30
                            return True
    return False

def esMiSobrinoTercero(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontrarObjetoPersona(jugador.padre)
    madre = encontrarObjetoPersona(jugador.madre)
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        return False
    # Buscar a los hijos de los hermanos
    hermanos = []
    if padre:
        for persona in personas:
            if str(persona.padre) == str(padre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    if madre:
        for persona in personas:
            if str(persona.padre) == str(madre.id) and str(persona.id) != str(jugador.id):
                hermanos.append(persona)
    for hermano in hermanos:
        hijos_hermano = []
        for persona in personas:
            if str(persona.padre) == str(hermano.id):
                hijos_hermano.append(persona)
        for hijo in hijos_hermano:
            nietos_hijo = []
            for persona in personas:
                if str(persona.padre) == str(hijo.id):
                    nietos_hijo.append(persona)
            for nieto in nietos_hijo:
                bisnietos_nieto = []
                for persona in personas:
                    if str(persona.padre) == str(nieto.id):
                        bisnietos_nieto.append(persona)
                for bisnieto in bisnietos_nieto:
                    trastataranietos = []
                    for persona in personas:
                        if str(persona.padre) == str(bisnieto.id):
                            trastataranietos.append(persona)
                    for trastaranieto in trastataranietos:
                        pentanietos = []
                        for persona in personas:
                            if str(persona.padre) == str(trastaranieto.id):
                                pentanietos.append(persona)
                        for pentanieto in pentanietos:
                            if str(pentanieto.id) == idpersona:
                                puntaje_judador += 30
                                return True
    return False

def comprobarConsanginidad(idHabitante):
    global jugador
    
    leerDatosJuego()
    #Buscar los grados de consanginidad
    jugador = encontrarObjetoPersona(idJugador)
    
    funciones = [
        esMiPadre,
        esMiHijo,
        esMiAbuelo,
        esMiNieto,
        esMiHermano,
        esMiTio,
        esMiSobrino,
        esMiBisabuelo,
        esMiBisnieto,
        esMiTataraabuelo,
        esMiTataranieto,
        esMiTioAbuelo,
        esMiPrimo,
        esMiSobrinoNieto,
        esMiTrastataraAbuelo,
        esMiTrastaranieto,
        esMiTioBisabuelo,
        esMiTioSegundo,
        esMiSobrinoSegundo,
        esMiSobrinoBisnieto,
        esMiPentabuelo,
        esMiPentanieto,
        esMiTioTataraabuelo,
        esMiTioTataranieto,
        esMiTioTercero,
        esMiSobrinoTercero
    ]
    
    #Si el habitante ya fue encontrado
    if  idHabitante in datosJuego["habitantesEncontrados"]:
        return True
    
    #Si no ha sido encontrado
    for funcion in funciones:
        if funcion(idHabitante):
            datosJuego["habitantesEncontrados"].append(idHabitante)
            datosJuego["puntaje"] = puntaje_judador
            guardarDatosJuego(datosJuego)
            return True

    return False #Si no se encuentra
import json
from apiConsultas import *
from persona import personas
import pygame

#Obtener el id del jugador
with open('./archivosJuego/jugador.json', 'r') as archivo:
    # Cargar el contenido del archivo JSON en un diccionario
    datosJugador = json.load(archivo)

idJugador = datosJugador["id"]
puntaje_judador = 0

#Encontrar el objeto de una persona mediante su id
def encontraObjetoPersona(id):
    if len(personas) == 0:
        consultarCasasMapa() #Para no tener que ejecutar el juego
    
    for persona in personas:
        if str(persona.id) == str(id):
            return persona
            
    return False

#Buscar los grados de consanginidad
jugador = encontraObjetoPersona(idJugador)

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

    persona = encontraObjetoPersona(idPersona)
    
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
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMiHermano(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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
def EsMiTio(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMiSobrino(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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

def EsMibisabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontraObjetoPersona(padre.padre)
        abuelaPadre = encontraObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontraObjetoPersona(madre.padre)
        abuelaMadre = encontraObjetoPersona(madre.madre)
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

def EsMiBisnieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMitataraabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontraObjetoPersona(padre.padre)
        abuelaPadre = encontraObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontraObjetoPersona(madre.padre)
        abuelaMadre = encontraObjetoPersona(madre.madre)
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

def EsMitataranieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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


def EsMiTioAbuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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

def EsMiSobrinoNieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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


# grado 5 (+25) (trastataraabuelo, trastataranieto, tio-bisabuelo, tio Sengundo, sobrino segundo, sobrino bisnietos )

def EsMiTrastataraabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontraObjetoPersona(padre.padre)
        abuelaPadre = encontraObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontraObjetoPersona(madre.padre)
        abuelaMadre = encontraObjetoPersona(madre.madre)
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

def EsMiTrastaranieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMiTioBisabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMiTioSegundo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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

def EsMiSobrinoSegundo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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

def EsMiSobrinoBisnieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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

def EsMiPentabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
    # Verificar si la persona es el padre o la madre del jugador
    if (padre and str(padre.id) == idpersona) or (madre and str(madre.id) == idpersona):
        # Si la persona es el padre o la madre del jugador, entonces no puede ser abuelo
        return False
    
    # Buscar a los abuelos del jugador
    abuelos = []
    if padre:
        abueloPadre = encontraObjetoPersona(padre.padre)
        abuelaPadre = encontraObjetoPersona(padre.madre)
        if abueloPadre:
            abuelos.append(abueloPadre)
        if abuelaPadre:
            abuelos.append(abuelaPadre)
    if madre:
        abueloMadre = encontraObjetoPersona(madre.padre)
        abuelaMadre = encontraObjetoPersona(madre.madre)
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

def EsMiPentanieto(idpersona):
    global puntaje_judador


    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMiTioTataraabuelo(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMiTioTataranieto(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    
    # Buscar al padre del jugador
    padre = encontraObjetoPersona(jugador.padre)
    # Buscar a la madre del jugador
    madre = encontraObjetoPersona(jugador.madre)
    
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

def EsMiTioTercero(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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

def EsMiSobrinoTercero(idpersona):
    global puntaje_judador

    idpersona = str(idpersona)
    padre = encontraObjetoPersona(jugador.padre)
    madre = encontraObjetoPersona(jugador.madre)
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
    pass
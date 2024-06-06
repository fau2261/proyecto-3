import pygame
import json
import consanginidad
from apiConsultas import *
from persona import personas
import schedule
import datetime
import time

with open('./archivosJuego/infoJuego.json', 'r') as archivo:
    # Cargar el contenido del archivo JSON en un diccionario
    datosJuego = json.load(archivo)

def guardarDatosJuego(datos):
    with open('./archivosJuego/infoJuego.json', 'w') as archivo:
        json.dump(datos, archivo)
        
def guardarPartida(jsonPartida):
    try:
        # Intenta abrir el archivo en modo lectura
        with open('./archivosJuego/historial.txt', 'r') as archivo:
            # Carga el contenido del archivo como una lista de diccionarios
            partidas = json.load(archivo)
    except FileNotFoundError:
        # Si el archivo no existe, inicializa una lista vacía
        partidas = []
    
    # Agrega el nuevo diccionario a la lista de partidas
    partidas.append(jsonPartida)
    
    # Abre el archivo en modo escritura para sobrescribirlo con la lista actualizada
    with open('./archivosJuego/historial.txt', 'w') as archivo:
        # Escribe la lista de partidas en el archivo
        json.dump(partidas, archivo)

def mostrarPopup(mensaje):
    pygame.init()
    popup_ancho = 1000
    popup_alto = 200
    popup_ventana = pygame.display.set_mode((popup_ancho, popup_alto))
    pygame.display.set_caption("Popup")

    font = pygame.font.Font(None, 24)
    texto = font.render(mensaje, True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(popup_ancho // 2, popup_alto // 2))

    popup_ventana.fill((0, 0, 0))
    popup_ventana.blit(texto, texto_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

def seleccionarJugador(mensaje):
    pygame.init()
    popup_ancho = 400
    pantalla_alto = 600
    popup_alto = 200 + len(personas) * 30  # Ajuste el alto de la ventana según el número de personas
    popup_ventana = pygame.display.set_mode((popup_ancho, pantalla_alto))
    pygame.display.set_caption("Popup")

    font = pygame.font.Font(None, 24)
    texto = font.render(mensaje, True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(popup_ancho // 2, 30))

    popup_ventana.fill((0, 0, 0))
    popup_ventana.blit(texto, texto_rect)

    scroll_pos = 0  # Posición de desplazamiento inicial

    # Mostrar lista de personas
    while True:
        for i, persona in enumerate(personas):
            if 60 + i * 30 - scroll_pos > 0 and 60 + i * 30 - scroll_pos < pantalla_alto:
                texto_persona = font.render(persona.nombre, True, (255, 255, 255))
                texto_rect_persona = texto_persona.get_rect(topleft=(30, 60 + i * 30 - scroll_pos))
                popup_ventana.blit(texto_persona, texto_rect_persona)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scroll_pos = max(0, scroll_pos - 30)  # Desplazar hacia arriba
                elif event.key == pygame.K_DOWN:
                    scroll_pos = min(popup_alto - pantalla_alto, scroll_pos + 30)  # Desplazar hacia abajo
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Verificar clic de botón izquierdo del mouse
                for i, persona in enumerate(personas):
                    texto_rect_persona = pygame.Rect(30, 60 + i * 30 - scroll_pos, 200, 30)
                    if texto_rect_persona.collidepoint(event.pos):
                        datosJuego["id"] = persona.id  # Asignar el ID de la persona seleccionada
                        # Guardar los datos del jugador seleccionado en el archivo JSON
                        if seleccionarJugadorAPI(persona.id):
                            guardarDatosJuego(datosJuego)
                        else:
                            mostrarPopup("Jugador no disponible, se le dará al jugador por defecto.")
                            datosJuego["id"] = "1"
                            guardarDatosJuego(datosJuego)
                            
                        print(persona.id)
                        pygame.quit()
                        return

def tenerHijos():

    personas=[]
    #for persona in personas 
    pass

def casar():
    pass

# funcion del tiempo
import datetime

def ejecutarCiclo():
    def guardar_hora():
        with open("./archivosJuego/horas.txt", "w") as archivo:
            hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(hora_actual + "\n")

    def contar_ciclos():
        with open("./archivosJuego/horas.txt", "r") as archivo:
            ultima_conexion = datetime.datetime.fromisoformat(archivo.read().strip())

        hora_actual= datetime.datetime.now()
        diferencia = hora_actual - ultima_conexion
    
        ciclos_pasados = int(diferencia.total_seconds() // (3 * 60 * 60))
        print(f"Horas pasadas: {diferencia}")
        print(f"Ciclos pasados: {ciclos_pasados}")
        
        for iCiclo in range(ciclos_pasados):
            casar()
            tenerHijos()

    contar_ciclos()
    guardar_hora()


def crearNuevaPartida():
    #Guardar partida actual en el historial
    guardarPartida(datosJuego)
    
    #Se reinician los datos del juego
    consanginidad.puntaje_judador = 0
    datosJuego["puntaje"] = 0
    datosJuego["id"] = None
    datosJuego["habitantesEncontrados"] = []
    
    guardarDatosJuego(datosJuego)
    
    iniciarJuego()


def iniciarJuego():
    global infoCasas
    
    #Obtiene las posiciones de las casas y crea a las personas
    infoCasas = consultarCasasMapa()
    ejecutarCiclo()
    
    #Si no se ha seleccionado un personaje para jugar
    if datosJuego["id"] == None or encontraObjetoPersona(datosJuego["id"]) == False:
        seleccionarJugador("Seleccione un jugador antes de continuar.")
    
    # Inicializar pygame
    pygame.init()

    # Crear la ventana
    ANCHO_VENTANA = 800
    ALTO_VENTANA = 800
    vtnJuego = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

    # Definir título e ícono
    pygame.display.set_caption("GeneaCity")  # Título

    icon = pygame.image.load("./assets/icono.png")  # Cargando imagen
    pygame.display.set_icon(icon)  # Asignando ícono
    clock = pygame.time.Clock()

    # Crear el mapa
    ANCHO_MAPA = 10000
    ALTO_MAPA = 10000
    mapa = pygame.Surface((ANCHO_MAPA, ALTO_MAPA))

    # Cambiar color del mapa
    mapa.fill((197, 216, 109))  # RGB

    # Jugador
    imgHombre = pygame.image.load("assets/hombre3.png").convert_alpha()
    rectHombre = imgHombre.get_rect(center=(ANCHO_MAPA // 2, ALTO_MAPA // 2))

    # Fuente para mostrar coordenadas
    fuente = pygame.font.Font(None, 36)
    
    # Crear Casas
    imgCasa = pygame.image.load("assets/casa1.png").convert_alpha()
    casasRects = []

    for infoCasa in infoCasas:
        posc = (infoCasa['x'], infoCasa['y'])

        try:
            # Ajustar el rectángulo de la casa a la posición correcta
            rectCasa = imgCasa.get_rect(topleft=posc)
            rectCasa = rectCasa.inflate(-rectCasa.width* 0.5 , -rectCasa.height *0.6 )  # Reducir el tamaño del rectángulo
            casasRects.append((infoCasa['id'], rectCasa))
            mapa.blit(imgCasa, posc)
        except Exception as e:
            print(f"Error {e}: {posc}")
    
    #Sonido coin
    sonido = pygame.mixer.Sound('./assets/coin.mp3')
    
    # Gameloop
    running = True
    while running:
            # Guardar la posición anterior del jugador
            pos_anterior = rectHombre.topleft

            velocidad = 5 #Cambiar valor a 1 para tener una mejor jugabilidad
            # Obtener teclas presionadas, movimiento con WASD y flechas
            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_a] or tecla[pygame.K_LEFT]:
                rectHombre.x -= velocidad
            if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
                rectHombre.x += velocidad
            if tecla[pygame.K_w] or tecla[pygame.K_UP]:
                rectHombre.y -= velocidad
            if tecla[pygame.K_s] or tecla[pygame.K_DOWN]:
                rectHombre.y += velocidad

            # Limitar la posición del jugador al tamaño del mapa
            rectHombre.clamp_ip(mapa.get_rect())

            # Detectar colisiones con casas
            for rectCasa in casasRects:
                if rectHombre.colliderect(rectCasa[1]):
                    rectHombre.topleft = pos_anterior  # Revertir el movimiento
                    break

            # Calcular la posición de la cámara para centrar al jugador
            camX = rectHombre.x - ANCHO_VENTANA // 2
            camY = rectHombre.y - ALTO_VENTANA // 2

            # Asegurarse de que la cámara no se salga del mapa
            camX = max(0, min(camX, ANCHO_MAPA - ANCHO_VENTANA))
            camY = max(0, min(camY, ALTO_MAPA - ALTO_VENTANA))

            # Dibujar el fondo del mapa
            vtnJuego.fill((0, 0, 0))  # Rellenar el fondo de la ventana

            # Dibujar la parte visible del mapa en la ventana
            vtnJuego.blit(mapa, (0, 0), (camX, camY, ANCHO_VENTANA, ALTO_VENTANA))

            # Mostrar coordenadas del jugador
            coordenadasTexto = f'X: {rectHombre.x}, Y: {rectHombre.y}'
            textoSuperficie = fuente.render(coordenadasTexto, True, (255, 255, 255))
            vtnJuego.blit(textoSuperficie, (10, 10))

            #Puntaje jugador.
            puntajeJugador = f'Puntaje: {consanginidad.puntaje_judador}'
            textoSuperficie = fuente.render(puntajeJugador, True, (255, 255, 255))
            vtnJuego.blit(textoSuperficie, (10, 35))

            # Dibujar al jugador
            vtnJuego.blit(imgHombre, (rectHombre.x - camX, rectHombre.y - camY))

            pygame.display.update()  # Actualizar cambios en la pantalla
            clock.tick(60)  # Limitar los FPS a 60
            
            # Loop para mantener la ventana abierta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Evento para cerrar la ventana
                    running = False
                #Evento al tocar la casa
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Detectar clic del botón izquierdo del mouse
                    mouse_pos = pygame.mouse.get_pos()
                    # Ajustar la posición del mouse a la posición de la cámara
                    mouse_map_pos = (mouse_pos[0] + camX, mouse_pos[1] + camY)
                    for i, rectCasa in enumerate(casasRects):
                        if rectCasa[1].collidepoint(mouse_map_pos):
                            habitantes = consultarPersonasCasa(rectCasa[0])
                            
                            #Imprimir habitantes
                            print(f'\nCasa {rectCasa[0]}')
                            if habitantes != False:
                                for habitante in habitantes:
                                    esFamilia = consanginidad.comprobarConsanginidad(habitante.id)
                                    
                                    if esFamilia:
                                        sonido.play()
                                    
                                    print(f"{habitante.nombre} : {esFamilia}")
                                break

    pygame.quit()  # Salir de pygame correctamente
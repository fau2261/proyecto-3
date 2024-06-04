import pygame
from apiConsultas import consultarCasasMapa

def iniciarJuego():
    # Inicializar pygame
    pygame.init()

    # Crear la ventana
    ANCHO_VENTANA = 800
    ALTO_VENTANA = 800
    vtnJuego = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

    # Definir título e ícono
    pygame.display.set_caption("GeneaCity")  # Título

    icon = pygame.image.load("assets/icono.png")  # Cargando imagen
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

    # Colocar varias casas en el mapa
    poscionCasas = consultarCasasMapa()
    casasRects = []

    cantError = 0

    for posc in poscionCasas:
        try:
            rectCasa = imgCasa.get_rect(center=posc)
            casasRects.append(rectCasa)
            mapa.blit(imgCasa, posc)
        except Exception as e:
            print(f"Error {e}: {posc}")
            cantError += 1

    # Gameloop
    running = True
    while running:
        try:
            # Loop para mantener la ventana abierta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Evento para cerrar la ventana
                    running = False
                elif event.type == pygame.KEYDOWN:  # Evento por presionar una tecla (con flechas)
                    if event.key in [pygame.K_UP]:
                        rectHombre.y -= 10
                    elif event.key in [pygame.K_DOWN]:
                        rectHombre.y += 10
                    elif event.key in [pygame.K_LEFT]:
                        rectHombre.x -= 10
                    elif event.key in [pygame.K_RIGHT]:
                        rectHombre.x += 10

            tecla = pygame.key.get_pressed() # Obtener teclas presionadas, movimiento con WASD de los jugadores
            if tecla[pygame.K_a]:
                rectHombre.x -= 3
            if tecla[pygame.K_d]:
                rectHombre.x += 3
            if tecla[pygame.K_w]:
                rectHombre.y -= 3
            if tecla[pygame.K_s]:
                rectHombre.y += 3

            # Limitar la posición del jugador al tamaño del mapa
            rectHombre.clamp_ip(mapa.get_rect())

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

            # Dibujar al jugador
            vtnJuego.blit(imgHombre, (rectHombre.x - camX, rectHombre.y - camY))

            pygame.display.update()  # Actualizar cambios en la pantalla
            clock.tick(60)  # Limitar los FPS a 60


        except Exception as e:
            print(f'Ocurrió un error: {e}')
            print(f'Jugador coordenadas: X: {rectHombre.x}, Y: {rectHombre.y}')
            print(f'Camara coordenadas: camX: {camX}, camY: {camY}')
            running = False

    pygame.quit()  # Salir de pygame correctamente
    
iniciarJuego() # Llamar a la función para iniciar el juego

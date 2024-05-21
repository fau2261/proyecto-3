import pygame

def iniciarJuego():
    #Inicializar pygame
    pygame.init()

    #Crear la ventana
    vtnJuego = pygame.display.set_mode((800, 800))

    #Definir título e ícono
    pygame.display.set_caption("GeneaCity") #Título

    icon = pygame.image.load("assets/img/icono.png") #Cargando imagen
    pygame.display.set_icon(icon) #Asignando título

    #Jugador
    jugadorImg = pygame.image.load("assets\img\hombre2.png")
    jugadorImg = pygame.transform.scale(jugadorImg, (50, 50))
    jugadorX = 400
    jugadorY = 400

    def jugador():
        vtnJuego.blit(jugadorImg, (jugadorX, jugadorY))

    #Gameloop
    running = True
    while running:
        #Cambiar color de la ventana
        vtnJuego.fill((197, 216, 109)) #RGB

        #Loop para mantener la ventana abierta
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Evento para cerra la ventana
                running == False
            elif event.type == pygame.KEYDOWN: #Evento por presionar una tecla
                if event.key in [pygame.K_UP, pygame.K_w]:
                    jugadorY -= 10
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    jugadorY += 10
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    jugadorX -= 10
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    jugadorX += 10

        jugador()
        pygame.display.update() #Actualizar cambios en la pantalla
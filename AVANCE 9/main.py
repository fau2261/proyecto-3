import pygame
import geneacity
import json
import impresionArbol

def main():
    global vtnMenu, font
    pygame.init()

    vtnMenu = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("GeneaCity Menu")

    # Cargar una fuente de texto que parezca de juego retro
    font = pygame.font.Font("assets/retro_font.ttf", 36)

    class Botones:
        def __init__(self, x, y, width, height, text):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.color = (255, 140, 0)  # Color naranja
            self.hover_color = (255, 165, 0)  # Color naranja más claro al pasar el mouse
            self.clicked_color = (255, 110, 0)  # Color naranja más oscuro cuando se hace clic
            self.text_color = (255, 255, 255)  # Color del texto blanco
            self.font = font
            self.clicked = False
            self.padding = 20

        def draw(self):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                pygame.draw.rect(vtnMenu, self.hover_color, (self.x, self.y, self.width, self.height), border_radius=15)
                pygame.draw.rect(vtnMenu, (255, 255, 255), (self.x, self.y, self.width, self.height), 4, border_radius=15)

                if click[0] == 1:
                    self.clicked = True
            else:
                self.clicked = False
                pygame.draw.rect(vtnMenu, self.color, (self.x, self.y, self.width, self.height), border_radius=15)
                pygame.draw.rect(vtnMenu, (255, 255, 255), (self.x, self.y, self.width, self.height), 4, border_radius=15)

            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            text_rect.x = self.x + (self.width - text_rect.width) / 2
            text_rect.y = self.y + (self.height - text_rect.height) / 2
            vtnMenu.blit(text_surf, text_rect)

            return self.clicked

    btnContinuarPartida = Botones(200, 250, 400, 70, "Continuar Partida")
    btnArbolPartida = Botones(580, 600, 200, 70, "Árbol")
    btnCrearPartida = Botones(200, 350, 400, 70, "Crear Partida")
    btnHistorialPartidas = Botones(200, 450, 400, 70, "Historial de Partidas")

    running = True
    while running:
        vtnMenu.fill((202, 228, 241))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if btnCrearPartida.draw():
            # Lógica para crear una nueva partida
            running = False
            print("Crear Partida")
            geneacity.crearNuevaPartida()

        if btnContinuarPartida.draw():
            # Lógica para continuar una partida guardada
            running = False
            print("Continuar Partida")
            geneacity.iniciarJuego()

        if btnHistorialPartidas.draw():
            # Lógica para ver el historial de partidas
            print("Historial de Partidas")
            mostrarHistorial()

        if btnArbolPartida.draw():
            # Lógica para ver el historial de partidas
            print("Árbol juego")
            impresionArbol.mostrarArbol()
            

        pygame.display.update()

def dividirTexto(texto, ancho_max):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if font.size(linea_actual + palabra)[0] <= ancho_max:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "

    if linea_actual:
        lineas.append(linea_actual.strip())

    return lineas

def mostrarHistorial():
    try:
        with open('./archivosJuego/historial.txt', 'r') as archivo:
            partidas = json.load(archivo)
            # Limpia la pantalla
            vtnMenu.fill((202, 228, 241))
            # Muestra el título
            titulo_surf = font.render("Historial de Partidas:", True, (255, 255, 255))
            titulo_rect = titulo_surf.get_rect(center=(400, 100))
            vtnMenu.blit(titulo_surf, titulo_rect)
            # Muestra cada partida
            y_offset = 150
            for partida in partidas:
                info_partida = f"ID: {partida['id']}, Puntaje: {partida['puntaje']}, Habitantes Encontrados: {partida['habitantesEncontrados']}"
                lineas = dividirTexto(info_partida, 750)  # Ajusta el ancho máximo según el tamaño de la ventana
                for linea in lineas:
                    info_surf = font.render(linea, True, (0, 23, 108))
                    info_rect = info_surf.get_rect(center=(400, y_offset))
                    vtnMenu.blit(info_surf, info_rect)
                    y_offset += 40
    except FileNotFoundError:
        print("No se encontró el archivo del historial de partidas.")

if __name__ == "__main__":
    main()

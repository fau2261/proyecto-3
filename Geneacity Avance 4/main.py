import pygame
import geneacity

def main():
    pygame.init()

    vtnMenu = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("GeneaCity Menu")
    imgBtn1 = pygame.image.load("assets/btn1.png").convert_alpha()
    imgBtn2 = pygame.image.load("assets/btn2.png").convert_alpha()

    class Botones:
        def __init__(self, x, y, image, tamano):
            ancho = image.get_width()
            alto = image.get_height()
            self.image = pygame.transform.scale(image, (int(ancho * tamano), int(alto * tamano)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.click = False

        def draw(self):
            distinguirBtn = False
            posicionMouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(posicionMouse):
                if pygame.mouse.get_pressed()[0] == 1 and not self.click:
                    self.click = True
                    distinguirBtn = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False
            vtnMenu.blit(self.image, (self.rect.x, self.rect.y))
            return distinguirBtn

    btnInicio = Botones(250, 300, imgBtn1, 0.8)
    btnSalida = Botones(275, 500, imgBtn2, 0.8)

    running = True
    while running:
        vtnMenu.fill((202, 228, 241))

        if btnInicio.draw():
            geneacity.iniciarJuego()  
            running = False
            print("Iniciar Juego")

        if btnSalida.draw():
            running = False
            print("Exit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        pygame.display.update()

if __name__ == "__main__":
    main()  

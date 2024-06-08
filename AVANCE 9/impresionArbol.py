import pygame
import sys
import math
import main
import json
from claseArbol import Arbol
from apiConsultas import encontrarObjetoPersona, consultarCasasMapa
from persona import personas

def mostrarArbol():
    Verde=(0,255,0)
    Rojo=(255,0,0) 
    Azul=(0,0,255)

    def llenadoarbol():
        with open('./archivosJuego/infoJuego.json', 'r') as archivo:
            # Cargar el contenido del archivo JSON en un diccionario
            datosJuego = json.load(archivo)
        
        if len(personas) == 0:
            consultarCasasMapa()
        
        idEncontrados = datosJuego["habitantesEncontrados"]
        idEncontrados.reverse()
        idEncontrados.append(datosJuego['id'])

        for i, idEncontrado in enumerate(idEncontrados):
            persona = encontrarObjetoPersona(idEncontrado)
            if i == 0:
                miarbol = Arbol(persona.nombre, persona.edad)
            else:
                print(miarbol(persona.nombre, persona.edad))

        return miarbol
        

        """while True:
            valor=input("Indique el valor o cualquier letra para deternerse:   ")
            if c==0:
                miarbol=Arbol(int(valor))
                c=1
            else:
                if valor.isdigit():
                    print(miarbol(int(valor)))
                else:
                    print("Fin del árbol")
                    return miarbol
"""
    miarbol=llenadoarbol()

    #Inicio Pygame
    pygame.init()
    pantalla = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Árbol Genealógico")
    pantalla.fill((233, 150, 122))

    def impresion(clase,lado,x,n):
        pygame.draw.circle(pantalla, Verde, (x, n), 20)
        fuente = pygame.font.Font(None, 20)
        Nodo= clase.Nombre
        Nodo = fuente.render(str(clase.Nombre), True, (205, 92, 92))
        texto = Nodo.get_rect()
        texto.center = (x, n)
        pantalla.blit(Nodo,texto)

        if lado=="L" or lado=="RL": 
            pygame.draw.line(pantalla,(205, 92, 92),(x,(n+20)),(x-80,(n+60)),5)
        if lado=="R" or lado=="RL":
            pygame.draw.line(pantalla,(205, 92, 92),(x,(n+20)),(x+80,(n+60)),5)
            
    def impresionarbol(clase,lado,x,y):
        if clase != None:  
            if clase.Left != None and clase.Right != None: 
                impresion(clase,"RL", x,y)
            elif clase.Left != None:
                print(f"Nodo a la izquierda, {clase.Nombre} {x}  {y}  {lado}")
                impresion(clase,"L",x,y)
            elif clase.Right != None:
                print(f"Nodo a la derecha, {clase.Nombre} {x} {y} {lado}")
                impresion(clase,"R",x,y)
            else:
                impresion(clase,"NA",x,y)
                
            impresionarbol(clase.Left,lado,x-80,y+50)
            impresionarbol(clase.Right,lado,x+80,y+50)

    #Configuración para pintar la raíz del árbol
    impresionarbol(miarbol,"RL", x=600,y=50)
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                main.main()
                #sys.exit()

        pygame.display.update()


from typing import Any

class Arbol:
    
    def __init__(self, nombre: str, edad: int, left=None, right=None) -> None:
        self.Nombre = nombre
        self.Edad = edad
        self.Left = left
        self.Right = right
    
    def __call__(self, nombre: str, edad: int) -> Any:
        if self.Nombre == nombre or self.Nombre == None:
            return "Dato ya existe"
        else:
            self.__append__(self, nombre, edad)
            return "Dato agregado"
      
    def __append__(self, clase, nombre: str, edad: int):
        while True:
            if clase.Nombre > nombre and clase.Nombre != nombre:
                if clase.Left == None:
                    clase.Left = Arbol(nombre, edad)
                    break
                else:
                    clase = clase.Left
            elif clase.Nombre != nombre:
                if clase.Right == None:
                    clase.Right = Arbol(nombre, edad)
                    break
                else:
                    clase = clase.Right
            else:
                break

    def inorden(self):
        self.__inorden__(self)
        
    def __inorden__(self, clase):
        if clase != None:
            self.__inorden__(clase.Left)
            print(f"Nombre: {clase.Nombre}, Edad: {clase.Edad}")
            self.__inorden__(clase.Right)
    
    def preorden(self):
        self.__preorden__(self)
    
    def __preorden__(self, clase):
        if clase != None:
            print(f"Nombre: {clase.Nombre}, Edad: {clase.Edad}")
            self.__preorden__(clase.Left)
            self.__preorden__(clase.Right)
    
    def impresion(self, orden):
        self.__impresion__(self, orden)
        return orden
    
    def __impresion__(self, clase, orden):
        if clase != None:
            print(f"Nombre: {clase.Nombre}, Edad: {clase.Edad}")
            orden.append((clase.Nombre, clase.Edad))
            self.__impresion__(clase.Left, orden)
            orden.append("Cambio")
            self.__impresion__(clase.Right, orden)
        return orden
    
    def posorden(self):
        self.__posorden__(self)
    
    def __posorden__(self, clase):
        if clase is None:
            return
        self.__posorden__(clase.Left)
        self.__posorden__(clase.Right)
        print(f"Nombre: {clase.Nombre}, Edad: {clase.Edad}")

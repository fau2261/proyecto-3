personas = []

class Persona():
    def __init__(self, id, nombre, genero, estadoMarital, padre, madre, edad) -> None:
        self.id = id
        self.nombre = nombre
        self.genero = genero
        self.estadoMarital = estadoMarital
        self.padre = padre
        self.madre = madre
        self.edad = edad
        
        personas.append(self)

    def informacion(self):
        print("---------------------------------------------")
        print(self.id)
        print(self.nombre)
        print(self.genero)
        print(self.estadoMarital)
        print(self.padre)
        print(self.madre)
        print(self.edad)
        print("---------------------------------------------")
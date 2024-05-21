import tkinter as tk
import geneacity 

def onClickBtnCrearJuego():
    vtnMenu.destroy()
    geneacity.iniciarJuego()

def onClickbtnContinuarJuego():
    print("Continuar juego")

def onClickBtnVerHistorial():
    print("Ver historial")

def main():
    global vtnMenu

    #Ventana menú
    vtnMenu = tk.Tk()
    vtnMenu.title("GeneaCity")
    vtnMenu.geometry("800x800")
    vtnMenu.resizable(False, False)
    vtnMenu.configure(background="#669bbc")

    #Botón crear juego
    btnCrearJuego = tk.Button(vtnMenu)
    btnCrearJuego.configure(text="Nuevo juego", width=20, height=2, font=("Helvetica", 11, "bold"), fg="white", bg="#0077b6", command=onClickBtnCrearJuego)
    btnCrearJuego.pack()

    #Botón cargar juego
    btnContinuarJuego = tk.Button(vtnMenu)
    btnContinuarJuego.configure(text="Continuar juego", width=20, height=2, font=("Helvetica", 11, "bold"), fg="white", bg="#0077b6", command=onClickbtnContinuarJuego)
    btnContinuarJuego.pack()

    #Boton ver historial
    btnVerHistorial = tk.Button(vtnMenu)
    btnVerHistorial.configure(text="Ver historial", width=20, height=2, font=("Helvetica", 11, "bold"), fg="white", bg="#0077b6", command=onClickBtnVerHistorial)
    btnVerHistorial.pack()

    vtnMenu.mainloop()


if __name__ == "__main__":
    main()
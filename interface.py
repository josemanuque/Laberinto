import tkinter as tk
from tkinter import filedialog
from tkinter import *
from pyswip import Prolog

# Variables globales
prolog = Prolog() # Instancia de prolog
path = ""


def obtenerArchivo(btnStart):
    path = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Prolog files","*.pro"),("Prolog files","*.pl")))
    if len(path) != 0: 
        btnStart.config(state=NORMAL) # Habilita el boton de iniciar juego
    return

def setTheme(ventana):
    ventana.tk.call("source", "tktheme/azure.tcl")
    ventana.tk.call("set_theme", "dark")
    return

# Funcion que crea la ventana de inicio
def showVentanaInicio():
    ventanaInicio = tk.Tk()
    ancho = 800
    alto = 600
    ventanaInicio.title("Inicio")
    ventanaInicio.geometry(f"{ancho}x{alto}") # Tamaño de la ventana
    # Theme
    setTheme(ventanaInicio)
    # Label
    lblTitulo = Label(ventanaInicio, text="Laberinto", font=('Helvetica', 16, 'bold'))
    lblTitulo.place(x=ancho/2, y=(alto-200)/2, anchor=CENTER) # Posicion del label

    # Botones
    btnStart = Button(ventanaInicio, text="Iniciar Juego", command=obtenerArchivo, state=DISABLED) # Comando del boton
    btnStart.place(x=ancho/2, y=(alto)/2, anchor=CENTER) # Posicion del boton
    btnCargar = Button(ventanaInicio, text="Cargar archivo", command=lambda: obtenerArchivo(btnStart)) # Comando del boton
    btnCargar.place(x=ancho/2, y=(alto-100)/2, anchor=CENTER) # Posicion del boton
    ventanaInicio.mainloop()
    return



# Main
if __name__ == "__main__":
    showVentanaInicio()

    
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from pyswip import Prolog

# Variables globales
prolog = Prolog() # Instancia de prolog
prolog.consult("logic.pro")
path = "test.txt"
matriz = []

def obtenerArchivo(btnStart):
    global path
    #path = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Maze files","*.txt"),("All Files","*.*")))
    query = prolog.query(f"creaMatriz('{path}', X).") # Consulta el archivo de prolog
    guardarMatriz(query) # Guarda la matriz en un una lista de listas
 
    if len(path) != 0: 
        btnStart.config(state=NORMAL) # Habilita el boton de iniciar juego
    return

def guardarMatriz(query):
    global matriz
    matriz = list(query)[0].get("X")
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            matriz[fila][columna] = matriz[fila][columna].decode("utf-8")
    print(matriz)
    return matriz


def setTheme(ventana):
    ventana.tk.call("source", "tktheme/azure.tcl")
    ventana.tk.call("set_theme", "dark")
    return

def showVentanaJuego():
    ventanaJuego = tk.Tk()
    ancho = 600
    alto = 400
    ventanaJuego.title("Juego")
    ventanaJuego.geometry(f"{ancho}x{alto}") # Tamaño de la ventana
    # Theme
    setTheme(ventanaJuego)
    # Label
    lblTitulo = Label(ventanaJuego, text="Laberinto", font=('Helvetica', 16, 'bold'))
    lblTitulo.place(x=ancho/2, y=(alto-200)/2, anchor=CENTER) # Posicion del label
    ventanaJuego.mainloop()
    return


def iniciarJuego(ventanaInicio):
    ventanaInicio.destroy()
    showVentanaJuego()
    return

# Funcion que crea la ventana de inicio
def showVentanaInicio():
    ventanaInicio = tk.Tk()
    ancho = 600
    alto = 400
    ventanaInicio.title("Inicio")
    ventanaInicio.geometry(f"{ancho}x{alto}") # Tamaño de la ventana
    # Theme
    setTheme(ventanaInicio)
    # Label
    lblTitulo = Label(ventanaInicio, text="Laberinto", font=('Helvetica', 16, 'bold'))
    lblTitulo.place(x=ancho/2, y=(alto-200)/2, anchor=CENTER) # Posicion del label

    # Botones
    btnStart = Button(ventanaInicio, text="Iniciar Juego", command=lambda: iniciarJuego(ventanaInicio), state=DISABLED) # Comando del boton
    btnStart.place(x=ancho/2, y=(alto)/2, anchor=CENTER) # Posicion del boton
    btnCargar = Button(ventanaInicio, text="Cargar archivo", command=lambda: obtenerArchivo(btnStart)) # Comando del boton
    btnCargar.place(x=ancho/2, y=(alto-100)/2, anchor=CENTER) # Posicion del boton
    ventanaInicio.mainloop()
    return



# Main
if __name__ == "__main__":
    showVentanaInicio()

    
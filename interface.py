import tkinter as tk
import pygame as p
from tkinter import filedialog
from tkinter import *
from pyswip import Prolog

# Variables globales
prolog = Prolog() # Instancia de prolog
prolog.consult("logic.pro")
path = "matriz.txt"
matriz = []

def obtenerArchivo(btnStart):
    global path
    #path = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Maze files","*.txt"),("All Files","*.*")))
    query = prolog.query(f"creaMatriz('{path}', Matriz).") # Consulta el archivo de prolog
    guardarMatriz(query) # Guarda la matriz en un una lista de listas
 
    if len(path) != 0: 
        btnStart.config(state=NORMAL) # Habilita el boton de iniciar juego
    return

def guardarMatriz(query):
    global matriz
    matriz = list(query)[0].get("Matriz") # Convierte clase generator a lista y obtiene el valor la llave X del diccionario
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            matriz[fila][columna] = matriz[fila][columna].decode("utf-8")
    print(matriz)
    return matriz


def pintarMatriz(ventanaJuego):
    global matriz
    ancho = 1000
    alto = 800
    tamanoCelda = 50
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == "x":
                p.draw.rect(ventanaJuego, (255, 255, 255), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                """
                elif matriz[fila][columna] == "0":
                    p.draw.rect(ventanaJuego, (0, 0, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                elif matriz[fila][columna] == "S":
                    p.draw.rect(ventanaJuego, (0, 255, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                elif matriz[fila][columna] == "E":
                    p.draw.rect(ventanaJuego, (255, 0, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                """
            else:
                p.draw.rect(ventanaJuego, (0, 51, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
    return


def setTheme(ventana):
    ventana.tk.call("source", "tktheme/azure.tcl")
    ventana.tk.call("set_theme", "dark")
    return

def showVentanaJuego():
    p.init()
    ancho = 1000
    alto = 800
    ventanaJuego = p.display.set_mode((ancho, alto)) # Tamaño de la ventana
    p.display.set_caption("Laberinto") # Titulo de la ventana
    ventanaJuego.fill((0, 0, 0)) # Color de fondo
    pintarMatriz(ventanaJuego) # Pinta la matriz en la ventana
    p.display.flip() # Actualiza la ventana
    
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return

                
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

    
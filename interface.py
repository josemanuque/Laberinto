import tkinter as tk
import pygame as p
import time
from tkinter import filedialog
from tkinter import *
from pyswip import Prolog

# Variables globales
prolog = Prolog() # Instancia de prolog
prolog.consult("logic.pro")
path = "matriz.txt"
matriz = []
ficha = {
    "x" : 0,
    "y" : 0,
    "movimientos" : 0,
    "tiempoInicio" : 0
}

btnSolucion = p.Rect(600,150,150,30) #boton ver solucion
btnSugerencia = p.Rect(600,200,150,30) #boton ver sugerencia
btnVolver = p.Rect(600,250,150,30) #boton ver volver
btnReinicar = p.Rect(600,300,150,30) #boton ver reiniciar



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
            elif matriz[fila][columna] == "i":
                p.draw.rect(ventanaJuego, (0, 200, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.Font(None, 15)
                text = font.render("i", True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)

            elif fila == ficha['y'] and columna == ficha['x']:
                p.draw.rect(ventanaJuego, (0, 0, 255), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.Font(None, 15)
                text = font.render("P", True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)

            elif matriz[fila][columna] == "f":
                p.draw.rect(ventanaJuego, (0, 200, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.Font(None, 15)
                text = font.render("f", True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)

            else:
                p.draw.rect(ventanaJuego, (0, 51, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.Font(None, 15)
                text = font.render(matriz[fila][columna], True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)
    return


def setTheme(ventana):
    ventana.tk.call("source", "tktheme/azure.tcl")
    ventana.tk.call("set_theme", "dark")
    return

def setFicha():
    global ficha
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == "i":
                ficha['x'] = columna
                ficha['y'] = fila
                ficha['tiempoInicio'] = time.time()
                return
    return


#Acomoda la etiqueta al botón
def acomodarLabel(ventanaJuego,label,btn):

    ventanaJuego.blit(label,(btn.x+(btn.width - label.get_width())/2, 
                            btn.y+(btn.height - label.get_height())/2) )

    return 


def showVentanaJuego():
    p.init()
    ancho = 800
    alto = 600

    btnfont = p.font.Font(None,32)

    ventanaJuego = p.display.set_mode((ancho, alto)) # Tamaño de la ventana
    p.display.set_caption("Laberinto") # Titulo de la ventana
    ventanaJuego.fill((0, 0, 0)) # Color de fondo
    setFicha()
    pintarMatriz(ventanaJuego) # Pinta la matriz en la ventana
    mostrarSolucion(ventanaJuego)
   
    #Colocando los botones en la ventana del juego
    p.draw.rect(ventanaJuego,(100,100,100),btnSugerencia,0)
    p.draw.rect(ventanaJuego,(100,100,100),btnSolucion,0)
    p.draw.rect(ventanaJuego,(100,100,100),btnReinicar,0)
    p.draw.rect(ventanaJuego,(100,100,100),btnVolver,0)


    btnSolucionLabel = btnfont.render("Sugerencia", True, (0,50,0))
    btnSugerenciaLabel = btnfont.render("Ver solución", True, (0,50,0))
    btnReiniciarLabel = btnfont.render("Reiniciar", True, (0,50,0))
    btnVolverLabel = btnfont.render("Volver", True, (0,50,0))
    
    acomodarLabel(ventanaJuego,btnSolucionLabel,btnSolucion)
    acomodarLabel(ventanaJuego,btnSugerenciaLabel,btnSugerencia)
    acomodarLabel(ventanaJuego,btnReiniciarLabel,btnReinicar)
    acomodarLabel(ventanaJuego,btnVolverLabel,btnVolver)


    teclas(ventanaJuego) # Espera una tecla para moverse
    p.display.flip() # Actualiza la ventana
    
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return  
    return

def obtenerSolucion():
    global matriz
    print(f"solucionarLaberinto({matriz}, ListaSolucion)")
    query = prolog.query(f"solucionarLaberinto({matriz}, ListaSolucion)")
    lista = list(query)
    if len(lista) == 0:
        print("No hay solucion")
        return
    elif len(lista) > 0:
        print("Hay mas de una solucion, se uniran ambas")
        listaPreparada = []
        for solucion in range(len(lista)):
            for elemento in range(len(lista[solucion]['ListaSolucion'])):
                if (lista[solucion]['ListaSolucion'][elemento] not in listaPreparada):
                    listaPreparada.append(lista[solucion]['ListaSolucion'][elemento])
        print(listaPreparada)
        return listaPreparada

def mostrarSolucion(ventanaJuego):
    global matriz
    lista = obtenerSolucion()
    ancho = 1000
    alto = 800
    tamanoCelda = 50
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            for l in range(len(lista)):
                if lista[l] == [fila, columna]:
                    p.draw.rect(ventanaJuego, (0, 255, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                    font = p.font.Font(None, 18)
                    text = font.render("Sol", True, (0, 0, 0)) # Texto, antialias, color
                    text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                    ventanaJuego.blit(text, text_rect)
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

def teclas(ventanaJuego):
    loop = True
    while loop:
        for event in p.event.get():
            if event.type == p.QUIT:
                loop = False
                p.quit()
                showVentanaInicio()
                
            if event.type == p.KEYDOWN:
                keys = p.key.get_pressed()
                if keys[p.K_LEFT]:
                    cambiarPosicion("izquierda", ventanaJuego)
                elif keys[p.K_RIGHT]:
                    cambiarPosicion("derecha", ventanaJuego)
                elif keys[p.K_UP]:
                    cambiarPosicion("arriba", ventanaJuego)
                elif keys[p.K_DOWN]:
                    cambiarPosicion("abajo", ventanaJuego)
            
            elif event.type == p.MOUSEBUTTONDOWN:
                if btnSolucion.collidepoint(p.mouse.get_pos()):
                    print("ver solucion")
                if btnSugerencia.collidepoint(p.mouse.get_pos()):
                    print("Sugerencia")
                if btnReinicar.collidepoint(p.mouse.get_pos()):
                    print("Reiniciar")
                if btnVolver.collidepoint(p.mouse.get_pos()):
                    print("Volver")
                    p.quit()
                    showVentanaInicio()

        p.display.update()
        
#Mover ficha de la matriz
def cambiarPosicion(direccion, ventanaJuego):
    global matriz
    global ficha
    
    if direccion == "izquierda":
        posicionSiguiente = { "X": ficha["x"] - 1, "Y": ficha["y"] }
    elif direccion == "derecha":
        posicionSiguiente = { "X": ficha["x"] + 1, "Y": ficha["y"] }
    elif direccion == "arriba":
        posicionSiguiente = { "X": ficha["x"], "Y": ficha["y"] - 1 }
    elif direccion == "abajo":
        posicionSiguiente = { "X": ficha["x"], "Y": ficha["y"] + 1 }

    if esPosicionValida(posicionSiguiente, direccion):
        ficha["x"] = posicionSiguiente["X"]
        ficha["y"] = posicionSiguiente["Y"]
        ficha["tiempoInicio"] = time.time()
        pintarMatriz(ventanaJuego) # Pinta la matriz en la ventana

def esPosicionValida(posicionSiguiente, direccion):
    global matriz
    print(f"movimientoValido({matriz[ficha['y']][ficha['x']]}, {direccion}, {matriz[posicionSiguiente['Y']][posicionSiguiente['X']]})")
    if not (posicionSiguiente["X"] >= 0 and posicionSiguiente["X"] < len(matriz) and posicionSiguiente["Y"] >= 0 and posicionSiguiente["Y"] < len(matriz[0])):
        return False
    if bool(list(prolog.query(f"movimientoValido({matriz[ficha['y']][ficha['x']]}, {direccion}, {matriz[posicionSiguiente['Y']][posicionSiguiente['X']]})"))) == False:
        return False
    return True
        

# Main
if __name__ == "__main__":
    showVentanaInicio()

    
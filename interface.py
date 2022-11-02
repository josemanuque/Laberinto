import tkinter as tk
import pygame as p
import time
from tkinter import *
from tkinter import messagebox
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

# Botones para pygame
btnSugerencia = p.Rect(600,150,150,30) #boton ver solucion
btnSolucion = p.Rect(600,200,150,30) #boton ver sugerencia
btnVerificar = p.Rect(600,100,150,30) #boton reiniciar
btnReinicar = p.Rect(600,250,150,30) #boton ver reiniciar
btnVolver = p.Rect(600,300,150,30) #boton ver volver

nickname = ""
tipoFinal = ""


""" 
ObtenerArchivo
Entrada: btnStart.
Salida: matriz.
Funcionamiento: Obtiene la matriz del archivo txt.
"""
def obtenerArchivo(btnStart):
    global path
    #path = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Maze files","*.txt"),("All Files","*.*")))
    query = prolog.query(f"creaMatriz('{path}', Matriz).") # Consulta el archivo de prolog
    guardarMatriz(query) # Guarda la matriz en un una lista de listas
 
    if len(path) != 0: 
        btnStart.config(state=NORMAL) # Habilita el boton de iniciar juego
    return
""" 
GuardarMatriz
Entrada: query.
Salida: matriz.
Funcionamiento: Guarda la matriz en una lista de listas.
"""
def guardarMatriz(query):
    global matriz
    matriz = list(query)[0].get("Matriz") # Convierte clase generator a lista y obtiene el valor la llave X del diccionario
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            matriz[fila][columna] = matriz[fila][columna].decode("utf-8")
    #print(matriz)
    return matriz

""" 
PintarMatriz
Entrada: ventanaJuego.
Salida: ninguna.
Funcionamiento: Pinta la matriz en la ventana de juego.
"""
def pintarMatriz(ventanaJuego):
    global matriz
    ancho = 1000
    alto = 800
    tamanoCelda = 50
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == "x":
                p.draw.rect(ventanaJuego, (6, 27, 47), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))

            elif matriz[fila][columna] == "i":
                p.draw.rect(ventanaJuego, (0, 200, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.Font(None, 18)
                text = font.render("Inicio", True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)

            elif fila == ficha['y'] and columna == ficha['x']:
                p.draw.rect(ventanaJuego, (30, 74, 151), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.SysFont("segoeuisymbol", 18)
                text = font.render("★", True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                if( matriz[ficha['y']][ficha["x"]] == "f"):
                    print("Has ganado")
                    estadisticas()

                    # ventanaDatos(ventanaJuego)

                ventanaJuego.blit(text, text_rect)

            elif matriz[fila][columna] == "f":
                p.draw.rect(ventanaJuego, (0, 200, 0), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.SysFont("segoeuisymbol", 18)
                text = font.render("🏁", True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)

            else:
                p.draw.rect(ventanaJuego, (27, 143, 96), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.Font(None, 18)
                text = font.render(matriz[fila][columna], True, (255, 255, 255)) # Texto, antialias, color
                text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)
    return

""" 
SetTheme
Entrada: ventana de TK.
Salida: ninguna.
Funcionamiento: Cambia el tema de la ventana de TK.
"""
def setTheme(ventana):
    ventana.tk.call("source", "tktheme/azure.tcl")
    ventana.tk.call("set_theme", "dark")
    return

""" 
SetFicha
Entrada: ninguna.
Salida: ninguna.
Funcionamiento: Setea la posicion de la ficha en la matriz.
"""
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


""" 
acomodarLabel
Entrada: label, ventana, boton.
Salida: ninguna.
Funcionamiento: Acomoda el label en la ventana.
"""
def acomodarLabel(ventanaJuego,label,btn):

    ventanaJuego.blit(label,(btn.x+(btn.width - label.get_width())/2, 
                            btn.y+(btn.height - label.get_height())/2) )

    return 

""" 
showVentanaJuego
Entrada: ninguna.
Salida: ninguna.
Funcionamiento: Muestra la ventana de juego.
"""
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
    
   
    #Colocando los botones en la ventana del juego
    p.draw.rect(ventanaJuego,(0,51,0),btnSugerencia,0)
    p.draw.rect(ventanaJuego,(0,51,0),btnSolucion,0)
    p.draw.rect(ventanaJuego,(0,51,0),btnReinicar,0)
    p.draw.rect(ventanaJuego,(0,51,0),btnVolver,0)
    p.draw.rect(ventanaJuego,(0,51,0),btnVerificar,0)

    #Colocando labels en los botones
    btnSugerenciaLabel = btnfont.render("Sugerencia", True, (255,255,255))
    btnSolucionLabel = btnfont.render("Ver solución", True, (255,255,255))
    btnReiniciarLabel = btnfont.render("Reiniciar", True, (255,255,255))
    btnVolverLabel = btnfont.render("Volver", True, (255,255,255))
    btnVerificarLabel = btnfont.render("Verificar", True, (255,255,255))
    
    acomodarLabel(ventanaJuego,btnSolucionLabel,btnSolucion)
    acomodarLabel(ventanaJuego,btnSugerenciaLabel,btnSugerencia)
    acomodarLabel(ventanaJuego,btnReiniciarLabel,btnReinicar)
    acomodarLabel(ventanaJuego,btnVolverLabel,btnVolver)
    acomodarLabel(ventanaJuego,btnVerificarLabel,btnVerificar)


    teclas(ventanaJuego) # Espera una tecla para moverse
    p.display.flip() # Actualiza la ventana
    
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return  

""" 
obtenerSolucion
Entrada: elegir si se quiere que la solucion sea unica o que se muestren todas (parametro opcional).
Salida: lista con el camino de la solucion.
Funcionamiento: Obtiene la solucion del laberinto llamando a Prolog.
"""
def obtenerSolucion(solucionUnica = 0):
    global matriz
    #print(f"solucionarLaberinto({matriz}, ListaSolucion)")
    query = prolog.query(f"solucionarLaberinto({matriz}, ListaSolucion)")
    lista = list(query)
    if len(lista) == 0:
        print("No hay solucion")
        return
    elif solucionUnica == 1:
        listaPreparada = []
        for solucion in range(len(lista)):
            listaPreparada += [lista[solucion]['ListaSolucion']]

        listaPreparada = min(listaPreparada, key=len)
        return listaPreparada

    elif len(lista) > 0:
        print("Hay mas de una solucion, se uniran ambas")
        listaPreparada = []
        for solucion in range(len(lista)):
            for elemento in range(len(lista[solucion]['ListaSolucion'])):
                if (lista[solucion]['ListaSolucion'][elemento] not in listaPreparada):
                    listaPreparada.append(lista[solucion]['ListaSolucion'][elemento])
        return listaPreparada

""" 
mostrarSolucion
Entrada: ventanaJuego (Pygame).
Salida: ninguna.
Funcionamiento: Muestra la solucion del laberinto.
"""
def mostrarSolucion(ventanaJuego):
    global matriz
    lista = obtenerSolucion(0)
    ancho = 1000
    alto = 800
    tamanoCelda = 50
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            for l in range(len(lista)):
                if lista[l] == [fila, columna]:
                    p.draw.rect(ventanaJuego, (233, 102, 58), (columna*tamanoCelda, fila*tamanoCelda, tamanoCelda, tamanoCelda))
                    font = p.font.Font(None, 18)
                    text = font.render(matriz[fila][columna], True, (255, 255, 255)) # Texto, antialias, color
                    text_rect = text.get_rect(center=(columna*tamanoCelda + tamanoCelda/2, fila*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                    ventanaJuego.blit(text, text_rect)
    return

""" 
esSolucion
Entrada: ninguna
Salida: booleano.
Funcionamiento: Verifica si la solucion es correcta.
"""
def esSolucion():
    global ficha
    lista = obtenerSolucion()
    for l in range(len(lista)):
        if lista[l] == [ficha['y'], ficha['x']]:
            return True
    return False

""" 
mostrarValidezPosicion
Entrada: ventanaJuego (Pygame).
Salida: ninguna.
Funcionamiento: Muestra si la posicion actual es valida o no. Muestra una ventana con la informacion.
"""
def mostrarValidezPosicion(ventanaJuego):
    global ficha
    #temp = Tk().wm_withdraw() #to hide the main window
    if esSolucion():
        messagebox.showinfo('Posición Válida', 'Está en una posición válida')
    else:
        messagebox.showinfo('Posición No Válida', 'No está en una posición válida')
    return

""" 
distance
Entrada: dos listas con dos elementos.
Salida: distancia entre las dos listas.
Funcionamiento: Calcula la distancia entre dos listas.
"""
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

""" 
mostrarSugerencia
Entrada: ventanaJuego (Pygame).
Salida: ninguna.
Funcionamiento: Muestra la sugerencia de la siguiente posicion a tomar. Dibuja hint en ventana.
"""
def mostrarSugerencia(ventanaJuego):
    tamanoCelda = 50
    lista = obtenerSolucion(1)
    if [ficha["y"], ficha["x"]] not in lista:
        messagebox.showinfo('No Válida', 'No existen sugerencias. Está en una posición no válida')
        return
    for l in range(len(lista)):
        if lista[l] == [ficha["y"], ficha["x"]]:
            if l == 0:
                messagebox.showinfo('Sugerencia', 'Ya está en la posición final')
                return
            else:
                coordenada = lista[l - 1]
                messagebox.showinfo('Sugerencia', f'La siguiente posición válida es ({lista[l-1][0]},{lista[l-1][1]})')
                p.draw.rect(ventanaJuego, (231, 214, 83), (coordenada[1]*tamanoCelda, coordenada[0]*tamanoCelda, tamanoCelda, tamanoCelda))
                font = p.font.SysFont("segoeuisymbol", 18)
                text = font.render("💡", True, (0, 0, 0)) # Texto, antialias, color
                text_rect = text.get_rect(center=(coordenada[1]*tamanoCelda + tamanoCelda/2, coordenada[0]*tamanoCelda + tamanoCelda/2)) # Posicion del texto
                ventanaJuego.blit(text, text_rect)
                return

""" 
ventanaDatos
Entrada: ninguna.
Salida: ninguna.
Funcionamiento: Muestra la ventana de datos. Para pedir Nickname.
"""
#----------------------------------Pedir Nickname
def ventanaDatos(ventanaInicio):
    print("vuelve Paloma")
    ventanaInicio.destroy()
    ventanaDatos = Tk()
    nicknameVar = StringVar()
    ventanaDatos.geometry("250x250")
    ventanaDatos.title("Data Form")
  
    heading = Label(text="Are you ready?", bg = "green", fg = "black", width= "500" ,height=3)
    heading.pack()

    jugador_text = Label(text= "Nickname")
    jugador_text.place(x=10,y=60)

    jugador_entry = Entry(textvariable = nicknameVar, width=30)
    jugador_entry.place(x=110 , y = 60)

    btnStart = Button(ventanaDatos, text="Iniciar Juego",command=lambda: iniciarJuego(ventanaDatos,nicknameVar.get()), bg="grey") # Comando del boton

    btnStart.place(x=250/2, y=(250)/2, anchor=CENTER) # Posicion del boton


#----------------------------------------Mostar estadisticas
""" 
estadisticas
Entrada: ninguna.
Salida: ninguna.
Funcionamiento: Muestra la ventana de estadisticas.
"""
def estadisticas():
    global nickname
    global ficha
    global tipoFinal

    p.quit()
    ventanaEstadisticas = Tk()

    ventanaEstadisticas.geometry("300x300")
    ventanaEstadisticas.title("Estadisticas")
  
    heading = Label(text="Resumen de partida.", bg = "gray", fg = "black", width= "500" ,height=3)
    heading.pack()

    jugador_text = Label(text= "Jugador: ")
    jugador_text.place(x=10,y=60)
    jugador_text2 = Label(text= " "+ nickname + " " , borderwidth=1, relief="solid")
    jugador_text2.place(x=65,y=60)



    movimientos_text = Label(text= "Movimientos realizados: ")
    movimientos_text.place(x=10,y=120)
    movimientos_text2 = Label(text= " " + str(ficha["movimientos"]) + " ", borderwidth=1, relief="solid")
    movimientos_text2.place(x=147,y=120)

    tipoFinalizacion_text = Label(text= "Finalización: ")
    tipoFinalizacion_text.place(x=10,y=180)
    tipoFinalizacion_text2 = Label(text= " "+ tipoFinal + " " , borderwidth=1, relief="solid")
    tipoFinalizacion_text2.place(x=85,y=180)

  

    # btnStart = Button(ventanaDatos, text="Iniciar Juego",command=lambda: iniciarJuego(ventanaEstadisticas,nicknameVar.get()), bg="grey") # Comando del boton

    # btnStart.place(x=250/2, y=(250)/2, anchor=CENTER) # Posicion del boton



""" 
iniciarJuego
Entrada: ventanaDatos (Tk), nickname (String).
Salida: ninguna.
Funcionamiento: Inicia el juego. Cierra ventanaDatos y abre ventanaJuego.
"""
def iniciarJuego(ventanaDatos,nick):
    global nickname
    ventanaDatos.destroy()
    nickname = nick
    
    showVentanaJuego()
    return


# Funcion que crea la ventana de inicio
""" 
showVentanaInicio
Entrada: ninguna.
Salida: ninguna.
Funcionamiento: Muestra la ventana de inicio.
"""
def showVentanaInicio():
    global nickname
    global ficha

    print(nickname,  ficha["movimientos"])
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
    btnStart = Button(ventanaInicio, text="Iniciar Juego", command=lambda: ventanaDatos(ventanaInicio), state=DISABLED) # Comando del boton
    btnStart.place(x=ancho/2, y=(alto)/2, anchor=CENTER) # Posicion del boton
    btnCargar = Button(ventanaInicio, text="Cargar archivo", command=lambda: obtenerArchivo(btnStart)) # Comando del boton
    btnCargar.place(x=ancho/2, y=(alto-100)/2, anchor=CENTER) # Posicion del boton
    ventanaInicio.mainloop()
    return

""" 
teclas
Entrada: ninguna.
Salida: ninguna.
Funcionamiento: Funciona como un listener de teclas, llama a funciones al presionar teclas o botones.
"""
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
                    mostrarSolucion(ventanaJuego)
                if btnSugerencia.collidepoint(p.mouse.get_pos()):
                    mostrarSugerencia(ventanaJuego)
                if btnVerificar.collidepoint(p.mouse.get_pos()):
                    mostrarValidezPosicion(ventanaJuego)
                if btnReinicar.collidepoint(p.mouse.get_pos()):
                    print("Reiniciar")
                if btnVolver.collidepoint(p.mouse.get_pos()):
                    print("Volver")
                    p.quit()
                    showVentanaInicio()

        p.display.update()
        
""" 
CambiarPosicion
Entrada: direccion (String), ventanaJuego (Tk).
Salida: ninguna.
Funcionamiento: Cambia la posicion de la ficha en la ventanaJuego.
"""
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
        ficha["movimientos"] +=1
        pintarMatriz(ventanaJuego) # Pinta la matriz en la ventana

""" 
esPosicionValida
Entrada: posicion (Diccionario), direccion (String).
Salida: Boolean.
Funcionamiento: Verifica si la posicion es valida.
"""
def esPosicionValida(posicionSiguiente, direccion):
    global matriz
    if posicionSiguiente["X"] < 0 or posicionSiguiente["X"] > (len(matriz[0])- 1) or posicionSiguiente["Y"] < 0 or posicionSiguiente["Y"] > (len(matriz) - 1):
        print("Fuera de rango")
        return False
    if bool(list(prolog.query(f"movimientoValido({matriz[ficha['y']][ficha['x']]}, {direccion}, {matriz[posicionSiguiente['Y']][posicionSiguiente['X']]})"))) == False:
        return False
    return True
        

# Main
if __name__ == "__main__":
    showVentanaInicio()

    
% Base de Conocimiento

posicionValida(i).
posicionValida(ad).
posicionValida(ar).
posicionValida(ab).
posicionValida(at).
posicionValida(inter).
posicionValida(f).

direccionValida(i, derecha).
direccionValida(i, arriba).
direccionValida(i, abajo).
direccionValida(i, izquierda).

direccionValida(ad, derecha).
direccionValida(ar, arriba).
direccionValida(ab, abajo).
direccionValida(at, izquierda).

direccionValida(inter, derecha).
direccionValida(inter, arriba).
direccionValida(inter, abajo).
direccionValida(inter, izquierda).

movimiento(izquierda).
movimiento(derecha).
movimiento(arriba).
movimiento(abajo).

% Funciones

movimientoValido(PosicionActual, Direccion, PosicionSiguiente) :-
    posicionValida(PosicionActual),
    direccionValida(PosicionActual, Direccion),
    posicionValida(PosicionSiguiente).

movimientoValido(Matriz, PosicionActual, Direccion, PosicionSiguiente) :-
    obtenerElemento(Matriz, PosicionActual, Elemento),
    obtenerElemento(Matriz, PosicionSiguiente, ElementoSiguiente),
    movimientoValido(Elemento, Direccion, ElementoSiguiente).

% Lee matriz de strings de un archivo e inserta en lista
creaMatriz(File, Matriz) :-
    open(File, read, Stream),
    read_string(Stream, _, String),
    close(Stream),
    split_string(String, ".\n", ".\n", Lista),
    creaMatrizAux(Lista, Matriz).

creaMatrizAux([], []).
creaMatrizAux([H|T], [H1|T1]) :-
    split_string(H, ",", "[]", H1),
    creaMatrizAux(T, T1).


% Imprime matriz

imprimirMatriz([]).
imprimirMatriz([Fila|Matriz]) :-
    imprimirFila(Fila),
    imprimirMatriz(Matriz).

imprimirFila([]) :-
    nl.
imprimirFila([Caracter|Fila]) :-
    put(Caracter),
    imprimirFila(Fila).


% Busca la posicion de un caracter en la matriz
buscarPosicion(Matriz, Caracter, Posicion) :-
    buscarPosicionAux(Matriz, Caracter, Posicion, 0, 0).

buscarPosicionAux([], _, _, _, _) :-
    fail.
buscarPosicionAux([Fila|Matriz], Caracter, Posicion, FilaActual, ColumnaActual) :-
    buscarPosicionAuxFila(Fila, Caracter, Posicion, FilaActual, ColumnaActual);
    FilaActual1 is FilaActual + 1,
    buscarPosicionAux(Matriz, Caracter, Posicion, FilaActual1, ColumnaActual).

buscarPosicionAuxFila([], _, _, _, _) :-
    fail.
buscarPosicionAuxFila([Caracter|_], Caracter, Posicion, FilaActual, ColumnaActual) :-
    Posicion = [FilaActual, ColumnaActual].
buscarPosicionAuxFila([_|Fila], Caracter, Posicion, FilaActual, ColumnaActual) :-
    ColumnaActual1 is ColumnaActual + 1,
    buscarPosicionAuxFila(Fila, Caracter, Posicion, FilaActual, ColumnaActual1).


obtenerElemento(Matriz, Posicion, Elemento) :-
    obtenerElementoAux(Matriz, Posicion, Elemento, 0, 0).

obtenerElementoAux([], _, _, _, _) :-
    fail.
obtenerElementoAux([Fila|Matriz], Posicion, Elemento, FilaActual, ColumnaActual) :-
    obtenerElementoAuxFila(Fila, Posicion, Elemento, FilaActual, ColumnaActual);
    FilaActual1 is FilaActual + 1,
    obtenerElementoAux(Matriz, Posicion, Elemento, FilaActual1, ColumnaActual).

obtenerElementoAuxFila([], _, _, _, _) :-
    fail.
obtenerElementoAuxFila([Elemento|_], Posicion, Elemento, FilaActual, ColumnaActual) :-
    Posicion = [FilaActual, ColumnaActual].
obtenerElementoAuxFila([_|Fila], Posicion, Elemento, FilaActual, ColumnaActual) :-
    ColumnaActual1 is ColumnaActual + 1,
    obtenerElementoAuxFila(Fila, Posicion, Elemento, FilaActual, ColumnaActual1).


puntos([[-1, 0], [1, 0], [0, -1], [0, 1]]).

obtenerPuntos(derecha, Res) :-
    nth0(3, [[-1, 0], [1, 0], [0, -1], [0, 1]], Res).
obtenerPuntos(izquierda, Res) :-
    nth0(2, [[-1, 0], [1, 0], [0, -1], [0, 1]], Res).
obtenerPuntos(arriba, Res) :-
    nth0(0, [[-1, 0], [1, 0], [0, -1], [0, 1]], Res).
obtenerPuntos(abajo, Res) :-
    nth0(1, [[-1, 0], [1, 0], [0, -1], [0, 1]], Res).


avanzarPosicion(Movimiento, PosicionActual, NuevaPos) :-
    obtenerPuntos(Movimiento, Res),
    nth0(0, Res, AvanceX),
    nth0(1, Res, AvanceY),
    nth0(0, PosicionActual, Columna),
    nth0(1, PosicionActual, Fila),
    ColumnaNueva is Columna + AvanceX,
    FilaNueva is Fila + AvanceY,
    ColumnaNueva >= 0,
    FilaNueva >= 0,
    NuevaPos = [ColumnaNueva, FilaNueva].

% Retorna lista con posiciones que solucionan el laberinto

solucionarLaberinto(Matriz, Solucion) :-
    buscarPosicion(Matriz, i, PosicionInicial),
    buscarPosicion(Matriz, f, PosicionFinal),
    solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion).

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion) :-
    solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, []).

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    PosicionInicial = PosicionFinal,
    Solucion = [PosicionInicial|Visitados].

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    movimiento(Movimiento),
    avanzarPosicion(Movimiento, PosicionInicial, PosicionSiguiente),
    movimientoValido(Matriz, PosicionInicial, Movimiento, PosicionSiguiente),
    \+member(PosicionSiguiente, Visitados),
    write("POS Inicial: "), write(PosicionInicial), nl,
    write("POS Siguiente: "), write(PosicionSiguiente), nl,
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion, [PosicionInicial|Visitados]).

/******************
solucionarLaberinto(Matriz, Solucion) :-
    buscarPosicion(Matriz, i, PosicionInicial),
    buscarPosicion(Matriz, f, PosicionFinal),
    solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion).

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion) :-
    solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, []).

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    PosicionInicial = PosicionFinal,
    Solucion = [PosicionInicial|Visitados].

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    movimiento(Movimiento),
    movimientoValido(Matriz, PosicionInicial, Movimiento, PosicionSiguiente),
    \+member(PosicionSiguiente, Visitados),
    write("POS Inicial: "), write(PosicionInicial), nl,
    write(PosicionSiguiente), nl,
    nth0(0, PosicionInicial, Fila),
    nth0(1, PosicionInicial, Columna),
    ColumnNueva is Columna + 1,
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion, [PosicionInicial|Visitados]).
********************/


/****
solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionInicial, Elemento),
    nth0(0, PosicionInicial, Fila),
    nth0(1, PosicionInicial, Columna),
    ColumnNueva is Columna + 1,
    PosicionSiguiente = [Fila, ColumnaNueva],
    obtenerElemento(Matriz, PosicionSiguiente, ElementoSiguiente),
    movimientoValido(Elemento, derecha, ElementoSiguiente),
    write(ElementoSiguiente), nl,
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1],
    write(Solucion).


solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    write("Hola Mundo"), nl,
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionInicial, Elemento),
    nth0(0, PosicionInicial, Fila),
    nth0(1, PosicionInicial, Columna),
    ColumnNueva is Columna - 1,
    PosicionSiguiente = [Fila, ColumnaNueva],
    obtenerElemento(Matriz, PosicionSiguiente, ElementoSiguiente),
    movimientoValido(Elemento, izquierda, ElementoSiguiente),
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1],
    write("Hello World"), nl.

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionInicial, Elemento),
    nth0(0, PosicionInicial, Fila),
    nth0(1, PosicionInicial, Columna),
    FilaNueva is Fila + 1,
    PosicionSiguiente = [FilaNueva, Columna],
    obtenerElemento(Matriz, PosicionSiguiente, ElementoSiguiente),
    movimientoValido(Elemento, abajo, ElementoSiguiente),
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1],
    write("Hola Mundo"), nl.

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionInicial, Elemento),
    nth0(0, PosicionInicial, Fila),
    nth0(1, PosicionInicial, Columna),
    FilaNueva is Fila - 1,
    PosicionSiguiente = [FilaNueva, Columna],
    obtenerElemento(Matriz, PosicionSiguiente, ElementoSiguiente),
    movimientoValido(Elemento, arriba, ElementoSiguiente),
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1],
    write("Hola Mundo"), nl.
*********/

/* 
solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    movimientoValido(PosicionInicial, derecha, PosicionSiguiente),
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionSiguiente, Elemento),
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion1, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1].
solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    movimientoValido(PosicionInicial, izquierda, PosicionSiguiente),
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionSiguiente, Elemento),
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion1, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1].

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    movimientoValido(PosicionInicial, arriba, PosicionSiguiente),
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionSiguiente, Elemento),
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion1, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1].

solucionarLaberintoAux(Matriz, PosicionInicial, PosicionFinal, Solucion, Visitados) :-
    movimientoValido(PosicionInicial, abajo, PosicionSiguiente),
    not(member(PosicionSiguiente, Visitados)),
    obtenerElemento(Matriz, PosicionSiguiente, Elemento),
    solucionarLaberintoAux(Matriz, PosicionSiguiente, PosicionFinal, Solucion1, [PosicionInicial|Visitados]),
    Solucion = [PosicionInicial|Solucion1].

*/
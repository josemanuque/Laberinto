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

% Funciones

movimientoValido(PosicionActual, Direccion, PosicionSiguiente) :-
    posicionValida(PosicionActual),
    direccionValida(PosicionActual, Direccion),
    posicionValida(PosicionSiguiente).


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
    


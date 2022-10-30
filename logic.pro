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


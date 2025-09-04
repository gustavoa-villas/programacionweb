#Cuadricula como la de un tablero de ajedres don de hay una ficha que se mueve como la reina del ajedres, inputs: posición de la reina, 
# tamaño del tablero, bloqueos(lugares donde no se puede mover) output: cantidad de movimientos (cantidad de movimientos que puede hacer la reina)
def movimientos_reina(posicion, tamaño, bloqueos):
    bloqueos = set(bloqueos)
    direcciones = [
        (1, 0), (-1, 0),  # vertical
        (0, 1), (0, -1),  # horizontal
        (1, 1), (-1, -1), # diagonal principal
        (1, -1), (-1, 1)  # diagonal secundaria
    ]
    
    movimientos = 0
    x, y = posicion

    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        while 0 <= nx < tamaño and 0 <= ny < tamaño and (nx, ny) not in bloqueos:
            movimientos += 1
            nx += dx
            ny += dy
    
    return movimientos

#pruebas, datos para ingresar
tamaño_tablero = 4
posicion_reina = (0, 2)
bloqueos = [(1, 1)]

# salida
movs = movimientos_reina(posicion_reina, tamaño_tablero, bloqueos)
print("Cantidad de movimientos posibles:", movs)

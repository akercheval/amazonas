### Tarea 3 - Amazonas
### Por Adam Kercheval
### Este programa cumple los requisitos para el Bonus:
###     El jugador "Bot" tiene inteligencia aleatoria sus movimientos no
###     dependen en ninguna estrategia. Su implementación entera está en
###     la función "botfunc"
import os
from random import randint

################################################################################
###                                                                          ###
###                     Implementación de clase Jugador                      ###
###                                                                          ###
################################################################################

class Jugador:

    def __init__(self, celdas, num, nombre, simb, bot):
        self.nombre = nombre
        self.celdas = celdas
        self.num = num
        self.simb = simb
        self.bot = bot

    def valido(self, lista, inicio, fin):
        if inicio not in self.celdas:
            if self.bot == False:
                print("No hay amazona en la celda de inicio!", end=" ")
            return False
        if inicio == fin:
            if self.bot == False:
                print("La celda inicial y la celda final son iguales!", end=" ")
            return False
        ix = ord(inicio[0]) - 97
        fx = ord(fin[0]) - 97
        iy = 10 - int(inicio[1:])
        fy = 10 - int(fin[1:])
        if fx > 9 or fx < 0 or fy > 9 or fy < 0:
            if self.bot == False:
                print("Celda especificada no esta en el tablero!", end=" ")
            return False
        ### movimiento vertical ###
        if ix == fx and iy < fy:
            for i in range(iy + 1,fy + 1):
                if lista[i][ix] == '*' or lista[i][ix] == 'X' \
                        or lista[i][ix] == 'O':
                    if self.bot == False:
                        print("Hay jugador o flecha bloqueando!", end = " ")
                    return False
            return True
        elif ix == fx and iy > fy:
            for i in range(fy,iy):
                if lista[i][ix] == '*' or lista[i][ix] == 'X' \
                        or lista[i][ix] == 'O':
                    if self.bot == False:
                        print("Hay jugador o flecha bloqueando!", end = " ")
                    return False
            return True
        ### movimiento horizontal ###
        elif iy == fy and ix < fx:
            for i in range(ix + 1,fx + 1):
                if lista[iy][i] == '*' or lista[iy][i] == 'X' \
                       or lista[iy][i] == 'O':
                    if self.bot == False:
                        print("Hay jugador o flecha bloqueando!", end = " ")
                    return False
            return True
        elif iy == fy and ix > fx:
            for i in range(fx,ix):
                if lista[iy][i] == '*' or lista[iy][i] == 'X' \
                        or lista[iy][i] == 'O':
                    if self.bot == False:
                        print("Hay jugador o flecha bloqueando!", end = " ")
                    return False
            return True
        ### movimiento diagonal ###
        elif abs(ix - fx) == abs(iy - fy):
            r = abs(ix - fx) + 1
            ### movimiento arriba y a la derecha
            if ix < fx and iy > fy:
                for i in range(1,r):
                    if lista[iy - i][ix + i] == '*' or lista[iy - i][ix + i] == 'X' \
                            or lista[iy - i][ix + i] == 'O':
                        if self.bot == False:
                            print("Hay jugador o flecha bloqueando!", end = " ")
                        return False
                return True
            ### movimiento arriba y a la izquierda
            if ix > fx and iy > fy:
                for i in range(1,r):
                    if lista[iy - i][ix - i] == '*' or lista[iy - i][ix - i] == 'X' \
                            or lista[iy - i][ix - i] == 'O':
                        if self.bot == False:
                            print("Hay jugador o flecha bloqueando!", end = " ")
                        return False
                return True
            ### movimiento abajo y a la derecha
            if ix < fx and iy < fy:
                for i in range(1,r):
                    if lista[iy + i][ix + i] == '*' or lista[iy + i][ix + i] == 'X' \
                            or lista[iy + i][ix + i] == 'O':
                        if self.bot == False:
                            print("Hay jugador o flecha bloqueando!", end = " ")
                        return False
                return True
            ### movimiento abajo y a la izquierda
            if ix > fx and iy < fy:
                for i in range(1,r):
                    if lista[iy + i][ix - i] == '*' or lista[iy + i][ix - i] == 'X' \
                            or lista[iy + i][ix - i] == 'O':
                        if self.bot == False:
                            print("Hay jugador o flecha bloqueando!", end = " ")
                        return False
                return True
        if self.bot == False:
            print("Solo puede mover o lanzar verticalmente, horizontalmente", end="")
            print(" o diagonalmente!", end=" ")
        return False


    def movimiento_valido(self, inicio, fin, lista):
        if self.valido(lista, inicio, fin):
            return True
        else:
            return False

    def lanzamiento_valido(self, inicio, fin, lista):
        if self.valido(lista, inicio, fin):
            return True
        else:
            return False

    def quedan_movimientos(self, celda, lista):
        x = ord(celda[0]) - 97
        y = 10 - int(celda[1:])
        for i in range(-1,2):
            for j in range(-1,2):
                tx = x + j
                ty = y + i
                if tx < 0 or tx > 9:
                    continue
                if ty < 0 or ty > 9:
                    continue
                if i == 0 and j == 0:
                    continue
                if lista[ty][tx] == ' ':
                    return True
        return False

    # una nota: ese función no verifica si la amazona pueda mover y lanzar una
    # flecha - solo verifica si pueda mover. Eso es porque si una amazona puede
    # mover, siempre puede lanzar una flecha por lo menos a la celda de que
    # acaba de salir. En otras palabras, no es necesario hacer más que
    # verificar si puede mover, porque si puede mover, puede lanzar.
    def perdedor(self, lista):
        for celda in self.celdas:
            if self.quedan_movimientos(celda, lista):
                return False
        return True

    def mover(self, inicio, fin, lista):
        if self.quedan_movimientos(inicio, lista) \
        and self.movimiento_valido(inicio, fin, lista):
            for i in range(len(self.celdas)):
                if self.celdas[i] == inicio:
                    self.celdas[i] = fin
            nueva = self.celdas[0] + ',' + self.celdas[1] + ',' + self.celdas[2] + \
                    ',' + self.celdas[3] + '\n'
            archivo = open("tablero.txt", "r")
            data = ""
            if self.num == 1:
                archivo.readline()
                data += nueva
                for i in range(3):
                    data += archivo.readline()
            else:
                data += archivo.readline()
                data += nueva
                archivo.readline()
                for i in range(2):
                    data += archivo.readline()

            data = str(data)
            data.split()
            guardar_tablero(data)
            if self.bot == False:
                print(self.nombre, "ha movido desde", inicio, "a", fin)
            return True
        else:
            if self.bot == False:
                print("Movimiento invalido.")
            return False

    def lanzar(self, inicio, fin, lista):
        if self.quedan_movimientos(inicio, lista) \
        and self.lanzamiento_valido(inicio, fin, lista):
            archivo = open("tablero.txt", "r")
            data = ""
            data += archivo.readline()
            data += archivo.readline()
            flechas = archivo.readline()
            if flechas == '1' or flechas == '2': #no hay flechas
                data += fin + '\n'
                if self.num == 1:
                    data += '2\n'
                else:
                    data += '1\n'
            else:
                flechas = flechas.strip() + ',' + fin + '\n'
                data += flechas
                if self.num == 1:
                    data += '2\n'
                else:
                    data += '1\n'

            data = str(data)
            data.split()
            guardar_tablero(data)
            if self.bot == False:
                print(self.nombre, "ha lanzado desde", inicio, "a", fin)
            return True
        else:
            if self.bot == False:
                print("Lanzamiento invalido")
            return False

    def botfunc(self, lista):
        if self.perdedor(lista) == True:
            salir(tablero, j2)
        num = randint(0,3)
        ini = self.celdas[num]
        while self.quedan_movimientos(ini, lista) == False:
            num = randint(0,3)
            ini = self.celdas[num]

        ## Mover ##

        x = randint(0,9)
        y = randint(0,9)
        fin = chr(x + 97) + str(9 - y)
        while self.mover(ini, fin, lista) == False:
            x = randint(0,9)
            y = randint(0,9)
            fin = chr(x + 97) + str(10 - y)
        print(self.nombre, "ha movido desde", ini, "a", fin)

        ## Lanzar ##

        tablero = cargar_tablero()
        lista = hacer_lista(tablero)
        if self.perdedor(lista) == True:
            salir(tablero, j2)
        ini = fin
        x = randint(0,9)
        y = randint(0,9)
        fin = chr(x + 97) + str(9 - y)
        while self.lanzar(ini, fin, lista) == False:
            x = randint(0,9)
            y = randint(0,9)
            fin = chr(x + 97) + str(10 - y)
        print(self.nombre, "ha lanzado desde", ini, "a", fin)



################################################################################
###                                                                          ###
###                     Funciones fuera de OOP                               ###
###                                                                          ###
################################################################################

def salir(tablero, quien_sale):
    if quien_sale.bot == False:
        print("Saliendo del juego!")
    if quien_sale == j1:
        ganador = j2
    else:
        ganador = j1
    print(ganador.nombre, "ha ganado!")
    print(str(tablero_to_string(tablero)))
    exit()

def guardar_tablero(tablero):
    archivo = open("tablero.txt", "w")
    archivo.write(tablero)
    archivo.close()

def cargar_tablero():
    tablero = [];
    if os.path.isfile("tablero.txt") == False:
        print("No hay archivo llamado 'tablero.txt'")
        return tablero;
    archivo = open("tablero.txt", "r")
    for line in archivo:
        tablero.append(line.strip().split(','))
    return tablero

def horizontal():
    return "  +---+---+---+---+---+---+---+---+---+---+\n"

def hacer_lista(tablero):
    lista = []
    for i in range(10):
        lista.append([" "] * 10)
    for i in range(3):
        for j in range(len(tablero[i])):
            if i == 2 and len(tablero[i][j]) == 1: #no hay flechas
                break
            y = (ord(tablero[i][j][0]) - 97)
            x = 10 - int(tablero[i][j][1:])
            if i == 0: #jugador 1
                lista[x][y] = 'O'
            elif i == 1: #jugador 2
                lista[x][y] = 'X'
            elif i == 2: #flechas
                lista[x][y] = '*'
    return lista

def tablero_to_string(tablero):
    lista = hacer_lista(tablero)
    tabstr = ""
    tabstr += " Jugador 1: O -- Jugador 2: X -- Flechas : *\n"
    tabstr += horizontal()
    for i in range(10):
        tabstr += str(10 - i)
        if ((10 - i) < 10):
            tabstr += " "
        for j in range(10):
           tabstr += ("| " + str(lista[i][j]) + " ")
        tabstr += "|\n"
        tabstr += horizontal()
    tabstr += "    a   b   c   d   e   f   g   h   i   j  \n"
    return tabstr

def nuevo_tablero():
    archivo = open("tablero.txt", "w")
    archivo.write("a4,d1,g1,j4\n")
    archivo.write("a7,d10,g10,j7\n")
    archivo.write("1")
    archivo.close()
    return cargar_tablero() #para retornar lista de listas con 4 elementos


################################################################################
###                                                                          ###
###                               Juego                                      ###
###                                                                          ###
################################################################################


print("=============== AMAZONAS - T2 IIC1103 ===============")
print("Bienvenido a Amazonas!")
print("En este juego, jugador 1 es 'O', jugador 2 es 'X', y las flechas son '*'")
print("Diga nombre de Jugador 1:")
nombre1 = input(">> ")
bot = input("Quiere jugar contra un bot? (s/n): ")
if bot == 's':
    bot_bool = True
    nombre2 = "Bot"
else:
    bot_bool = False
    print("Diga nombre de Jugador 2:")
    nombre2 = input(">> ")
print("Que quiere hacer?")
print("1) Empezar nuevo tablero")
print("2) Cargar partida guardada")
juego = int(input(">> "))
if juego == 1:
    tablero = nuevo_tablero()
else:
    tablero = cargar_tablero()
j1 = Jugador(tablero[0], 1, nombre1, 'O', False)
j2 = Jugador(tablero[1], 2, nombre2, 'X', bot_bool)
if tablero[-1][0] == '1':
    jugador = j1
else:
    jugador = j2
l = hacer_lista(tablero)

while(j1.perdedor(l) == False and j2.perdedor(l) == False):
    print("\n======== Turno de", jugador.nombre, "(", jugador.simb, ") ========")
    if jugador.bot == True:
        print(str(tablero_to_string(tablero)))
        jugador.botfunc(l)
        tablero = cargar_tablero()
        l = hacer_lista(tablero)
        if jugador == j1:
            jugador = j2
        else:
            jugador = j1
        continue
    print("En cualquier momento, puede escribir -1 para salir del juego\n")
    print(str(tablero_to_string(tablero)))
    print("\nEscoja una de sus amazonas:")
    ini = input(">> ")
    if ini == "-1":
        salir(tablero, jugador)
    while ini not in jugador.celdas:
        print("Amazona invalida - escoja otra! (forma: columna,fila - ejemplo: a8)")
        ini = input(">> ")
        if ini == "-1":
            salir(tablero, jugador)

    ### MOVER ###
    print("Amazona valida, hacia que celda quiere mover su amazona?")
    fin = input(">> ")
    if fin == "-1":
        salir(tablero, jugador)
    while jugador.mover(ini, fin, l) == False:
        fin = input("Escoja otra celda para mover (forma: columna,fila - ejemplo: a8): ")
        if fin == "-1":
            salir(tablero, jugador)
    tablero = cargar_tablero()
    l = hacer_lista(tablero)
    print(str(tablero_to_string(tablero)))

    ### LANZAR ###
    ini = fin
    print("Donde quiere lanzar una flecha?")
    fin = input(">> ")
    if fin == "-1":
        salir(tablero, jugador)
    while jugador.lanzar(ini, fin, l) == False:
        fin = input("Escoja otra celda para lanzar (forma: columna,fila - ejemplo: a8): ")
        if fin == "-1":
            salir(tablero, jugador)
    tablero = cargar_tablero()
    l = hacer_lista(tablero)
    if jugador == j1:
        jugador = j2
    else:
        jugador = j1

## Final del juego ##
print(str(tablero_to_string(tablero)))
if j1.perdedor(l):
    tablero = nuevo_tablero()
    print(j2.nombre, "ha ganado!")
elif j2.perdedor(l):
    tablero = nuevo_tablero()
    print(j1.nombre, "ha ganado!")

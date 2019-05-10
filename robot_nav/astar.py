from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from collections import deque
import os
import csv
import time
import operator
import math
from io import open





# convertir a coordenadas
def xconverter(tamano, cuadros, x):
    paso = int(tamano / cuadros) + 1
    x = paso * x
    return int(x)


def yconverter(tamano, cuadros, y):
    paso = int(tamano / cuadros) + 1
    y = tamano - paso * y
    return int(y)

def astar(mapa,resolution,a,b,c,d,angle):
    # radio de los circulos
    radio = 10

    # tiempo de pausa
    tiempo = 0.005
    # window setup
    cuadriculade = 10
    winsize = 700
    winsize = winsize + cuadriculade - 1

    if mapa == 1:
        mapa = u'map01.csv'
    elif mapa == 2:
        mapa = u'map02.csv'
    elif mapa == 3:
        mapa = u'map03.csv'
    elif mapa == 0:
        mapa = u'map00.csv'

    # lista de coordenadas donde se encuentran obstculos
    obs = []
    filepath = os.getcwd()
    # generacin visual de obstculos
    with open(filepath + "/" + mapa, u'r') as file:
        reader = csv.reader(file)
        for row in reader:
            ox, oy, w, h = float(row[0]), float(row[1]), float(row[2]), float(row[3])
            xo = xconverter(winsize, cuadriculade, ox)
            yo = 700 + cuadriculade - 1 - xconverter(winsize, cuadriculade, oy)

            for xi in xrange(0, int(h * resolution + 1)):
                for xa in xrange(0, int(w * resolution + 1)):
                    obs.append((ox * resolution + xa, oy * resolution + xi))

    if (obs[0] == (0.0, 0.0) and len(obs) == 1):
        obs[:] = []


    # asking for information


    xi = a
    yi = b
    xf = c
    yf = d


    # Forward search
    Q = deque([])
    Q.append((xi * resolution, yi * resolution))
    visited = []
    visited.append((xi * resolution, yi * resolution))
    acciones = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    found = False
    while (len(Q) > 0):
        ct = Q.popleft()
        if found == True:  # ct[0] == xf*resolution and ct[1]*resolution == yf:
            break
        for accion in acciones:
            nueva = (ct[0] + accion[0], ct[1] + accion[1])
            if (((nueva[0] <= 10 * resolution) and (nueva[0] >= 0 * resolution) and (nueva[1] <= 10 * resolution)) and ((
                    nueva[1] >= 0 * resolution))) and nueva not in visited and nueva not in obs:
                visited.append(nueva)
                Q.append(nueva)

                time.sleep(tiempo)
                if nueva[0] == xf * resolution and nueva[1] == yf * resolution:
                    found = True
                    break
    #esta seccion permite tratar con situaciones en donde xi=xf y yi=yf
    izqui=[]
    dere=[]
    arriba=[]
    abajo=[]
    if xi==xf:
        for x in visited:
            if x[0]<xi*resolution:
                izqui.append(x)
            else:
                dere.append(x)
        if len(dere)>len(izqui):
            visited=dere
        else:
            visited=izqui
    if yi==yf:
        for y in visited:
            if y[1]<yi*resolution:
                abajo.append(y)
            else:
                arriba.append(y)
        if len(arriba)>len(abajo):
            visited=arriba
        else:
            visited=abajo
    ######################################################################################3




    # A* implementation
    dicti = {}
    path = []
    path.append((xi * resolution, yi * resolution))
    visited.append((xf * resolution, yf * resolution))  # * resolution

    for x in visited:
        x = path[-1]
        for y in acciones:
            new = (x[0] + y[0], x[1] + y[1])
            old_price = ((xf * resolution - path[-1][0]) ** 2 + (yf * resolution - path[-1][1]) ** 2) ** (1 / 2)
            pasado = ((xi * resolution - new[0]) ** 2 + (yi * resolution - new[1]) ** 2) ** (1 / 2)

            new_price = ((xf * resolution - new[0]) ** 2 + (yf * resolution - new[1]) ** 2) ** (1 / 2)


            if xi==xf:
                if(new[1]!=yf*resolution):#si no se esta a la misma altura
                    if new in visited and new not in path and new[1]!=yi*resolution and abs(yf*resolution-new[1])<=abs(yf*resolution-path[-1][1]): #and new[1]>=path[-1][1]:
                        dicti[new] = new_price

                    else:
                        dicti[new] = 10000000000000
                else:#si no se esta a la misma distancia horizontal
                    if new in visited and new not in path and new[1]!=yi*resolution and abs(xf*resolution-new[0])<=abs(xf*resolution-path[-1][0]): #and new[1]>=path[-1][1]:
                        dicti[new] = new_price

                    else:
                        dicti[new] = 10000000000000





            elif yi==yf:
                if(new[0]!=xf*resolution):#si no se esta a la misma distancia horizontal
                    if new in visited and new not in path and new[0]!=xi*resolution and abs(xf*resolution-new[0])<=abs(xf*resolution-path[-1][0]):
                        dicti[new] = new_price
                    else:
                        dicti[new] = 10000000000000
                else:#si no se esta a la misma altura
                    if new in visited and new not in path and new[0]!=xi*resolution and abs(yf*resolution-new[1])<=abs(yf*resolution-path[-1][1]):
                        dicti[new] = new_price
                    else:
                        dicti[new] = 10000000000000



            else:
                if new in visited and new not in path:
                    dicti[new] = new_price

                else:
                    dicti[new] = 10000000000000




        t = min(dicti.items(), key=operator.itemgetter(1))[0]
        # se anade a la lista de los buenos
        path.append((t[0], t[1]))
        if t == (xf * resolution, yf * resolution):
            break
        # se limpia el diccionario
        dicti.clear()



    # Para implementacin en el robot

    angulos = {
        (0, 0): angle,
        (0, 1): 90,
        (1, 1): 45,
        (1, 0): 0,
        (1, -1): -45,
        (0, -1): -90,
        (-1, -1): -135,
        (-1, 0): 180,
        (-1, 1): 135

    }

    acciones = []
    mov = []
    for x in xrange(0, len(path) - 1):
        mov.append((path[x + 1][0] - path[x][0], path[x + 1][1] - path[x][1]))

    mov.insert(0, (0, 0))

    for x in xrange(0, len(mov) - 1):
        if (abs(mov[x + 1][0]) + abs(mov[x + 1][1])) == 2:
            acciones.append((angulos[mov[x + 1]] - angulos[mov[x]], (((1 / resolution) ** 2) * 2) ** (1 / 2)))
        else:
            acciones.append((angulos[mov[x + 1]] - angulos[mov[x]], 1 / resolution))

    ###################Movimientos fluidos##############################
    accionesfluidas = []
    x = 0

    while (x < len(acciones) - 1):
        rota = acciones[x][0]
        trasla = acciones[x][1]
        for w in xrange(x + 1, len(acciones)):

            if acciones[x][1] == acciones[w][1] and acciones[w][0] == 0:

                trasla = trasla + acciones[w][1]
                x = w

            else:
                break
        accionesfluidas.append((rota, trasla))
        x = x + 1

    ##################################################################

    costofinal = 0
    for x in mov:
        if x == (1, 1) or x == (-1, -1) or x == (-1, 1) or x == (1, -1):
            costofinal = costofinal + (((1 / resolution) ** 2) * 2) ** (1 / 2)
        else:
            costofinal = costofinal + (1 / resolution)
    info=path,mov,acciones
    # print(mov)
    #print(path)
    # print(acciones)
    # print(visited)
    return(info)
    #print(accionesfluidas)
    #print('El cossto final del recorrido es: ', costofinal)

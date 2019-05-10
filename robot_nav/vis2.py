#!/usr/bin/env python
from graphics import *
import os
import csv
import time
import operator
import math


# convertir a coordenadas
def xconverter(tamano, cuadros, x):
    paso = int(tamano / cuadros) + 1
    x = paso * x
    return int(x)
def yconverter(tamano, cuadros, y):
    paso = int(tamano / cuadros) + 1
    y = tamano - paso * y
    return int(y)

def input1():
    x=int(input(''))
    return x

# parametros de inicializacion
def visualizacion(map1,path,xi,yi,xf,yf,resolution,angle):
    if map1 == 1:
        mapa = 'map01.csv'
    elif map1 == 2:
        mapa = 'map02.csv'
    elif map1 == 3:
        mapa = 'map03.csv'
    elif map1 == '0':
        mapa = 'map00.csv'

    winsize=700
    cuadriculade=10
    win = GraphWin('ches', 710, 710) # give title and dimensions

    #prueba####################

    with open(os.path.dirname(__file__)+'/'+mapa, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            ox, oy, w, h = float(row[0]), float(row[1]), float(row[2]), float(row[3])
            xo = xconverter(winsize, cuadriculade, ox)
            yo = 700 + cuadriculade - 1 - xconverter(winsize, cuadriculade, oy)
            w = xconverter(winsize, cuadriculade, w)
            h = xconverter(winsize, cuadriculade, h)
            pi=Point(xo,yo)
            pf=Point(xo+w,yo-h)
            rect = Rectangle(pi, pf)
            rect.draw(win)

    #dibujo del punto inicial y final
    ip=Point(xconverter(winsize, cuadriculade, xi),yconverter(winsize, cuadriculade, yi))
    fp=Point(xconverter(winsize, cuadriculade, xf),yconverter(winsize, cuadriculade, yf))
    inicio = Circle(ip, 10)
    inicio.setFill("blue")
    inicio.draw(win)
    final = Circle(fp, 10)
    final.setFill("red")
    final.draw(win)


    # dibujo de la trayectoria

    for x in range(0, len(path) - 1):
        lini=Point(xconverter(winsize, cuadriculade, path[x][0] / resolution),yconverter(winsize, cuadriculade, path[x][1] / resolution))
        lifi=Point(xconverter(winsize, cuadriculade, path[x + 1][0] / resolution),yconverter(winsize, cuadriculade, path[x + 1][1] / resolution))
        trip=Line(lini,lifi)
        trip.draw(win)
    ima_de_ini=''
    if angle==90:
        ima_de_ini='N.png'
    elif angle==45:
        ima_de_ini='NE.png'
    elif angle==0:
        ima_de_ini='E.png'
    elif angle==-45:
        ima_de_ini='SE.png'
    elif angle==-90:
        ima_de_ini='S.png'
    elif angle==-135:
        ima_de_ini='SO.png'
    elif angle==180:
        ima_de_ini='O.png'
    elif angle==135:
        ima_de_ini='NO.png'



    angulos = {
        (0, 0): ima_de_ini,
        (0, 1): 'N.png',
        (1, 1): 'NE.png',
        (1, 0): 'E.png',
        (1, -1): 'SE.png',
        (0, -1): 'S.png',
        (-1, -1): 'SO.png',
        (-1, 0): 'O.png',
        (-1, 1): 'NO.png'

    }

    mov = []
    for x in range(0, len(path) - 1):
        mov.append((path[x + 1][0] - path[x][0], path[x + 1][1] - path[x][1]))

    mov.insert(0, (0, 0))


    movie=Point(xconverter(winsize, cuadriculade, path[0][0] / resolution),yconverter(winsize, cuadriculade, path[0][1] / resolution))
    actual=Image(movie,os.path.dirname(__file__)+'/'+angulos[mov[0]])
    actual.draw(win)

    x=0
    while(x<=len(mov)):
        mover=input1() #este se acualiza por medio del arduino
        obstacle=int(input('existe un obstaculo?: ')) #y este se deben de estar actualizando por medio del laser
        if obstacle==1:
            win.close()
            return
        if mover!=1:
            continue
        actual.undraw()
        x=x+1
        movie=Point(xconverter(winsize, cuadriculade, path[x][0] / resolution),yconverter(winsize, cuadriculade, path[x][1] / resolution))
        actual=Image(movie,os.path.dirname(__file__)+'/'+angulos[mov[x]])
        actual.draw(win)

        

        
    

            
    win.getMouse()
    win.close()


#p=[(4.0, 4.0), (5.0, 5.0), (5.0, 6.0), (5.0, 7.0), (5.0, 8.0), (6.0, 9.0), (7.0, 10.0), (8.0, 11.0), (9.0, 12.0),(9.0,13.0), (9.0, 14.0), (9.0, 15.0), (9.0, 16.0), (10.0, 17.0), (11.0, 18.0), (12.0, 18.0), (13.0, 18.0), (14.0, 18.0), (15.0, 18.0), (16.0, 18.0), (17.0, 18.0), (18.0, 18.0)]
#mapi=2
#a,b=2,2
#c,d=9,9
#resolucion=2

#visualizacion(mapi,p,a,b,c,d,resolucion,90)



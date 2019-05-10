#!/usr/bin/env python
from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from graphics import *
import os
import csv
import time
import operator
import math
import serial
from io import open
filepath = os.getcwd()
try:
    arduino=serial.Serial(u'/dev/ttyUSB0',baudrate=9600, timeout = None)
    #arduino.setDTR(True)
except:
    arduino=serial.Serial(u'/dev/ttyUSB1',baudrate=9600, timeout = None)
    #arduino.setDTR(True)
def readwrite(micro,x):
    if micro.isOpen():
        micro.flush()
        n=x
        micro.write(str(('%f'+'\n')%n).encode('utf-8'))
        time.sleep(.25)
        f=int((micro.read(1)).encode('hex'), 16)
        if f > 0:
            f=1
        else:
            f=0
        print f
        return(f)

    arduino.close()

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
    x=int(raw_input(u''))
    return x

# parametros de inicializacion
def visualizacion(map1,path,xi,yi,xf,yf,resolution,angle,acciones):
    if map1 == 1:
        mapa = u'map01.csv'
    elif map1 == 2:
        mapa = u'map02.csv'
    elif map1 == 3:
        mapa = u'map03.csv'
    elif map1 == u'0':
        mapa = u'map00.csv'

    winsize=700
    cuadriculade=10
    win = GraphWin('ches', 710, 710) # give title and dimensions

    #prueba####################

    with open(mapa, u'r') as file:
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
    inicio.setFill(u"blue")
    inicio.draw(win)
    final = Circle(fp, 10)
    final.setFill(u"red")
    final.draw(win)


    # dibujo de la trayectoria

    for x in xrange(0, len(path) - 1):
        lini=Point(xconverter(winsize, cuadriculade, path[x][0] / resolution),yconverter(winsize, cuadriculade, path[x][1] / resolution))
        lifi=Point(xconverter(winsize, cuadriculade, path[x + 1][0] / resolution),yconverter(winsize, cuadriculade, path[x + 1][1] / resolution))
        trip=Line(lini,lifi)
        trip.draw(win)
    ima_de_ini=u''
    if angle==90:
        ima_de_ini=u'N.png'
    elif angle==45:
        ima_de_ini=u'NE.png'
    elif angle==0:
        ima_de_ini=u'E.png'
    elif angle==-45:
        ima_de_ini=u'SE.png'
    elif angle==-90:
        ima_de_ini=u'S.png'
    elif angle==-135:
        ima_de_ini=u'SO.png'
    elif angle==180:
        ima_de_ini=u'O.png'
    elif angle==135:
        ima_de_ini=u'NO.png'



    angulos = {
        (0, 0): ima_de_ini,
        (0, 1): u'N.png',
        (1, 1): u'NE.png',
        (1, 0): u'E.png',
        (1, -1): u'SE.png',
        (0, -1): u'S.png',
        (-1, -1): u'SO.png',
        (-1, 0): u'O.png',
        (-1, 1): u'NO.png'

    }

    mov = []
    for x in xrange(0, len(path) - 1):
        mov.append((path[x + 1][0] - path[x][0], path[x + 1][1] - path[x][1]))

    mov.insert(0, (0, 0))


    movie=Point(xconverter(winsize, cuadriculade, path[0][0] / resolution),yconverter(winsize, cuadriculade, path[0][1] / resolution))
    actual=Image(movie,filepath + "/" + angulos[mov[0]])
    actual.draw(win)

    angulos2 = {
        (0, 1): 90,
        (1, 1): 45,
        (1, 0): 0,
        (1, -1): -45,
        (0, -1): -90,
        (-1, -1): -135,
        (-1, 0): 180,
        (-1, 1): 135

    }

    x=0
    while(x<=len(mov)-1):
        mover=readwrite(arduino,acciones[x][0]) #este se acualiza por medio del arduino
        obstacle=int(raw_input('existe un obstaculo?: ')) #y este se deben de estar actualizando por medio del laser

        if obstacle==1:
            readwrite(arduino,0)#ultima modificacion
            win.close()
            info=path[x][0],path[x][1],angulos2[mov[x]]
            return info
        mover=readwrite(arduino,acciones[x][1])
        if mover!=1:
            continue
        actual.undraw()
        x=x+1
        movie=Point(xconverter(winsize, cuadriculade, path[x][0] / resolution),yconverter(winsize, cuadriculade, path[x][1] / resolution))
        actual=Image(movie,filepath+u'/'+angulos[mov[x]])
        actual.draw(win)







    win.getMouse()
    win.close()

#print(readwrite(arduino,90))
#prueba
accio=[(-45, 0.7071067811865476), (45, 0.5), (0, 0.5), (0, 0.5), (-45, 0.7071067811865476), (0, 0.7071067811865476), (0, 0.7071067811865476), (0, 0.7071067811865476), (45, 0.5), (0, 0.5), (0, 0.5), (0, 0.5), (-45, 0.7071067811865476), (0, 0.7071067811865476), (-45, 0.5), (0, 0.5), (0, 0.5), (0, 0.5), (0, 0.5), (0, 0.5), (0, 0.5)]
p=[(4.0, 4.0), (5.0, 5.0), (5.0, 6.0), (5.0, 7.0), (5.0, 8.0), (6.0, 9.0), (7.0, 10.0), (8.0, 11.0), (9.0, 12.0),(9.0,13.0), (9.0, 14.0), (9.0, 15.0), (9.0, 16.0), (10.0, 17.0), (11.0, 18.0), (12.0, 18.0), (13.0, 18.0), (14.0, 18.0), (15.0, 18.0), (16.0, 18.0), (17.0, 18.0), (18.0, 18.0)]
mapi=2
a,b=2,2
c,d=9,9
resolucion=2

visualizacion(mapi,p,a,b,c,d,resolucion,90,accio)

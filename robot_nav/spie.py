#!/usr/bin/env python
from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
import rospy , struct

import numpy as np
from sensor_msgs.msg import LaserScan
from graphics import *
import os
import csv
import time
import operator
import math
import serial
from io import open
import astar
global anglesin, anglecos
global boundry, mapa
angle = np.arange(360)
angle = np.deg2rad(angle)
anglesin = np.sin(angle)
anglecos = np.cos(angle)

def callback(data):
    global anglesin
    global anglecos
    global xpoint
    global ypoint
    global boundry

    xpoint = data.ranges * anglesin
    ypoint = data.ranges * anglecos
    boundry= 0
    for x in xrange(360):
        if np.isinf(xpoint[x]) == 0 and np.isinf(ypoint[x]) == 0:
            if((-0.10 < xpoint[x] < .10) and (0 < ypoint[x] < .40)): #first quadrant
                if((-0.10 < xpoint[x] < .10) and (0 < ypoint[x] < .32)): #first quadrant
                    boundry = 1
                else:
                    boundry = 2



def xconverter(tamano, cuadros, x):
    paso = int(tamano / cuadros) + 1
    x = paso * x
    return int(x)
def yconverter(tamano, cuadros, y):
    paso = int(tamano / cuadros) + 1
    y = tamano - paso * y
    return int(y)
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
def input1():
    x=int(raw_input(u''))
    return x
def erase():
    global inicio, final, actual, trip, rect
    inicio.undraw()
    final.undraw()
    actual.undraw()
    for ii in xrange(len(trip)):
        trip[ii].undraw()
    for i in xrange(len(rect)):
        rect[i].undraw()
def writecsv(x,y):
    global mapa

    fields=[x, y, .5, .5]
    with open((filepath + "/" + mapa), 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
def updatemap():
    global win, cuadriculade, winsize
    global map1,resolution, xi, yi, xf, yf, angle, acciones, path, actual, filepath,mapa
    global inicio, final, actual, trip, rect

    if map1 == 1:
        mapa = u'map01.csv'
    elif map1 == 2:
        mapa = u'map02.csv'
    elif map1 == 3:
        mapa = u'map03.csv'
    elif map1 == u'0':
        mapa = u'map00.csv'

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
    #prueba####################

    with open((filepath + "/" + mapa), u'r') as file:
        reader = csv.reader(file)
        rect= []
        trip=[]
        holder =0
        boxs = 0
        for row in reader:
            ox, oy, w, h = float(row[0]), float(row[1]), float(row[2]), float(row[3])
            xo = xconverter(winsize, cuadriculade, ox)
            yo = 700 + cuadriculade - 1 - xconverter(winsize, cuadriculade, oy)
            w = xconverter(winsize, cuadriculade, w)
            h = xconverter(winsize, cuadriculade, h)
            pi=Point(xo,yo)
            pf=Point(xo+w,yo-h)
            rect.insert(boxs,Rectangle(pi,pf))
            rect[boxs].draw(win)
            boxs= boxs + 1

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
        trip.insert(holder,Line(lini,lifi))
        trip[holder].draw(win)
        holder= holder + 1


    mov = []
    for x in xrange(0, len(path) - 1):
        mov.append((path[x + 1][0] - path[x][0], path[x + 1][1] - path[x][1]))

    mov.insert(0, (0, 0))


    movie=Point(xconverter(winsize, cuadriculade, path[0][0] / resolution),yconverter(winsize, cuadriculade, path[0][1] / resolution))
    actual=Image(movie,filepath + "/" + angulos[mov[0]])
    actual.draw(win)

def start():

    global win, cuadriculade, winsize, filepath, boundry
    rospy.init_node('obstruction')
    rospy.Subscriber("scan", LaserScan, callback)
    filepath = os.getcwd()
    winsize=700
    cuadriculade=10
    win = GraphWin('ches', 710, 710) # give title and dimensions
    global map1,mov,resolution, xi, yi, xf, yf, angle, acciones, path, actual, ima_de_ini, angulos, angulos2
    global inicio, final, actual, trip, rect
    resolution = 2
    map1 = int(raw_input('mapa?: '))
    xi = int(raw_input('x inicial?: '))
    yi = int(raw_input('y inicial?: '))
    angle = 90
    xf = int(raw_input('x final?: '))
    yf = int(raw_input('y final?: '))
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


    path,mov, acciones = astar.astar(map1, resolution, xi, yi, xf, yf, angle)



    arduino=serial.Serial(u'/dev/ardu',baudrate=9600, timeout = None)
        #arduino.setDTR(True)

    x=0
    updatemap()
    while(x<=len(mov)-1):
        mover=readwrite(arduino,acciones[x][0]) # angle movement
        angle = angle + acciones[x][0]
        
        obstacle=boundry
        dist = .5
        if (obstacle == 1 and (angle == 0 or angle == 90 or angle == -90 or angle == 180 or angle == 45 or angle == -45 or angle == -135 or angle == 135) ):
            
            if (angle== 0):
                writecsv(xi+dist,yi)
            elif(angle== -90):
                writecsv(xi,yi-dist)
            elif(angle== 90):
                writecsv(xi,yi+dist)
            elif(angle== 180):
                writecsv(xi-dist,yi)
            elif (angle== 45):
                writecsv(xi+dist,yi+dist)
            elif(angle== -45):
                writecsv(xi+dist,yi-dist)
            elif(angle== 135):
                writecsv(xi-dist,yi+dist)
            elif(angle== -135):
                writecsv(xi-dist,yi-dist)
            path,mov, acciones  = astar.astar(map1, resolution, xi, yi, xf, yf, angle)
            mover=readwrite(arduino,0)
            erase()
            updatemap()
            x=0
        elif (obstacle == 2 and (angle == 45 or angle == -45 or angle == -135 or angle == 135) ):
            if (angle== 45):
                writecsv(xi+dist,yi+dist)
            elif(angle== -45):
                writecsv(xi+dist,yi-dist)
            elif(angle== 135):
                writecsv(xi-dist,yi+dist)
            elif(angle== -135):
                writecsv(xi-dist,yi-dist)
            path,mov, acciones  = astar.astar(map1, resolution, xi, yi, xf, yf, angle)
            mover=readwrite(arduino,0)
            erase()
            updatemap()
            x=0


        else:
            mover=readwrite(arduino,acciones[x][1])
            actual.undraw()
            x=x+1
            movie=Point(xconverter(winsize, cuadriculade, path[x][0] / resolution),yconverter(winsize, cuadriculade, path[x][1] / resolution))
            actual=Image(movie,filepath+u'/'+angulos[mov[x]])
            actual.draw(win)
            xi = path[x][0] / 2
            yi = path[x][1] / 2
if __name__ == '__main__':
    start()

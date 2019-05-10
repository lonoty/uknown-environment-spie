from __future__ import absolute_import
import astar
import visactu
import struct
mapa=int(raw_input(u'mapa: '))
xi=int(raw_input(u'coordenada inicial en x :' ))
yi=int(raw_input(u'coordenada inicial en y :' ))
xf=int(raw_input(u'coordenada final en x :' ))
yf=int(raw_input(u'coordenada final en y :' ))
angle=90
resolution=int(raw_input(u'resolucion: ' ))
while True:
    path,mov,acciones=astar.astar(mapa,resolution,xi,yi,xf,yf,angle) #path/mov/acciones
    xi,yi,angle=visactu.visualizacion(mapa,path,xi,yi,xf,yf,resolution,angle,acciones)
    print (xi,yi,angle)

from numpy import cos,sin,arctan,arccos,sqrt
import numpy
from PyQt4.QtGui import QTableWidget

def tableSize(table):
    return table.rowCount(),table.columnCount()

def resizeTableCells(table,size):
    rows = table.rowCount()
    for i in range(rows):
        table.setRowHeight(i,size)
            
    columns = table.columnCount()
    for j in range(columns):
        table.setColumnWidth(j,size)
    
def sphericalToCartesian(coord):
    r = coord[0]
    theta=coord[1]
    phi=coord[2]
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)
    return [x,y,z]

def cartesianToSpherical(coord):
    x = coord[0]
    y= coord[1]
    z=coord[2]
    
    r = sqrt(x*x+y*y+z*z)
    theta = arccos(z/r)
    phi = arctan(y/x)
    
    return [r,theta,phi]

def polarToRectangular(r,theta):
    return r*cos(theta),r*sin(theta)

def rectangularToPolar(coord):
    x = coord[0]
    y= coord[1]
    return [(x*x+y*y)**(0.5),arctan(y/x)]

def magnitude(vector):
    r=0
    for x in vector:
        r +=x*x
    return r**(0.5)


    
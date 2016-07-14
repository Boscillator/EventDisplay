#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __coconut_hash__ = 0x6d33903c

# Compiled with Coconut version 1.1.1-post_dev [Brontosaurus]

"""
Event display program.
PLEASE NOTE: This uses Coconut (http://coconut-lang.org/)
"""

# Coconut Header: --------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
import __coconut__
_coconut_sys.path.remove(_coconut_file_path)
for name in dir(__coconut__):
    if not name.startswith("__"):
        globals()[name] = getattr(__coconut__, name)

# Compiled Coconut: ------------------------------------------------------------


__author__ = 'Fred Buchanan, oscillator.b@gmail.com'


import sys
import csv
import colorsys
import random
import itertools
import pyqtgraph as pg
from pyqtgraph import QtCore
from pyqtgraph import QtGui

#function for how much rounding should be done on vertesis
roundF = _coconut.functools.partial(round, ndigits=2)

#Scale factor to remove stupid squares
def times(x): return x * 10000

#Frozen set of tracking radii
trackingRings = _coconut.frozenset(((times)(41.05), (times)(70.16), (times)(98.88), (times)(255), (times)(340), (times)(430), (times)(520), (times)(610), (times)(696), (times)(782), (times)(868), (times)(965), (times)(1080)))

class Partical(_coconut.collections.namedtuple("Partical", "id, pid, status, mother1, mother2, px, py, pz, m, scale, pol, xProd, yProd, zProd, tau")):
    """Repersents a partical"""
    __slots__ = ()
    pass

class Vertex(_coconut.collections.namedtuple("Vertex", "x, y")):
    """Repersents a vertex"""
    __slots__ = ()
    def __new__(cls, x, y):
        return (datamaker(cls))(*(roundF(x), roundF(y)))

#Camps a value between mival and maxval
def clamp(value, minval, maxval): return sorted((minval, value, maxval))[1]

def getParticalRGBA(pid):
    scaledPid = 255 / abs(pid)
    rgb = colorsys.hsv_to_rgb(scaledPid, 1, 1)
    scaledRgb = (tuple)([clamp(v, 0, 1) * 255 for v in rgb])
    return scaledRgb + (255,)

class ParticalRendererItem(pg.GraphicsObject):
    """Renders the particals"""
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        for partical in self.data:
            color = getParticalRGBA(partical.pid)
            for x in color:
                if (x < 0) or (x > 255):
                    print(partical.pid, color)
            p.setPen(pg.mkPen(color))
            prodPos = QtCore.QPointF(partical.xProd, partical.yProd)
            momentumPos = QtCore.QPointF(partical.px + partical.xProd, partical.py + partical.yProd)
            p.drawLine(momentumPos, prodPos)
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
## boundingRect _must_ indicate the entire area that will be drawn on
## or else we will get artifacts and possibly crashing.
## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

class RingRendererItem(pg.GraphicsObject):
    """Renders a tracking ring"""
    def __init__(self, radii):
        pg.GraphicsObject.__init__(self)
        self.radii = radii
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        center = QtCore.QPoint(0, 0)

        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        for radius in self.radii:
            p.drawEllipse(center, radius, radius)
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
## boundingRect _must_ indicate the entire area that will be drawn on
## or else we will get artifacts and possibly crashing.
## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

def take(n, iter): return _coconut_igetitem(iter, _coconut.slice(None, n))
def first(iterator): return _coconut_igetitem(iterator, 0)

def getCsvFileByName(fileName): return open(fileName)
def getCsvReaderByFile(csvFile): return csv.DictReader(csvFile)
getCsvReader = _coconut_compose(getCsvReaderByFile, getCsvFileByName)



def loadParticalFromRow(row): return Partical((int)(row['id']), (int)(row['pid']), (int)(row['status']), (int)(row['mother1']), (int)(row['mother2']), (times)((float)(row['px'])), (times)((float)(row['py'])), (times)((float)(row['pz'])), (float)(row['m']), (float)(row['scale']), (float)(row['pol']), (times)((float)(row['xProd'])), (times)((float)(row['yProd'])), (times)((float)(row['zProd'])), (float)(row['tau']))

def loadParticals(reader): return (list)((_coconut.functools.partial(map, loadParticalFromRow))(reader))
def filterStableParticals(particals): return (list)(filter(lambda partical: (partical.status >= 0), particals))

def loadVertexFromPartical(partical): return Vertex(partical.xProd, partical.yProd)
def loadVertesis(particals): return (set)((_coconut.functools.partial(map, loadVertexFromPartical))(particals))


def getVertexXList(vertises): return [v.x for v in vertises]
def getVertexYList(vertises): return [v.y for v in vertises]
def getUniquePIDs(particals): return (set)([abs(partical.pid) for partical in particals])


def sample100(data): return random.sample(data, 100)

def usage(): print("Usage: EventDisplay <event.csv>")

if len(sys.argv) != 2:
    usage()

def main():
    win = pg.GraphicsWindow(title="Event Display")

    particals = (filterStableParticals)((loadParticals)(getCsvReader(sys.argv[1]))) #Get particals from file
    vertises = (loadVertesis)(particals) #Get vertesis from particals
    vertisesX = (getVertexXList)(vertises) #Get a list of the x cords of vertises
    vertisesY = (getVertexYList)(vertises) #Get a list of the y cords of vertises

    win = pg.GraphicsWindow()

#create rings item


#Plot Particals
    p1 = win.addPlot(name='Particals')
    (p1.addItem)((ParticalRendererItem)(particals))
    rings1 = RingRendererItem(trackingRings)
    (p1.addItem)(rings1)
    p1.setWindowTitle('Particals')

#Add color legend
    l = pg.LegendItem((100, 60), offset=(70, 30))
    l.setParentItem(p1.graphicsItem())
    for pid in getUniquePIDs(particals):
        color = getParticalRGBA(pid)
        plotDataItem = pg.PlotDataItem([0], [0], pen=pg.mkPen(color)) #Create a dummy set of data for use in legend
        l.addItem(plotDataItem, str(pid)) #Add the item to the ledgend

#Plot Vertieses
    p2 = win.addPlot(name='Vertieses')
    p2.plot(vertisesX, vertisesY, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(255, 255, 255, 200))
    rings2 = RingRendererItem(trackingRings)
    (p2.addItem)(rings2)
    p2.setWindowTitle('Vertieses')

#Link the plots pan
    p1.setXLink('Vertieses')
    p1.setYLink('Vertieses')



#Start application if stuff is going on
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

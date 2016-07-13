#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __coconut_hash__ = 0x549ec022

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

roundF = _coconut.functools.partial(round, ndigits=2)

import sys
import csv
import random
import pyqtgraph as pg
from pyqtgraph import QtCore
from pyqtgraph import QtGui

class Partical(_coconut.collections.namedtuple("Partical", "id, pid, status, mother1, mother2, px, py, pz, m, scale, pol, xProd, yProd, zProd, tau")):
    """Repersents a partical"""
    __slots__ = ()
    pass

class Vertex(_coconut.collections.namedtuple("Vertex", "x, y")):
    """Repersents a vertex"""
    __slots__ = ()
    def __new__(cls, x, y):
        return (datamaker(cls))(*(roundF(x), roundF(y)))

class ParticalRendererItem(pg.GraphicsObject):
    """Renders the particals"""
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        for partical in self.data:
            prodPos = QtCore.QPoint(partical.xProd, partical.yProd)
#prodPos = QtCore.QPoint(0,0)
            momentumPos = QtCore.QPoint(partical.px + partical.xProd, partical.py + partical.yProd)
#momentumPos = QtCore.QPoint(0,0)
            p.drawLine(momentumPos, prodPos)
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

def times(x): return x * 10000

def loadParticalFromRow(row): return Partical((int)(row['id']), (int)(row['pid']), (int)(row['status']), (int)(row['mother1']), (int)(row['mother2']), (times)((float)(row['px'])), (times)((float)(row['py'])), (times)((float)(row['pz'])), (float)(row['m']), (float)(row['scale']), (float)(row['pol']), (times)((float)(row['xProd'])), (times)((float)(row['yProd'])), (times)((float)(row['zProd'])), (float)(row['tau']))

def loadParticals(reader): return (list)((_coconut.functools.partial(map, loadParticalFromRow))(reader))

def loadVertexFromPartical(partical): return Vertex(partical.xProd, partical.yProd)
def loadVertesis(particals): return (set)((_coconut.functools.partial(map, loadVertexFromPartical))(particals))
def getVertexXList(vertises): return [v.x for v in vertises]
def getVertexYList(vertises): return [v.y for v in vertises]

def sample100(data): return random.sample(data, 100)

def usage(): print("Usage: EventDisplay <event.csv>")

if len(sys.argv) != 2:
    usage()

def main():
    win = pg.GraphicsWindow(title="Event Display")

    particals = (loadParticals)(getCsvReader(sys.argv[1])) #Get particals from file
    vertises = (loadVertesis)(particals) #Get vertesis from particals
    vertisesX = (getVertexXList)(vertises) #Get a list of the x cords of vertises
    vertisesY = (getVertexYList)(vertises) #Get a list of the y cords of vertises

    win = pg.GraphicsWindow()

#Plot Particals
    p1 = win.addPlot(name='Particals')
    (p1.addItem)((ParticalRendererItem)(particals))
    p1.setWindowTitle('Particals')

#Plot Vertieses
    p2 = win.addPlot(name='Vertieses')
    p2.plot(vertisesX, vertisesY, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(255, 255, 255, 200))
    p2.setWindowTitle('Vertieses')

#Link the plots pan
    p2.setXLink('Particals')
    p2.setYLink('Particals')



#Start application if stuff is going on
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

#!/usr/bin/env python

# A Python translation of the "enrichments" example of QwtPlot3D

import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QVBoxLayout,
                             QHBoxLayout, QSlider)
#(QApplication, QCheckBox, QComboBox, QDateTimeEdit,
#        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
#        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
#        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, #QTextEdit,
#        QVBoxLayout, QWidget)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.Qwt3D._Qwt3D import *
from PyQt5.Qwt3D.OpenGL import *

# enable all tracing options of the SIP generated bindings (requires -r option)
if False:
    import sip
    sip.settracemask(0x3f)

# translated from enrichments.cpp

class Bar(VertexEnrichment):

    def __init__(self, radius = 0.0, level = 1.0):
        VertexEnrichment.__init__(self)
        self.configure(radius, level)

    # init()
    
    def clone(self):
        return self

    # clone()
     
    def configure(self, radius, level):
        self.radius = radius
        self.level = level

    # configure()
        
    def drawBegin(self):
        self.diag = self.radius*(self.plot.hull().maxVertex
                                 - self.plot.hull().minVertex).length()
        glLineWidth(0)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1, 1)

    # drawBegin()
     
    def drawEnd(self):
        pass

    # drawEnd()

    def draw(self, pos):
        interval = self.plot.hull().maxVertex.z - self.plot.hull().minVertex.z
        numlevel = self.plot.hull().minVertex.z + self.level * interval
        interval /= 100
        if pos.z > numlevel - interval and pos.z < numlevel + interval:
            Label3D().draw(pos, self.diag, 2*self.diag)
         
        minz = self.plot.hull().minVertex.z

        # FIXME: rgbat = self.plot.dataColor()(pos)
        rgbat = self.plot.dataColor()(pos.x, pos.y, pos.z)
        rgbab = self.plot.dataColor()(pos.x, pos.y, minz)
 
        glBegin(GL_QUADS)
        glColor4d(rgbab.r, rgbab.g, rgbab.b, rgbab.a)
        glVertex3d(pos.x - self.diag, pos.y - self.diag, minz)
        glVertex3d(pos.x + self.diag, pos.y - self.diag, minz)
        glVertex3d(pos.x + self.diag, pos.y + self.diag, minz)
        glVertex3d(pos.x - self.diag, pos.y + self.diag, minz)
        
         
        if pos.z > numlevel - interval and pos.z < numlevel + interval:
            glColor3d(0.7, 0.0, 0.0)
        else:
            glColor4d(rgbat.r, rgbat.g, rgbat.b, rgbat.a)
             
        glVertex3d(pos.x-self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, pos.z)
        
        glColor4d(rgbab.r, rgbab.g,rgbat.b, rgbab.a)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, minz)
        glColor4d(rgbat.r,rgbat.g, rgbat.b, rgbat.a)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, pos.z)
        
        glColor4d(rgbab.r, rgbab.g, rgbat.b, rgbab.a)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, minz)
        glColor4d(rgbat.r, rgbat.g, rgbat.b, rgbat.a)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, pos.z)
        
        glColor4d(rgbab.r, rgbab.g, rgbat.b, rgbab.a)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, minz)
        glColor4d(rgbat.r, rgbat.g, rgbat.b, rgbat.a)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, pos.z)
        
        glColor4d(rgbab.r, rgbab.g, rgbat.b, rgbab.a)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, minz)
        glColor4d(rgbat.r, rgbat.g, rgbat.b, rgbat.a)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, pos.z)
        glEnd()
         
        glColor3d(0, 0, 0)
        glBegin(GL_LINES)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, minz)
 
        glVertex3d(pos.x-self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, pos.z)
        
        glVertex3d(pos.x-self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x-self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y-self.diag, pos.z)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, minz)
        glVertex3d(pos.x+self.diag, pos.y+self.diag, pos.z)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, minz)
        glVertex3d(pos.x-self.diag, pos.y+self.diag, pos.z)
        glEnd()

    # draw()

# class Bar


class Label3D:
 
    def __init__(self):
        pass

    # __init__()
     
    def draw(self, pos, w, h):
        gap = 0.3
        glColor3d(1,1,1)
        glBegin(GL_QUADS)
        glVertex3d(pos.x - w, pos.y, pos.z + gap);
        glVertex3d(pos.x + w, pos.y, pos.z + gap);
        glVertex3d(pos.x + w, pos.y, pos.z + gap + h)
        glVertex3d(pos.x - w, pos.y, pos.z + gap + h)
        glEnd()
        glColor3d(0.4,0,0)
        glBegin(GL_LINE_LOOP)
        glVertex3d(pos.x - w, pos.y,pos.z + gap)
        glVertex3d(pos.x + w, pos.y,pos.z + gap)
        glVertex3d(pos.x + w, pos.y,pos.z + gap + h)
        glVertex3d(pos.x - w, pos.y, pos.z + gap + h)
        glEnd()
        glBegin(GL_LINES)
        glVertex3d(pos.x, pos.y, pos.z)
        glVertex3d(pos.x, pos.y, pos.z + gap)
        glEnd()

    # draw()

# class Label3D


class Hat(Function):
 
    def __init__(self, *args):
        Function.__init__(self, *args)

    # __init__()
    
    def __call__(self, x, y):
        return 1.0/(x*x + y*y + 0.5)

    # __call__()

    def name(self):
        return QString('$\\frac{1}{x^2+y^2+\\frac{1}{2}}$')

    # name()

# class Hat


# translated from enrichmentmainwindow.cpp
 
class EnrichmentDemo(QWidget):
     
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        family = QCoreApplication.instance().font().family()

        plot = self.plot = SurfacePlot(self)
        plot.setTitle('Bar Style (Vertex Enrichment)')
        if 'Verdana' in QFontDatabase().families():
            family = 'Verdana'
        family = 'Courier'
            
        plot.setTitleFont(family, 16, QFont.Bold)
        plot.coordinates().setLabelFont(family, 14)
        plot.coordinates().setNumberFont(family, 12)

        plot.setZoom(0.8);
        plot.setRotation(30.0, 0.0, 15.0)

        plot.setCoordinateStyle(BOX)
        self.width = 0.007
        self.level = .5
        self.bar = plot.setPlotStyle(Bar(self.width, self.level))
   
        hat = Hat(plot)
        hat.setMesh(23, 21)
        hat.setDomain(-1.8, 1.7, -1.6, 1.7)
        hat.create()
        
        plot.setFloorStyle(FLOORDATA)
        
        axes = plot.coordinates().axes # alias
        for axis in axes:
            axis.setMajors(5)
            axis.setMinors(4)
             
        plot.coordinates().setGridLinesColor(RGBA(0.0, 0.0, 0.5))
        plot.coordinates().setLineWidth(1)
        plot.coordinates().setNumberFont(family, 8)
        plot.coordinates().adjustNumbers(5)

        self.setColor()
        
        plot.updateData();
        plot.updateGL();

        # Level
        levelLabel = QLabel('Level')
        levelSlider = QSlider(self)
        levelSlider.setValue(50);
        levelSlider.setTickPosition(QSlider.TicksRight)
        levelLayout = QVBoxLayout()
        levelLayout.addWidget(levelLabel)
        levelLayout.addWidget(levelSlider)

        levelSlider.valueChanged.connect(self.setLevel)

        # Layout
        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(plot)
        mainLayout.addLayout(levelLayout)
       
    # __init__()

    def setColor(self):
        i, step = 252, 4
        colorVector = ColorVector()
        while (i>=0):
            colorVector.push_back(RGBA(i/255.0, max((i-60)/255.0, 0.0), 0.0))
            step -= 1
            if step == 0:
                i -= 4
                step = 4
        color = StandardColor(self.plot)
        color.setColorVector(colorVector)
        self.plot.setDataColor(color)

    # setColor()

    def setLevel(self, level):
        self.level = 1.0 - 0.01*level;
        self.bar.configure(self.width, self.level)
        self.plot.updateData()
        self.plot.updateGL()

    # setLevel()
 
# class EnrichmentDemo


def make(): 
    demo = EnrichmentDemo()
    demo.show()
    # Matrox cards on Linux work better with a resize() after show()
    demo.resize(600, 400)
    return demo
 
# make()
 
 
def main(args):
    app = QApplication(args)
    demo = make()
    app.exec_()
 
# main()
 
 
# Admire
if __name__ == '__main__':
    main(sys.argv)
    
# Local Variables: ***
# mode: python ***
# End: ***

#!/usr/bin/env python

import sys
from PyQt4.Qt import QApplication, QCoreApplication, QFont, QFontDatabase
from PyQt4.Qt import QSplitter, QTimer, SIGNAL, Qt
from PyQt4.Qwt3D import *


class Saddle(Function):

    def __init__(self, *args):
        Function.__init__(self, *args)

        self.setDomain(-2.5, 2.5, -2.5, 2.5)
        self.setMaxZ(1.5)
        self.setMinZ(-1.5)
        self.setMesh(31,31)

    # __init__()
    
    def __call__(self, x, y):
        return x*y

    # __call__()

# class Saddle


class Hat(Function):

    def __init__(self, *args):
        Function.__init__(self, *args)

        self.setDomain(-1.5, 1.5, -1.5, 1.5)
        self.setMesh(41, 41)

    # __init__()
    
    def __call__(self, x, y):
        return 1.0/(x*x+y*y+0.3)

    # __call__()

# class Hat


class Plot(SurfacePlot):

    def __init__(self, parent, updateinterval):
        SurfacePlot.__init__(self, parent)
        # fonts
        family = QCoreApplication.instance().font().family()
        if 'Verdana' in QFontDatabase().families():
            family = 'Verdana'
        family = 'Courier'

        self.setTitleFont(family, 16, QFont.Bold)
            
        self.setRotation(30, 0, 15)
        self.setShift(0.1, 0, 0)
        self.setZoom(0.8)

        self.coordinates().setNumberFont(family, 8)
        
        axes = self.coordinates().axes # alias
        for axis in axes:
            axis.setMajors(7)
            axis.setMinors(4)

        axes[X1].setLabelString("x")
        axes[Y1].setLabelString("y")
        axes[Z1].setLabelString("z")
        axes[X2].setLabelString("x")
        axes[Y2].setLabelString("y")
        axes[Z2].setLabelString("z")
        axes[X3].setLabelString("x")
        axes[Y3].setLabelString("y")
        axes[Z3].setLabelString("z")
        axes[X4].setLabelString("x")
        axes[Y4].setLabelString("y")
        axes[Z4].setLabelString("z")

        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.rotate)
        timer.start(updateinterval)
        
    # __init__()

    def rotate(self):
        self.setRotation(int(self.xRotation()+2) % 360,
                         int(self.yRotation()+2) % 360,
                         int(self.zRotation()+2) % 360)

    # rotate()

# class Plot()


def make():
    demo = QSplitter(Qt.Horizontal)

    plot1 = Plot(demo, 30)
    plot1.setFloorStyle(FLOORISO)
    plot1.setCoordinateStyle(BOX)
    saddle = Saddle(plot1)
    saddle.create()
    plot1.setTitle("Autoswitching axes")
    plot1.setBackgroundColor(RGBA(1.0, 1.0, 0.6))
    plot1.makeCurrent()
    plot1.updateData()
    plot1.updateGL()
    
    plot2 = Plot(demo, 80)
    plot2.setZoom(0.8)
    hat = Hat(plot2)
    hat.create()
    plot2.setPlotStyle(HIDDENLINE)
    plot2.setFloorStyle(FLOORDATA)
    plot2.setCoordinateStyle(FRAME)
    plot2.setBackgroundColor(RGBA(1.0, 1.0, 0.6))
    plot2.makeCurrent()
    plot2.updateData()
    plot2.updateGL()

    demo.resize(800, 400)
    demo.show()
                
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

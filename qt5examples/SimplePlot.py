#!/usr/bin/env python

import sys
from math import log
from PyQt5.Qt import QApplication, QCoreApplication, QFont, QFontDatabase
from PyQt5.Qwt3D import Function, RGBA, SurfacePlot, BOX, X1, Y1, Z1

class Rosenbrock(Function):

    def __init__(self, *args):
        Function.__init__(self, *args)

    # __init__()

    def __call__(self, x, y):
        return log((1-x)*(1-x) + 100*(y-x*x)*(y-x*x)) / 8

    # __call__()

# class Rosenbrock


class Plot(SurfacePlot):
    
    def __init__(self, *args):
        SurfacePlot.__init__(self, *args)
        # fonts
        family = QCoreApplication.instance().font().family()
        if 'Verdana' in QFontDatabase().families():
            family = 'Verdana'
        family = 'Courier'
            
        self.coordinates().setLabelFont(family, 14)
        self.coordinates().setNumberFont(family, 12)
            
        self.setTitle('A Simple SurfacePlot Demonstration');
        self.setTitleFont(family, 16, QFont.Bold)
        self.setBackgroundColor(RGBA(1.0, 1.0, 0.6))

        rosenbrock = Rosenbrock(self)

        rosenbrock.setMesh(41, 31)
        rosenbrock.setDomain(-1.73, 1.5, -1.5, 1.5)
        rosenbrock.setMinZ(-10)
        
        rosenbrock.create()

        self.setRotation(30, 0, 15)
        self.setScale(1, 1, 1)
        self.setShift(0.15, 0, 0)
        self.setZoom(0.9)

        axes = self.coordinates().axes # alias
        for axis in axes:
            axis.setMajors(7)
            axis.setMinors(4)
            
        axes[X1].setLabelString('x-axis')
        axes[Y1].setLabelString('y-axis')
        axes[Z1].setLabelString('z-axis')

        self.setCoordinateStyle(BOX);

        self.updateData();
        self.updateGL();

    # __init__()

# class Plot


def make():
    demo = Plot()
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


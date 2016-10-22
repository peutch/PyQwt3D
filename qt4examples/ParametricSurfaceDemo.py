#!/usr/bin/env python

import sys
from math import cos, pi, sin
from PyQt4.Qt import QApplication, QCoreApplication, QFont, QFontDatabase, Qt
from PyQt4.Qwt3D import ParametricSurface, RGBA, SurfacePlot, Triple, NOCOORD

class Sphere(ParametricSurface):

    def __init__(self, *args):
        ParametricSurface.__init__(self, *args)
        self.setMesh(41, 31)
        self.setDomain(0, 2*pi, 0, pi)
        self.setPeriodic(False, False)

    # __init__()

    def __call__(self, u, v):
        r = 1.0
        return Triple(r*cos(u)*sin(v), r*sin(u)*sin(v), r*cos(v))

    # __call__()

# class Sphere

        
class Plot(SurfacePlot):

    def __init__(self, *args):
        SurfacePlot.__init__(self, *args)
        # fonts
        family = QCoreApplication.instance().font().family()
        if 'Verdana' in QFontDatabase().families():
            family = 'Verdana'

        family = 'Courier'
        self.setTitleFont(family, 16, QFont.Bold)
##         self.setTitleColor(RGBA(1.0, 0.0, 0.0))
        
        self.setTitle("A Simple Parametric Surface Demonstration")

        self.setBackgroundColor(RGBA(1.0, 1.0, 0.6))

        sphere = Sphere(self)
        sphere.create()

        self.setRotation(45, 15, 0)
        self.setCoordinateStyle(NOCOORD);
        self.updateData()
        self.updateGL()

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

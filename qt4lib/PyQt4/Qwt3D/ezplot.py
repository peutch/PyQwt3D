#ezplot is some sugar coating for Qwt3D

# Copyright (C) 2003-2007 Gerard Vermeulen
#
# This file is part of PyQwt3D.
#
# PyQwt3D is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyQwt3D is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# In addition, as a special exception, Gerard Vermeulen gives permission
# to link PyQwt3D dynamically with non-free versions of Qt and PyQt,
# and to distribute PyQwt3D in this form, provided that equally powerful
# versions of Qt and PyQt have been released under the terms of the GNU
# General Public License.
#
# If PyQwt3D is dynamically linked with non-free versions of Qt and PyQt,
# PyQwt3D becomes a free plug-in for a non-free program.

__all__ = ('plot',)

import numpy as np
from PyQt4.Qwt3D._Qwt3D import SurfacePlot, RGBA
from PyQt4.Qwt3D._Qwt3D import X1, X2, X3, X4, Y1, Y2, Y3, Y4, Z1, Z2, Z3, Z4


def tocube(x, y, z):
    """
    For arrays x, y, z, return scale factors sx and sy, so that dz=sx*dx and
    dz=sy*dy, where dx=max(x)-min(x), dy=max(y)-min(y), and dz=max(z)-min(z)
    """
    dx = float(x.max()-x.min())
    dy = float(y.max()-y.min())
    dz = float(z.max()-z.min())

    return dz/dx, dz/dy

# tocube()


# numpy.meshgrid() returns arrays with the wrong shape!
def meshgrid(x, y):
    """
    For vectors x, y with lengths Nx=len(x) and Ny=len(y), return X, Y
    where X and Y are (Nx, Ny) shaped arrays with the elements of x
    and y repeated to fill the matrix

    EG,

      X, Y = meshgrid([1,2,3], [4,5,6,7])

      X =
        1   1   1   1
        2   2   2   2
        3   3   3   3


      Y =
        4   5   6   7
        4   5   6   7
        4   5   6   7
    """
    x = np.asarray(x)
    y = np.asarray(y)
    numRows, numCols = len(x), len(y)  # not reversed, contrary to np.meshgrid
    x = x.reshape(numRows, 1)
    X = x.repeat(numCols, axis=1)

    y = y.reshape(1, numCols)
    Y = y.repeat(numRows, axis=0)
    return X, Y

# meshgrid()


def plot(x, y, function, title='', labels=('x', 'y', 'z')):
    """
    For vectors x and y, return a plot of function(x, y)
    """
    x = np.asarray(x)
    y = np.asarray(y)
    # numpy.meshgrid() produces arrays with the wrong shape!
    z = function(*meshgrid(x, y))
    sx, sy = tocube(x, y, z)

    w = SurfacePlot()
    if title:
        w.setTitle(title)
    w.setBackgroundColor(RGBA(1.0, 1.0, 1.0))
    w.setScale(1.0, 1.0, 1.0)
    w.setRotation(30, 0, 15)
    # antialiasing
    w.coordinates().setLineSmooth(True)
    w.setSmoothMesh(True)

    # Load the data with scaled end points for the x- and y-axis,
    # so that all axes have a similar length (within a factor 2).
    # Rescale the axes limits, so that the axes look correct.
    w.loadFromData(z, sx*x.min(), sx*x.max(), sy*y.min(), sy*y.max())
    axes = w.coordinates().axes
    for axis in (axes[X1],
                 axes[X2],
                 axes[X3],
                 axes[X4]):
        start, stop = axis.limits()
        axis.setLimits(start/sx, stop/sx)
        axis.setMajors(5)
        axis.setMinors(0)
        axis.setLabelString(labels[0])
    for axis in (axes[Y1],
                 axes[Y2],
                 axes[Y3],
                 axes[Y4]):
        start, stop = axis.limits()
        axis.setLimits(start/sy, stop/sy)
        axis.setMajors(5)
        axis.setMinors(0)
        axis.setLabelString(labels[1])
    for axis in (axes[Z1],
                 axes[Z2],
                 axes[Z3],
                 axes[Z4]):
        axis.setMajors(5)
        axis.setMinors(0)
        axis.setLabelString(labels[2])

    w.updateData()
    w.updateGL()
    w.show()
    return w

# plot()


def test():
    def xonly(x, _): return x
    def yonly(_, y): return y
    def saddle(x, y): return x*y
    def rosenbrock(x, y): return (1-x)**2+100*(y-x**2)**2
    def fantasy(x, y): return x*y*np.exp(4-x*x-y*y)

    a = plot(np.linspace(-3, 3), np.linspace(-1, 1), xonly,
             title="f(x, y) = x")
    b = plot(np.linspace(-3, 3), np.linspace(-1, 1), yonly,
             title="f(x, y) = y")
    c = plot(np.linspace(-3, 3), np.linspace(-3, 3), saddle,
             title="f(x, y) = x*y")
    d = plot(np.linspace(-3, 3), np.linspace(-3, 3), rosenbrock,
             title="f(x, y) = (1-x)**2 + 100*(y-x**2)**2")
    e = plot(np.linspace(-2, 2), np.linspace(-2, 2), fantasy,
             title="f(x, y) = x*y*exp(4-x**2-y**2))")
    raw_input('Happy? ')

# test()


# Local Variables: ***
# mode: python ***
# End: ***
    

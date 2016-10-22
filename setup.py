#!/usr/bin/env python

import time
from distutils.core import setup

name = 'PyQwt3D'
version = '0.1.7'
#version = '%04d%02d%02d' % (time.localtime()[:3])

long_description = """
PyQwt3D is a set of Python bindings for the QwtPlot3D C++ class library.
The QwtPlot3D library (http://qwtplot3d.sourceforge.net) extends the Qt
framework with widgets to visualize 3-dimensional data.
"""

setup(
    name             = name,
    version          = version,
    description      = "Python bindings for the QwtPlot3D library",
    url              = "http://pyqwt.sourceforge.net",
    author           = "Gerard Vermeulen",
    author_email     = "gerard.vermeulen@grenoble.cnrs.fr",
    license          = "GPL",
    long_description = long_description,
    platforms        = "Unix, Windows (MSVC), MacOS/X",
    )

# Local Variables: ***
# mode: python ***
# End: ***

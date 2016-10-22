"""Qwt3D -- a Python interface for the QwtPlot3D library.
"""
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

from _Qwt3D import *

try:
    from ezplot import *
except ImportError, message:
    if 'numpy' in message:
        print 'Install numpy to use ezplot'
    else:
        raise ImportError, message

def save(plot3d, name, format,
         landscape=VectorWriter.OFF,
         textmode=VectorWriter.NATIVE,
         sortmode=VectorWriter.BSPSORT):
    """save a snapshot a Plot3D widget to a file. 
    - plot3d    : the Plot3D widget or a widget with Plot3D widget as child
    - name      : the file name
    - format    : a case-insensitive string indicating the file format
    - landscape : VectorWriter.ON, OFF or AUTO
    - textmode  : VectorWriter.PIXEL, NATIVE, or TEX
    - sortmode  : VectorWriter.NOSORT, SIMPLESORT, or BSPSORT

    PyQwt3D uses GL2PS to support vector formats as EPS, EPS_GZ, PDF, PGF, PS,
    PS_GZ, SVG, and SVG_GZ. It uses Qt to support pixmap formats as GIF, JPEG,
    PNG, and others.
    
    Returns True on success and False on failure.
    """    
    format = format.upper()
    if format in ['EPS', 'EPS_GZ',
                  'PDF',
                  'PGF',
                  'PS', 'PS_GZ',
                  'SVG', 'SVG_GZ',
                  ]:
        gl2ps = IO.outputHandler(format)
        if gl2ps:
            gl2ps.setLandscape(landscape)
            gl2ps.setTextMode(textmode)
            gl2ps.setSortMode(sortmode)
    else:
        format = format.lower()

    return IO.save(plot3d, name, format)

# save()

# Local Variables: ***
# mode: python ***
# End: ***


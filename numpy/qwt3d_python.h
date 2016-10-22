// qwt3d_python.h:
// - return a handle to the data of contiguous numarray and Numeric arrays.
//
// Copyright (C) 2004-2007 Gerard Vermeulen
//
// This file is part of PyQwt3D.
//
// PyQwt3D is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// PyQwt3D is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with PyQwt3D; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


#ifndef QWT3D_PYTHON_H
#define QWT3D_PYTHON_H

#include <Python.h>

#ifdef HAS_NUMARRAY
// to hide numarray's import_array()
void qwt3d_import_numarray();
#endif // HAS_NUMARRAY

#ifdef HAS_NUMERIC
// to hide Numeric's import_array()
void qwt3d_import_numeric();
#endif // HAS_NUMERIC

#ifdef HAS_NUMPY
// to hide NumPy's import_array()
#if PY_MAJOR_VERSION >= 3
    int qwt3d_import_numpy();
#else
    void qwt3d_import_numpy();
#endif
#endif // HAS_NUMPY

// returns 1, 0, -1 in case of success, wrong object type, failure
int try_PyObject_to_PyArrayContiguousFloat2D(
    PyObject *in,
    PyObject **out, double **data, unsigned int *nx, unsigned int *ny);

// returns 1, 0, -1 in case of success, wrong object type, failure
int try_PyObject_to_PyArrayContiguousFloat3D(
    PyObject *in,
    PyObject **out, double **data, unsigned int *nx, unsigned int *ny, unsigned int *nz);

#endif // QWT3D_PYTHON_H

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// indent-tabs-mode: nil
// End:

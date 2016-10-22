// qwt3d_numeric.h: encapsulates all PyQwt3D's calls to the Numeric C-API.
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


#ifndef QWT3D_NUMERIC_H
#define QWT3D_NUMERIC_H

#include <Python.h>

#ifdef HAS_NUMERIC

int try_PyObject_to_NumericArrayContiguousFloat2D(
    PyObject *in,
    PyObject **out, double **data, unsigned int *nx, unsigned int *ny);

int try_PyObject_to_NumericArrayContiguousFloat3D(
    PyObject *in,
    PyObject **out, double **data, unsigned int *nx, unsigned int *ny, unsigned int *nz);

#endif // HAS_NUMERIC

#endif // QWT3D_NUMERIC_H

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// indent-tabs-mode: nil
// End:

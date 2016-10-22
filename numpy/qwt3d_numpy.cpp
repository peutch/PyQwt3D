// qwt3d_numeric.cpp: encapsulates all PyQwt3D's calls to the Numeric C-API.
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


#ifdef HAS_NUMPY

#include <Python.h>
#include <numpy/arrayobject.h>
#include <qwt3d_python.h>
#include <qwt3d_numpy.h>


#if PY_MAJOR_VERSION >= 3
    int qwt3d_import_numpy() {
        // this is a function which does error handling
        import_array();
        return 0;
    }
#else
    void qwt3d_import_numpy() {
        // this is a function which does error handling
        import_array();
    }
#endif


int try_PyObject_to_NumPyArrayContiguousFloat2D(
    PyObject *in,
    PyObject **out, double **data, unsigned int *nx, unsigned int *ny)
{
    if (!PyArray_Check(in))
        return 0;

    *out = PyArray_ContiguousFromObject(in, PyArray_DOUBLE, 2, 2);

    if (!*out) {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Failed to make contiguous 2D array of PyArray_DOUBLE");

        return -1;
    }

    *data = reinterpret_cast<double *>(
        reinterpret_cast<PyArrayObject *>(*out)->data);
    *nx = reinterpret_cast<PyArrayObject *>(*out)->dimensions[0];
    *ny = reinterpret_cast<PyArrayObject *>(*out)->dimensions[1];

    return 1;
}


int try_PyObject_to_NumPyArrayContiguousFloat3D(
    PyObject *in,
    PyObject **out, double **data, unsigned int *nx, unsigned int *ny, unsigned int *nz)
{
    if (!PyArray_Check(in))
        return 0;

    *out = PyArray_ContiguousFromObject(in, PyArray_DOUBLE, 3, 3);

    if (!*out) {
        PyErr_SetString(
            PyExc_RuntimeError,
            "Failed to make contiguous 3D array of PyArray_DOUBLE");

        return -1;
    }

    *data = reinterpret_cast<double *>(
        reinterpret_cast<PyArrayObject *>(*out)->data);
    *nx = reinterpret_cast<PyArrayObject *>(*out)->dimensions[0];
    *ny = reinterpret_cast<PyArrayObject *>(*out)->dimensions[1];
    *nz = reinterpret_cast<PyArrayObject *>(*out)->dimensions[2];

    return 1;
}

#endif // HAS_NUMPY

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// indent-tabs-mode: nil
// End:

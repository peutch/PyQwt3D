#!/usr/bin/python
"""
Generate the build tree and Makefiles for PyQwt3D.
"""
# Copyright (C) 2003-2008 Gerard Vermeulen
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


import compileall
import glob
import optparse
import os
import pprint
import re
import shutil
import sys
import traceback


class Die(Exception):
    def __init__(self, info):
        Exception.__init__(self, info)

    # __init__()

# class Die


try:
    required = 'At least SIP-4.5 and its development tools are required.'
    import sipconfig
except ImportError:
    raise Die(required)
if 0x040500 > sipconfig._pkg_config['sip_version']:
    raise Die(required)
del required


def get_pyqt_configuration(options):
    """Return the PyQt configuration for Qt3 or Qt4
    """

    if options.qt == 3:
        required = 'At least PyQt-3.17 and its development tools are required.'
        options.qwt3d = 'Qwt3D_Qt3'
        options.opengl = 'OpenGL_Qt3'
        options.excluded_features.append("-x HAS_QT4 -x HAS_QT5")
        try:
            import pyqtconfig as pyqtconfig
        except ImportError:
            raise Die(required)
        if 0x031100 > pyqtconfig._pkg_config['pyqt_version']:
            raise Die(required)
    elif options.qt == 4:
        required = 'At least PyQt-4.1 and its development tools are required.'
        options.qwt3d = 'Qwt3D_Qt4'
        options.opengl = 'OpenGL_Qt4'
        options.excluded_features.append("-x HAS_QT3 -x HAS_QT5")
        try:
            import PyQt4.pyqtconfig as pyqtconfig
        except ImportError:
            raise Die(required)
        if 0x040100 > pyqtconfig._pkg_config['pyqt_version']:
            raise Die(required)

    options.subdirs.extend([options.qwt3d, options.opengl])

    try:
        configuration = pyqtconfig.Configuration()
    except AttributeError:
        raise Die(
            'Check if SIP and PyQt or PyQt4 have been installed properly.'
            )

    return configuration

# get_pyqt_configuration()


def compile_qt_program(name, configuration,
                       extra_defines=[],
                       extra_include_dirs=[],
                       extra_lib_dirs=[],
                       extra_libs=[],
                       ):
    """Compile a simple Qt application.

    name is the name of the single source file
    configuration is the pyqtconfig.Configuration()
    extra_defines is a list of extra preprocessor definitions
    extra_include_dirs is a list of extra directories to search for headers
    extra_lib_dirs is a list of extra directories to search for libraries
    extra_libs is a list of extra libraries
    """    
    makefile = sipconfig.ProgramMakefile(
        configuration, console=True, qt=True, warnings=True)
    
    makefile.extra_defines.extend(extra_defines)
    makefile.extra_include_dirs.extend(extra_include_dirs)
    makefile.extra_lib_dirs.extend(extra_lib_dirs)
    makefile.extra_libs.extend(extra_libs)

    exe, build = makefile.build_command(name)

    # zap a spurious executable
    try:
        os.remove(exe)
    except OSError:
        pass

    os.system(build)

    if not os.access(exe, os.X_OK):
        return None

    if sys.platform != 'win32':
        exe = './' + exe

    return exe

# compile_qt_program()

    
def lazy_copy_file(source, target):
    """Lazy copy a file to another file:
    - check for a SIP time stamp to skip,
    - check if source and target do really differ,
    - copy the source file to the target if they do,
    - return True on copy and False on no copy.
    """
    if not os.path.exists(target):
        shutil.copy2(source, target)
        return True

    sourcelines = open(source).readlines()
    targetlines = open(target).readlines()

    # global length check
    if len(sourcelines) != len(targetlines):
        shutil.copy2(source, target)
        return True
    
    # skip a SIP time stamp 
    if (len(sourcelines) > 3
        and sourcelines[3].startswith(' * Generated by SIP')
        ):
        line = 4
    else:
        line = 0
        
    # line by line check
    while line < len(sourcelines):
        if sourcelines[line] != targetlines[line]:
            shutil.copy2(source, target)
            return True
        line = line + 1
        
    return False

# lazy_copy_file()


def copy_files(sources, directory):
    """Copy a list of files to a directory
    """ 
    for source in sources:
        shutil.copy2(source, os.path.join(directory, os.path.basename(source)))

# copy_files()


def check_numarray(configuration, options, package):
    '''See if the numarray extension has been installed.
    '''
    if options.disable_numarray:
        options.excluded_features.append("-x HAS_NUMARRAY")
        return options

    try:
        import numarray

        # Try to find numarray/arrayobject.h.
        numarray_inc = os.path.join(
            configuration.py_inc_dir, 'numarray', 'arrayobject.h')
        if os.access(numarray_inc, os.F_OK):
            print('Found numarray-%s.\n' % numarray.__version__)
            options.extra_defines.append('HAS_NUMARRAY')
        else:
            print(('numarray has been installed, '
                   'but its headers are not in the standard location.\n'
                   '%s will be build without support for numarray.\n'
                   '(Linux users may have to install a development package)\n'
                   ) % (package,))
            raise ImportError
    except ImportError:
        options.excluded_features.append('-x HAS_NUMARRAY')
        print(('Failed to import numarray: '
               '%s will be build without support for numarray.\n'
               ) % (package,))

    return options

# check_numarray()


def check_numeric(configuration, options, package):
    """See if the Numeric extension has been installed.
    """
    if options.disable_numeric:
        options.excluded_features.append('-x HAS_NUMERIC')
        return options

    try:
        import Numeric

        # Try to find Numeric/arrayobject.h.
        numeric_inc = os.path.join(
            configuration.py_inc_dir, 'Numeric', 'arrayobject.h')
        if os.access(numeric_inc, os.F_OK):
            print('Found Numeric-%s.\n' % Numeric.__version__)
            options.extra_defines.append('HAS_NUMERIC')
        else:
            print(('Numeric has been installed, '
                   'but its headers are not in the standard location.\n'
                   '%s will be build without support for Numeric.\n'
                   '(Linux users may have to install a development package)\n'
                   ) % (package,))
            raise ImportError
    except ImportError:
        options.excluded_features.append('-x HAS_NUMERIC')
        print(('Failed to find Numeric: '
               '%s will be build without support for Numeric.\n'
               ) % (package,))

    return options

# check_numeric()


def check_numpy(configuration, options, package):
    """See if the NumPy extension has been installed.
    """

    if options.disable_numpy:
        options.excluded_features.append('-x HAS_NUMPY')
        return options

    try:
        import numpy

        # Try to find numpy/arrayobject.h.
        from  numpy.distutils.misc_util import get_numpy_include_dirs
        include_dirs = get_numpy_include_dirs()
        for inc_dir in include_dirs:
            header = os.path.join(inc_dir, 'numpy', 'arrayobject.h')
            if os.access(header, os.F_OK):
                break
        else:
            print(('NumPy has been installed, '
                   'but its headers are not in the standard location.\n'
                   '%s will be build without support for NumPy.\n'
                   '(Linux users may have to install a development package)\n'
                   ) % (package,))
            raise ImportError
        print('Found NumPy-%s.\n' % numpy.__version__)
        options.extra_defines.append('HAS_NUMPY')
        options.extra_include_dirs.extend(include_dirs)
    except ImportError:
        options.excluded_features.append('-x HAS_NUMPY')
        print(('Failed to find NumPy: '
               '%s will be build without support for NumPy.\n'
               ) % (package,))

    return options

# check_numpy()


def check_sip(configuration, options, package):
    """Check if PyQwt3D can be built with SIP.
    """
    version = configuration.sip_version
    version_str = configuration.sip_version_str
    required = '%s requires at least SIP-4.5' % (package,)
    
    print("Found SIP-%s.\n" % version_str)

    if 0x040500 > version:
        raise SystemExit(required)

    options.extra_include_dirs.append(configuration.sip_inc_dir)

    return options

# check_sip()


def check_compiler(configuration, options, package):
    """Check compiler specifics
    """
    print('Do not get upset by error messages in the next 3 compiler checks:')

    makefile = sipconfig.Makefile(configuration=configuration)
    generator = makefile.optional_string('MAKEFILE_GENERATOR', 'UNIX')
    # FIXME: 'MSVC' should be worse than 'MSVC.NET'
    if generator in ['MSVC', 'MSVC.NET']:
        options.extra_cxxflags.extend(['-GR', '-GX'])
    
    program = os.linesep.join([
        r'#include <stddef.h>',
        r'class a { public: void f(size_t); };',
        r'void a::f(%s) {};',
        r'int main() { return 0; }',
        r'',
        ])
    name = "size_t_check.cpp"
    new = [
        '// Automagically generated by configure.py',
        '',
        '// Uncomment one of the following three lines',
        ]

    for ctype in ('unsigned int', 'unsigned long', 'unsigned long long'):
        open(name, "w").write(program % ctype)
        print("Check if 'size_t' and '%s' are the same type:" % ctype)
        if compile_qt_program(name, configuration):
            comment = ''
            print("YES")
        else:
            print("NO")
            comment =  '// '
        new.append('%stypedef %s size_t;' % (comment, ctype))

    new.extend(['',
                '// Local Variables:',
                '// mode: C++',
                '// c-file-style: "stroustrup"',
                '// End:',
                '',
                ])

    new = '\n'.join(new)
    types_sip = os.path.join(os.pardir, 'sip', 'types.sip')
    if os.access(types_sip, os.R_OK):
        old = open(types_sip, 'r').read()
    else:
        old = ''
    if old != new:
        open(types_sip, 'w').write(new)    

    return options

# check_compiler()


def check_os(configuration, options, package):
    """Adapt to different operating systems
    """
    print("Found '%s' operating system:" % os.name)
    print(sys.version)
    print()

    if os.name == 'nt':
        options.extra_defines.append('WIN32')

    return options

# check_os()


def fix_build_file(name, extra_sources, extra_headers, extra_moc_headers):
    """Extend the targets of a SIP build file with extra files 
    """
    
    keys = ('target', 'sources', 'headers', 'moc_headers')
    sbf = {}
    for key in keys:
        sbf[key] = []

    # Parse,
    nr = 0
    for line in open(name, 'r'):
        nr += 1
        if line[0] != '#':
            eq = line.find('=')
            if eq == -1:
                raise SystemExit(
                    '"%s\" line %d: Line must be in the form '
                    '"key = value value...."' % (name, nr))
        key = line[:eq].strip()
        value = line[eq+1:].strip()
        if key in keys:
            sbf[key].append(value)

    # extend,
    sbf['sources'].extend(extra_sources)
    sbf['headers'].extend(extra_headers)
    sbf['moc_headers'].extend(extra_moc_headers)

    # and write.
    output = open(name, 'w')
    for key in keys:
        if sbf[key]:
            output.write('%s = %s\n' % (key, ' '.join(sbf[key])))#, file=output)

# fix_build_file()


def setup_opengl_build(configuration, options, package):
    """Setup the OpenGL extension build
    """

    print('Setup the OpenGL package build.')
    
    build_dir = options.opengl
    tmp_dir = 'tmp-' + build_dir
    build_file = os.path.join(tmp_dir, '%s.sbf' % options.opengl)

    # zap the temporary directory
    try:
        shutil.rmtree(tmp_dir)
    except:
        pass
    # make a clean temporary directory
    try:
        os.mkdir(tmp_dir)
    except:
        raise Die('Failed to create the temporary build directory.')

    if options.qt == 3:
        pyqt_sip_flags = configuration.pyqt_qt_sip_flags
        sipfile = os.path.join(
            os.pardir, "sip", "OpenGL_Qt3_Module.sip")
    elif options.qt == 4:
        pyqt_sip_flags = configuration.pyqt_sip_flags
        sipfile = os.path.join(
            os.pardir, "sip", "OpenGL_Qt4_Module.sip")

    # invoke SIP
    cmd = ' '.join(
        [configuration.sip_bin,
         '-b', build_file,
         '-c', tmp_dir,
         options.jobs,
         options.trace,
         ]
        # SIP assumes POSIX style path separators
        + [sipfile.replace('\\', '/')]
        )

    print('sip invokation:')
    pprint.pprint(cmd)
    if os.path.exists(build_file):
        os.remove(build_file)
    os.system(cmd)
    if not os.path.exists(build_file):
        raise Die('SIP failed to generate the C++ code.')

    # copy lazily to the build directory to speed up recompilation
    if not os.path.exists(build_dir):
        try:
            os.mkdir(build_dir)
        except:
            raise Die('Failed to create the build directory.')

    lazy_copies = 0
    for pattern in ('*.c', '*.cpp', '*.h', '*.py', '*.sbf'):
        for source in glob.glob(os.path.join(tmp_dir, pattern)):
            target = os.path.join(build_dir, os.path.basename(source))
            if lazy_copy_file(source, target):
                print('Copy %s -> %s.' % (source, target))
                lazy_copies += 1
    print('%s file(s) lazily copied.' % lazy_copies)

    # module makefile
    if options.qt == 3:
        makefile = sipconfig.ModuleMakefile(
            configuration = configuration,
            build_file = os.path.basename(build_file),
            dir = build_dir,
            install_dir = options.module_install_path,
            #installs = installs,
            qt = 1,
            opengl = 1,
            warnings = 1,
            debug = options.debug,
            )
    elif options.qt == 4:
        # FIXME
        options.extra_include_dirs.append(
            os.path.join(configuration.qt_inc_dir, 'Qt'))
        makefile = sipconfig.ModuleMakefile(
            configuration = configuration,
            build_file = os.path.basename(build_file),
            dir = build_dir,
            install_dir = options.module_install_path,
            #installs = installs,
            qt = ['QtOpenGL'],
            opengl = 1,
            warnings = 1,
            debug = options.debug,
            )

    makefile.extra_cflags.extend(options.extra_cflags)
    makefile.extra_cxxflags.extend(options.extra_cxxflags)
    makefile.extra_defines.extend(options.extra_defines)
    makefile.extra_include_dirs.extend(options.extra_include_dirs)
    makefile.extra_lflags.extend(options.extra_lflags)
    makefile.extra_libs.extend(options.extra_libs)
    makefile.extra_lib_dirs.extend(options.extra_lib_dirs)
    makefile.generate()

# setup_opengl_build()


def nsis():
    """Generate the script for the Nullsoft Scriptable Install System.
    """
    try:
        from numpy.version import version as numpy_version
        from PyQt4.Qt import PYQT_VERSION_STR, QT_VERSION_STR
    except:
        return

    open('PyQwt3D.nsi', 'w').write(open('PyQwt3D.nsi.in').read() % {
        'PYQT_VERSION': PYQT_VERSION_STR,
        'PYTHON_VERSION': '%s.%s' % sys.version_info[:2],
        'QT_VERSION': QT_VERSION_STR,
        'NUMPY_VERSION': numpy_version,
        })

# nsis()


def setup_qwt3d_build(configuration, options, package):
    """Setup the Qwt3D extension build
    """

    print('Setup the Qwt3D package build.')

    # initialize
    build_dir = options.qwt3d
    tmp_dir = "tmp-%s" % options.qwt3d
    build_file = os.path.join(tmp_dir, "qwt3d.sbf")
    sip_dir = os.path.join(configuration.pyqt_sip_dir, 'Qwt3D')
    extra_sources = []
    extra_headers = []
    extra_moc_headers = []
    if configuration.qt_version < 0x040000:
        extra_py_files = glob.glob(
            os.path.join(os.pardir, 'qt3lib', 'Qwt3D', '*.py'))
    else:
        extra_py_files = glob.glob(
            os.path.join(os.pardir, 'qt4lib', 'PyQt4', 'Qwt3D', '*.py'))

    # do we compile and link the sources of QwtPlot3D into PyQwt3D?

    if options.qwtplot3d_sources:
        # yes, zap all 'qwtplot3d'
        while options.extra_libs.count('qwtplot3d'):
            options.extra_libs.remove('qwtplot3d')
    #elif ('qwtplot3d' not in options.extra_libs: Must be added manually. libqwtplot3d or libqwtplot3d-qt4 is ok
    #   no, add 'qwtplot3d' if needed
    #    options.extra_libs.append('qwtplot3d')

    # do we also compile and link the sources of zlib into PyQwt3D?
    if options.zlib_sources:
        options.extra_defines.append('HAVE_ZLIB')

    print("Extended options:")
    pprint.pprint(options.__dict__)
    print()
    
    # do we compile and link the sources of QwtPlot3D statically into PyQwt3D?
    if options.qwtplot3d_sources:
        extra_sources += glob.glob(os.path.join(
            options.qwtplot3d_sources, 'src', '*.cpp'))
        extra_sources += glob.glob(os.path.join(
            options.qwtplot3d_sources, '3rdparty', 'gl2ps', '*.c'))
        extra_headers += glob.glob(os.path.join(
            options.qwtplot3d_sources, 'include', '*.h'))
        extra_headers += glob.glob(os.path.join(
            options.qwtplot3d_sources, '3rdparty', 'gl2ps', '*.h'))
        extra_moc_headers = []
        for header in extra_headers:
            text = open(header).read()
            if re.compile(r'^\s*Q_OBJECT', re.M).search(text):
                extra_moc_headers.append(header)

    # do we compile and link the sources of zlib statically into PyQwt3D?
    if options.zlib_sources:
        examples = ('example.c', 'minigzip.c')
        for source in glob.glob(os.path.join(options.zlib_sources, '*.c')):
            if os.path.basename(source) not in examples:
                extra_sources.append(source)
        extra_headers += glob.glob(os.path.join(
            options.zlib_sources, '*.h'))

    # add the interface to the numerical Python extensions
    extra_sources += glob.glob(os.path.join(os.pardir, 'numpy', '*.cpp'))
    extra_headers += glob.glob(os.path.join(os.pardir, 'numpy', '*.h'))

    # add the extra headers which make protected data members accessible
    extra_headers += glob.glob(os.path.join(os.pardir, 'include', '*.h'))

    # put all code into a clean temporary directory
    try:
        shutil.rmtree(tmp_dir)
    except:
        pass
    try:
        os.mkdir(tmp_dir)
    except:
        raise SystemExit("Failed to create the temporary build directory")

    # copy the extra files
    copy_files(extra_sources, tmp_dir)
    copy_files(extra_headers, tmp_dir)
    copy_files(extra_moc_headers, tmp_dir)
    copy_files(extra_py_files, tmp_dir)

    # fix '#include "gl2ps".h' because gl2ps.h got relocated 
    if options.qwtplot3d_sources:
        for source in [os.path.join(tmp_dir, 'qwt3d_io_gl2ps.cpp')]:
            text = open(source).read()
            if -1 != text.find('../3rdparty/gl2ps/'): 
                open(source, 'w').write(text.replace('../3rdparty/gl2ps/', ''))

    if options.qt == 3:
        pyqt_sip_flags = configuration.pyqt_qt_sip_flags
        sipfile = os.path.join(
            os.pardir, "sip", "Qwt3D_Qt3_Module.sip")
    elif options.qt == 4:
        pyqt_sip_flags = configuration.pyqt_sip_flags
        sipfile = os.path.join(
            os.pardir, "sip", "Qwt3D_Qt4_Module.sip")
        
    # invoke SIP
    cmd = " ".join(
        [configuration.sip_bin,
         # SIP assumes POSIX style path separators
         #"-I", os.path.join(os.pardir, "sip").replace("\\", "/"),
         "-I", configuration.pyqt_sip_dir.replace("\\", "/"),
         "-b", build_file,
         "-c", tmp_dir,
         options.jobs,
         options.trace,
         pyqt_sip_flags,
         ]
        + options.sip_include_dirs
        + options.excluded_features
        + options.timelines
        # SIP assumes POSIX style path separators
        + [sipfile.replace("\\", "/")]
        )

    print("sip invokation:")
    pprint.pprint(cmd)
    print()

    if os.path.exists(build_file):
        os.remove(build_file)
    os.system(cmd)
    if not os.path.exists(build_file):
        raise SystemExit('SIP failed to generate the C++ code.')

    # FIXME: sip-4.7 does not generate those include files anymore
    for name in [os.path.join(tmp_dir, name) for name in [
        'sip_Qwt3DAxisVector.h',
        'sip_Qwt3DColorVector.h',
        'sip_Qwt3DCellField.h',
        'sip_Qwt3DDoubleVector.h',
        'sip_Qwt3DFreeVector.h',
        'sip_Qwt3DTriple.h',
        'sip_Qwt3DTripleField.h',
        ]]:
        if not os.path.exists(name):
            open(name, 'w')

    # fix the SIP build file
    fix_build_file(build_file,
                   [os.path.basename(f) for f in extra_sources],
                   [os.path.basename(f) for f in extra_headers],
                   [os.path.basename(f) for f in extra_moc_headers])
    
    # Windows fix: resolve the scope of POINTS in enumValues[]
    for source in glob.glob(os.path.join(tmp_dir, '*.cpp')):
        text = open(source).read()
        # sipNm__Qwt3D_POINTS changed between: SIP-4.2 and SIP-4.2.1
        if (-1 != text.find('{sipNm__Qwt3D_POINTS, POINTS')):
                text = text.replace('{sipNm__Qwt3D_POINTS, POINTS',
                                    '{sipNm__Qwt3D_POINTS, Qwt3D::POINTS')
                open(source, 'w').write(text)

    # copy lazily to the build directory to speed up recompilation
    if not os.path.exists(build_dir):
        try:
            os.mkdir(build_dir)
        except:
            raise SystemExit("Failed to create the build directory")

    lazy_copies = 0
    for pattern in ('*.c', '*.cpp', '*.h', '*.py', '*.sbf'):
        for source in glob.glob(os.path.join(tmp_dir, pattern)):
            target = os.path.join(build_dir, os.path.basename(source))
            if lazy_copy_file(source, target):
                print("Copy %s -> %s." % (source, target))
                lazy_copies += 1
    print("%s file(s) lazily copied." % lazy_copies)

    # byte-compile the Python files
    compileall.compile_dir(build_dir, 1, options.module_install_path)

    # files to be installed
    installs = []
    installs.append([[os.path.basename(f) for f in glob.glob(
        os.path.join(build_dir, '*.py*'))], options.module_install_path])
    for option in options.sip_include_dirs:
        # split and undo the POSIX style path separator
        directory = option.split()[-1].replace('/', os.sep)
        if directory.startswith(os.pardir):
            installs.append([[os.path.join(os.pardir, f) for f in glob.glob(
                os.path.join(directory, "*.sip"))], sip_dir])

    # module makefile
    if options.qt == 3:
        makefile = sipconfig.ModuleMakefile(
            configuration = configuration,
            build_file = os.path.basename(build_file),
            dir = build_dir,
            install_dir = options.module_install_path,
            installs = installs,
            qt = 1,
            opengl = 1,
            warnings = 1,
            debug = options.debug,
            )
    elif options.qt == 4:
        # FIXME
        options.extra_include_dirs.append(
            os.path.join(configuration.qt_inc_dir, 'Qt'))
        makefile = sipconfig.ModuleMakefile(
            configuration = configuration,
            build_file = os.path.basename(build_file),
            dir = build_dir,
            install_dir = options.module_install_path,
            installs = installs,
            qt = ['QtCore', 'QtGui', 'QtOpenGL'],
            opengl = 1,
            warnings = 1,
            debug = options.debug,
            )

    makefile.extra_cflags.extend(options.extra_cflags)
    makefile.extra_cxxflags.extend(options.extra_cxxflags)
    makefile.extra_defines.extend(options.extra_defines)
    makefile.extra_include_dirs.extend(options.extra_include_dirs)
    makefile.extra_lflags.extend(options.extra_lflags)
    makefile.extra_libs.extend(options.extra_libs)
    makefile.extra_lib_dirs.extend(options.extra_lib_dirs)
    makefile.generate()

    if options.qt == 4:
        nsis()

# setup_qwt3d_build()

    
def setup_parent_build(configuration, options):
    """Generate the parent Makefile
    """
    print("Setup the PyQwt3D build.")
     
    sipconfig.ParentMakefile(configuration = configuration,
                             subdirs = options.subdirs).generate()

# setup_parent_build()


def parse_args():
    """Return the parsed options and args from the command line
    """

    usage = (
        'python configure.py [options]'
        '\n\nEach option takes at most one argument, but some options'
        '\naccumulate arguments when repeated. For example, invoke:'
        '\n\n\tpython configure.py -I %s -I %s'
        '\n\nto search the current *and* parent directories for headers.'
        ) % (os.curdir, os.pardir)

    parser = optparse.OptionParser(usage=usage)

    common_options = optparse.OptionGroup(parser, 'Common options')
    common_options.add_option(
        '-3', '--qt3', action='store_const', const=3, dest='qt',
        help=('build for Qt3 and PyQt [default Qt4]'))
    common_options.add_option(
        '-4', '--qt4', action='store_const', const=4, dest='qt',
        default=4,
        help=('build for Qt4 and PyQt4 [default Qt4]'))
    common_options.add_option(
        '-Q', '--qwtplot3d-sources', default='', action='store',
        type='string', metavar='/sources/of/qwtplot3d',
        help=('compile and link the QwtPlot3D source files in'
              ' /sources/of/qwtplot3d statically into PyQwt3D'
              ' (required on Windows)'))
    common_options.add_option(
        '-Z', '--zlib-sources', default='', action='store',
        type='string', metavar='/sources/of/zlib',
        help=('compile and link the QwtPlot3D source files in'
              ' /sources/of/zlib statically into PyQwt3D'
              ' (the -Z option is ignored without the -Q option)'))
    common_options.add_option(
        '-D', '--extra-defines', default=[], action='append',
        type='string', metavar='HAVE_ZLIB',
        help=('add an extra preprocessor definition (HAVE_ZLIB enables'
              ' compression of EPS/PDF/PS/SVG output and HAVE_LIBPNG enables'
              ' pixmaps in the SVG output, but both defines are ignored'
              ' without the -Q option)'))
    common_options.add_option(
        '-I', '--extra-include-dirs', default=[], action='append',
        type='string', metavar='/usr/include/qwtplot3d',
        help=('add an extra directory to search for headers'
              ' (the compiler must be able to find the QwtPlot3D headers'
              ' without the -Q option)'))
    common_options.add_option(
        '-L', '--extra-lib-dirs', default=[], action='append',
        type='string', metavar='/usr/lib/qt3/lib',
        help=('add an extra directory to search for libraries'
              ' (the linker must be able to find the QwtPlot3D library'
              ' without the -Q option)'))
    common_options.add_option(
        '-j', '--jobs', default=0, action='store',
        type='int', metavar='N',
        help=('concatenate the SIP generated code into N files'
              ' [default 1 per class] (to speed up make by running '
              ' simultaneous jobs on multiprocessor systems)'))
    common_options.add_option(
        '-l', '--extra-libs', default=[], action='append',
        type='string', metavar='z',
        help=('add an extra library (to link the zlib library, you must'
              ' specify "zlib" or "zlib1" on Windows'
              ' and "z" on POSIX and MacOS/X)'))
    parser.add_option_group(common_options)

    make_options = optparse.OptionGroup(parser, 'Make options')
    make_options.add_option(
        '--debug', default=False, action='store_true',
        help='enable debugging symbols [default disabled]')
    make_options.add_option(
        '--extra-cflags', default=[], action='append',
        type='string', metavar='EXTRA_CFLAG',
        help='add an extra C compiler flag')
    make_options.add_option(
        '--extra-cxxflags', default=[], action='append',
        type='string', metavar='EXTRA_CXXFLAG',
        help='add an extra C++ compiler flag')
    make_options.add_option(
        '--extra-lflags', default=[], action='append',
        type='string', metavar='EXTRA_LFLAG',
        help='add an extra linker flag')
    parser.add_option_group(make_options)

    sip_options = optparse.OptionGroup(parser, 'SIP options')
    sip_options.add_option(
        '-x', '--excluded-features', default=[], action='append',
        type='string', metavar='EXTRA_SENSORY_PERCEPTION',
        help=('add a feature for SIP to exclude'
              ' (normally one of the features in sip/features.sip)'))
    sip_options.add_option(
        '-t', '--timelines', default=[], action='append',
        type='string', metavar='ESP_3_2_1',
        help=('add a timeline for SIP to adapt to a library version'
              ' (normally one of the timeline options in sip/timelines.sip)'))
    sip_options.add_option(
        '--sip-include-dirs', default=[os.path.join(os.pardir, 'sip')],
        action='append', type='string', metavar='SIP_INCLUDE_DIR',
        help='add an extra directory for SIP to search')
    sip_options.add_option(
        '--trace', default=False, action='store_true',
        help=('enable trace of the execution of the bindings'
              ' [default disabled]'))
    parser.add_option_group(sip_options)
    
    detection_options = optparse.OptionGroup(parser, 'Detection options')
    detection_options.add_option(
        '--disable-numarray', default=False, action='store_true',
        help='disable detection and use of numarray [default enabled]')
    detection_options.add_option(
        '--disable-numeric', default=False, action='store_true',
        help='disable detection and use of Numeric [default enabled]')
    detection_options.add_option(
        '--disable-numpy',
        default=False,
        action='store_true',
        help='disable detection and use of NumPy [default enabled]'
        )
    parser.add_option_group(detection_options)

    install_options = optparse.OptionGroup(parser, 'Install options')
    install_options.add_option(
        '--module-install-path', default='', action='store',
        help= 'specify the install directory for the Python modules'
        )
    parser.add_option_group(install_options)

    options, args =  parser.parse_args()
    
    # tweak some of the options to facilitate later processing
    if options.jobs < 1:
        options.jobs = ''
    else:
        options.jobs = '-j %s' % options.jobs
        
    options.excluded_features = [
        ('-x %s' % f) for f in options.excluded_features
        ]

    # SIP assumes POSIX style path separators
    options.sip_include_dirs = [
        ('-I %s' % f).replace('\\', '/') for f in options.sip_include_dirs
    ]
    
    options.timelines = [
        ('-t %s' % t) for t in options.timelines
        ]

    if options.trace:
        options.trace = '-r'
    else:
        options.trace = ''
        
    if options.qwtplot3d_sources == '':
        options.zlib_sources = ''

    if options.trace:
        options.trace = '-r'
        options.extra_defines.append('TRACE_PYQWT3D')
    else:
        options.trace = ''

    options.modules = []
    options.subdirs = []

    return options, args

# parse_args()


def main():
    
    # parse the command line
    options, args = parse_args()

    print("Command line options:")
    pprint.pprint(options.__dict__)
    print()

    configuration = get_pyqt_configuration(options)

    # extend the options
    options = check_sip(configuration, options, 'PyQwt3D')
    options = check_os(configuration, options, 'PyQwt3D')
    options = check_compiler(configuration, options, 'PyQwt3D')
    options = check_numarray(configuration, options, 'PyQwt3D')
    options = check_numeric(configuration, options, 'PyQwt3D')
    options = check_numpy(configuration, options, 'PyQwt3D')
    if not options.module_install_path:
        options.module_install_path = os.path.join(
            configuration.pyqt_mod_dir, 'Qwt3D')

    setup_opengl_build(configuration, options, 'PyQwt3D')
    setup_qwt3d_build(configuration, options, 'PyQwt3D')

    # main makefile
    sipconfig.ParentMakefile(
        configuration = configuration,
        subdirs = options.subdirs).generate()

# main()


if __name__ == "__main__":
    main()

# Local Variables: ***
# mode: python ***
# End: ***

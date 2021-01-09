"""The build configuration file for PyQwt3D, used by sip."""

import os
from os.path import abspath, join
from sipbuild import Option
import subprocess
from pyqtbuild import PyQtBindings, PyQtProject
import PyQt5


class Qwt3dProject(PyQtProject):
    """The Qwt3D Project class."""

    def __init__(self):
        super().__init__()
        self.bindings_factories = [Qwt3dBindings]

    def update(self, tool):
        """Allows SIP to find PyQt5 .sip files."""
        super().update(tool)
        self.sip_include_dirs.append(join(PyQt5.__path__[0], 'bindings'))


class Qwt3dBindings(PyQtBindings):
    """The Qwt3D Bindings class."""

    def __init__(self, project):
        super().__init__(project, name='Qwt3D',
                         sip_file='Qwt3D_Qt5_Module.sip',
                         qmake_QT=['widgets'])

    def get_options(self):
        """Our custom options that a user can pass to sip-build."""
        options = super().get_options()
        options += [
            Option('qwt3d_incdir',
                   help='the directory containing the Qwtplot3d header file',
                   metavar='DIR'),
            #Option('qwt3d_featuresdir',
            #       help='the directory containing the qwt.prf features file',
            #       metavar='DIR'),
            Option('qwt3d_libdir',
                   help='the directory containing the Qwt3D library',
                   metavar='DIR'),
            Option('qwt3d_lib',
                   help='the Qwt3D library',
                   metavar='LIB',
                   default='qwtplot3d'),
            Option('excluded_features', option_type=list)
        ]
        return options

    @staticmethod
    def run_pkg_config(option):
        output = subprocess.check_output(
            ['pkg-config', option, 'Qwt3D_Qt5_Module'],
            text=True)
        return output.rstrip()

    def apply_user_defaults(self, tool):
        """Apply values from user-configurable options."""
        self.include_dirs.append("numpy")
        if self.qwt3d_incdir is not None:
            self.include_dirs.append(self.qwt3d_incdir)
        #if self.qwt3d_featuresdir is not None:
        #    os.environ['QMAKEFEATURES'] = #abspath(self.qsci_features_dir)
        if self.qwt3d_libdir is not None:
            self.library_dirs.append(self.qwt3d_libdir)
        if self.qwt3d_lib is not None:
            self.libraries.append(self.qwt3d_lib)
        #excl = self.run_pkg_config('--excluded-features-x').split()
        #self.include_dirs.extend(
        #    flag[2:] for flag in excl if flag.startswith('-x'))
        self.disabled_features.append('HAS_QT3')
        self.disabled_features.append('HAS_QT4')
        self.disabled_features.append('HAS_NUMARRAY')
        self.disabled_features.append('HAS_NUMERIC')
        super().apply_user_defaults(tool)

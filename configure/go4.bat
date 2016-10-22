REM Example for "python configure.py [options]" on Windows
REM Edit the argument for the -Q option to suit your system

python configure.py -4 -Q ..\qwtplot3d-0.2.7 -Z ..\zlib-1.2.3 -D HAVE_ZLIB
nmake
nmake install

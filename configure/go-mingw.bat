REM Example for "python configure.py [options]" on Windows
REM Edit the argument for the -Q option to suit your system
REM Assumes that only libpng.a has been built in c:\build\libpng-1.2.18

python configure.py -4 -Q ..\qwtplot3d-0.2.7 -Z ..\zlib-1.2.3 -D HAVE_ZLIB -D HAVE_PNG -I c:\build\libpng-1.2.32 -L c:\build\libpng-1.2.32 -l png
make
make install

#!/usr/bin/env python

import inspect, sys
# iqt is part of PyQwt
from PyQt5.Qwt3D import Plot3D, save

get_input = input
# If this is Python 2, use raw_input()
if sys.version_info[:2] <= (2, 7):
    get_input = raw_input

def walk(p):
    if isinstance(p, Plot3D):
        yield p
    else:
        for c in p.children():
            for cc in walk(c):
               yield cc

# def walk()


def main():
    print(inspect.getsource(save))

    for demo in ['ParametricSurfaceDemo',
                 'SimplePlot',
                 'TestNumPy',
                 ]:
        result = __import__(demo).make()
        get_input("Is the demo looking HAPPY? ")

        for format in ('png', 'pdf', 'ps', 'eps', 'svg'):
            print('Saving %s.%s...' % (demo, format))
            if save(result, '%s.%s' % (demo, format), format):
                print('success')
            else:
                print('failure')

    for demo in ['AutoSwitch',
                 'EnrichmentDemo',
                 ]:
        result = __import__(demo).make()
        get_input("Is the demo looking HAPPY? ")

        for i, w in enumerate(walk(result)):
            for format in ('png', 'pdf', 'ps', 'eps', 'svg'):
                print('Saving %s%s.%s...' % (demo, i, format),)
                if save(w, '%s%s.%s' % (demo, i, format), format):
                    print('success')
                else:
                    print('failure')
            
# main()

if __name__ == '__main__':
    main()

# Local Variables: ***
# mode: python ***
# End: ***

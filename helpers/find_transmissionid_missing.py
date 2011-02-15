# -*- coding: utf-8 -*-
"""\
This module collects cables w/o transmission id.
"""
import re
from cablemap.core import cables_from_directory

def find_cables_without_tid(in_dir, knowncables):
    def want_cable(f):
        name = f[:f.rfind('.')]
        return name not in knowncables
    s = set(knowncables)
    s.update([cable.reference_id for cable in cables_from_directory(in_dir, want_cable) if not cable.partial and not cable.transmission_id])
    return s
    
if __name__ == '__main__':
    import os, codecs
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    filename = os.path.join(os.path.dirname(__file__), 'no_transmissionid.txt')
    f = codecs.open(filename, 'rb', 'utf-8')
    current = set([l.rstrip() for l in f])
    f.close()
    cables = find_cables_without_tid('./cable/', current)
    diff = cables ^ current
    if diff:
        print('difference: %r' % diff)
        f = codecs.open(filename, 'wb', 'utf-8')
        for ref in sorted(cables):
            f.write(ref)
            f.write('\n')


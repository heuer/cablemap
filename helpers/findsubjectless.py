# -*- coding: utf-8 -*-
"""\
This module collects cables w/o subject.
"""
import re
from cablemap.core import cables_from_directory

def find_cables_without_subject(in_dir, knowncables):
    def want_cable(f):
        name = f[:f.rfind('.')]
        print name
        print name not in knowncables
        return name not in knowncables
    s = set(knowncables)
    s.update([cable.reference_id for cable in cables_from_directory(in_dir, want_cable) if not cable.subject])
    return s
    
if __name__ == '__main__':
    import os, codecs
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    filename = os.path.join(os.path.dirname(__file__), 'no_subject.txt')
    f = codecs.open(filename, 'rb', 'utf-8')
    current = set([l.rstrip() for l in f])
    f.close()
    cables = find_cables_without_subject('./cable/', current)
    diff = cables ^ current
    if diff:
        print 'difference: ', diff
        f = codecs.open(filename, 'wb', 'utf-8')
        for ref in sorted(cables):
            f.write(ref)
            f.write('\n')


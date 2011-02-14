# -*- coding: utf-8 -*-
"""\
This module reports malformed cable ids.
"""
import os
import re
from cablemap.core.constants import REFERENCE_ID_PATTERN, MALFORMED_CABLE_IDS

def find_malformed_ids(in_dir):
    s = set()
    for root, dirs, files in os.walk(in_dir):
        for name in (n for n in files if '.html' in n):
            name = name[:name.rindex('.')]
            if not REFERENCE_ID_PATTERN.match(name):
                s.add(name)
    return s
    
if __name__ == '__main__':
    import os, codecs
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    current = set(MALFORMED_CABLE_IDS.keys())
    s = find_malformed_ids('./cable/')
    diff = s ^ current
    if diff:
        print 'difference: ', diff

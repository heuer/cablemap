# -*- coding: utf-8 -*-
"""\
This module reports malformed cable ids.
"""
import os
import re
from cablemap.core.constants import REFERENCE_ID_PATTERN, MALFORMED_CABLE_IDS, INVALID_CABLE_IDS

def find_malformed_ids(in_dir):
    dct = {}
    for root, dirs, files in os.walk(in_dir):
        for name in (n for n in files if '.html' in n):
            reference_id = name[:name.rindex('.')]
            if not REFERENCE_ID_PATTERN.match(reference_id):
                dct[reference_id] = os.path.join(root, name)
    return dct
    
if __name__ == '__main__':
    import os, codecs
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    current = set(MALFORMED_CABLE_IDS.keys()) | set(INVALID_CABLE_IDS.keys())
    dct = find_malformed_ids('./cable/')
    s = set(dct.keys())
    diff = s ^ current
    if diff:
        print('difference: %r' % diff)
        for ref in diff:
            print('%s: %s' % (ref, dct.get(ref)))

# -*- coding: utf-8 -*-
"""\
This module provides utility functions to convert cable(s)
to text.
"""
import codecs
from cablemap.core.reader import cable_from_file

def cable_to_text(cable, include_header):
    """\
    Returns the header/content of the cable as text.
    """
    if include_header:
        return '\n\n'.join(cable.header, cable.content)
    return cable.content

def generate_text_files(in_dir, out_dir, include_header=False):
    """\
    Walks through the `in_dir` and generates text versions of
    the cables in the `out_dir`.
    """
    for root, dirs, files in os.walk(in_dir):
        for name in files:
            if not name.rfind('.htm'):
                continue
            cable = cable_from_file(root + '/' + name)
            out = codecs.open(out_dir + '/' + cable.reference_id + '.txt', 'wb', encoding='utf-8')
            out.write(cable_to_text(cable, include_header))
            out.close()


if __name__ == '__main__':
    import os
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    if not os.path.isdir('./out/'):
        os.mkdir('./out')
    generate_text_files('./cable/', './out')

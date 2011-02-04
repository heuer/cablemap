# -*- coding: utf-8 -*-
"""\
This module converts cable(s) to text.

It expects a cable directory ./cable/ with the cables
and saves the cables as text (the filename is the reference
id of the cable).
"""
import codecs
from cablemap.core import cables_from_directory

def cable_to_text(cable, include_header):
    """\
    Returns the header/content of the cable as text.
    """
    if include_header:
        return u'\n\n'.join(cable.header, cable.content)
    return cable.content

def generate_text_files(in_dir, out_dir, include_header=False):
    """\
    Walks through the `in_dir` and generates text versions of
    the cables in the `out_dir`.
    """
    for cable in cables_from_directory(in_dir):
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

# -*- coding: utf-8 -*-
"""\
This module converts cables to JSON.

It expects a cable directory ./cable/ with the cables
and saves the cables as JSON (the filename is the reference
id of the cable).
"""
import codecs
from cablemap.core import cable_from_file
from cablemap.core.cableutils import cable_to_json

def generate_json_files(in_dir, out_dir):
    """\
    Walks through the `in_dir` and generates text versions of
    the cables in the `out_dir`.
    """
    for root, dirs, files in os.walk(in_dir):
        for name in [n for n in files if '.html' in n]:
            cable = cable_from_file(root + '/' + name)
            out = codecs.open(out_dir + '/' + cable.reference_id + '.json', 'wb', encoding='utf-8')
            out.write(cable_to_json(cable))
            out.close()


if __name__ == '__main__':
    import os
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    if not os.path.isdir('./out/'):
        os.mkdir('./out')
    generate_json_files('./cable/', './out')

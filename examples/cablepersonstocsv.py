# -*- coding: utf-8 -*-
"""\
This module tries to detect person names and assigns cable ids
to the mentioned person names.

Note: This script matches person names very naive. It's based on
string matching an cannot distinguish between the person JFK and
the airport JFK.

It expects a cable directory ./cable/ with the cables
and saves the cables into './cable2persons.csv'
"""
from __future__ import with_statement
import csv
import codecs
import cStringIO
from cablemap.core import cables_from_source

# Source: <http://docs.python.org/library/csv.html>
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def generate_csv(path, out):
    """\
    Walks through the `path` and generates the CSV file `out`
    """
    known_persons = ()
    with codecs.open(os.path.join(os.path.dirname(__file__), 'person_names.txt'), 'rb', 'utf-8') as f:
        known_persons = set((l.rstrip() for l in f))
    writer = UnicodeWriter(open(out, 'wb'), delimiter=';')
    for cable in cables_from_source(path):
        content = cable.content_body
        if not content:
            continue
        persons = [person for person in known_persons if person in content]
        if persons:
            row = [cable.reference_id]
            row.extend(persons)
            writer.writerow(row)


if __name__ == '__main__':
    import os
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    generate_csv('./cable/', './cable2persons.csv')

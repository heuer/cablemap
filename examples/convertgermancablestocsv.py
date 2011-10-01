# -*- coding: utf-8 -*-
"""\
This module shows how to use a predicate to filter
cables and converts cable(s) from Germany to CSV.
"""
import csv
import codecs
import cStringIO
from cablemap.core import cables_from_source, predicates as pred
from cablemap.core.utils import titlefy

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


def generate_csv(src, out):
    """\
    Walks through `src` and generates the CSV file `out`
    """
    writer = UnicodeWriter(open(out, 'wb'), delimiter=';')
    writer.writerow(('Reference ID', 'Created', 'Origin', 'Subject'))
    for cable in cables_from_source(src, predicate=pred.origin_filter(pred.origin_germany)):
        writer.writerow((cable.reference_id, cable.created, cable.origin, titlefy(cable.subject)))


if __name__ == '__main__':
    generate_csv('./cable/', './german-cables.csv')

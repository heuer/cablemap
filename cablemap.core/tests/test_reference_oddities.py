# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Several REF parsing tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

_TEST_DATA = (
        (u'01VATICAN5095', [u'99ROME2196']),
        (u'04THEHAGUE1919', [u'04USEUBRUSSELS3226']),
        (u'05BRASILIA1851', [u'05STATE127529', u'05STATE110840', u'05USUNNEWYORK1442']),
        (u'05PORTAUPRINCE1609', [u'05PORTAUPRINCE1537', u'05TOKYO3020', u'05OSLO868', u'05OTTAWA1734']),
        (u'06PORTAUPRINCE2187', [u'06PORTAUPRINCE1734', u'06PORTAUPRINCE1561']),
        (u'06SANJOSE2734', [u'06STATE19152', u'06SANJOSE2223', u'06SANJOSE1955']),
        (u'07LIMA2129', [u'07LIMA1841', u'07LIMA2000', u'07LIMA2009', u'07LIMA2026']),
        (u'07LIMA2323', [u'07LIMA2000', u'07LIMA2009', u'07LIMA2126', u'07LIMA2236']),
        (u'04HALIFAX40', [u'03OTTAWA1924', u'03OTTAWA566', u'03OTTAWA503', u'03HALIFAX58', u'02OTTAWA3205']),

    )


def test_references():
    def check(cable_id, references):
        cable = cable_by_id(cable_id)
        assert cable
        eq_(references, [ref.value for ref in cable.references if ref.is_cable()])
    for cable_id, refs in _TEST_DATA:
        yield check, cable_id, refs
    

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

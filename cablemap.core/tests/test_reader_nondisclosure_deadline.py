# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests non-disclosure deadline parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from cablemap.core.reader import parse_nondisclosure_deadline

_TEST_DATA = (
    # Input string, expected
    ('DEPT FOR WHA/BSC E.O. 12958: DECL: 11/22/2012 ', u'2012-11-22'),
    ('EO 12958 DECL: 2020/02/23', u'2020-02-23'),
    ('E.O. 12958: DECL: 11/03/2015', u'2015-11-03'),
    ('EO 12958 DECL: 12/31/2034', u'2034-12-31'),
    ('E.O. 12958 DECL: 12/31/2034', u'2034-12-31'),
    ('E.o. 12958: decl: 07/01/2034', u'2034-07-01'),
    (u'''E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu Subject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?
(U) Classifi''', u'2014-01-07'),
    (u'EO 12958: decl: 12/31/2034', u'2034-12-31'),
    (u'EO 12958: decl: 6/30/08', u'2008-06-30'),
    (u'EO 12958: decl: 6/3/08', u'2008-06-03'),
    (u'EO 12958: decl: 06/30/08', u'2008-06-30'),
    (u'E.O. 12958: N/A', None)
)

def test_non_disclosure_deadline():
    def check(content, expected):
        assert parse_nondisclosure_deadline(content) == expected
    for content, expected in _TEST_DATA:
        yield check, content, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

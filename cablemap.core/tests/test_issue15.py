# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against issue #15.
<https://github.com/heuer/cablemap/issues/#issue/15>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

_TEST_DATA = (
    # Cable id, expected subject
    ('06COPENHAGEN336', u"MOHAMMED CARTOONS: DENMARK WILL NOT PROSECUTE THE NEWSPAPER"),
    ('07OSLO320', u'NORWAY WILL FREEZE ANY SEPAH ASSETS'),
    ('08MOSCOW2426', u'TFGG01: ENERGY AND THE CONFLICT IN GEORGIA'),
)

def test_issue15():
    def check(cable, expected):
        eq_(expected, cable.subject)
    for ref, subject in _TEST_DATA:
        yield check, cable_by_id(ref), subject


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

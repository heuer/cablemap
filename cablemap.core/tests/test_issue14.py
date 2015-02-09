# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against issue #14.
<https://github.com/heuer/cablemap/issues/#issue/14>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

_TEST_DATA = (
    # Cable id, expected subject
    ('06GENEVA2654', u"LITTLE PROGRESS AND MUCH CONFUSION AND FRUSTRATION LEAD TO ADJOURNMENT OF HUMAN RIGHTS COUNCIL'S SECOND SESSION"),
    ('06GENEVA1673', u'HRC: SPECIAL SESSION ON PALESTINE'),
    ('07BERN881', u'FM CALMY-REY "TAKES NOTE" OF USG CONCERNS REGARDING IRAN/IAEA AND IRAN/EGL'),
    ('10STATE284', u'ESTABLISHING A DATE FOR THE INAUGURAL POLITICAL MILITARY DIALOGUE WITH LIBYA'),
    (u'03TEGUCIGALPA1725', u''),
    (u'04QUITO2502', u''),
    (u'04QUITO2879', u''),
    (u'06ABUJA1587', u''),
    (u'06BANGKOK5133', u''),
    (u'07CAIRO3070', u''),
    (u'08ANKARA588', u''),
    (u'08FREETOWN122', u''),
)

def test_issue14():
    def check(cable, expected):
        eq_(expected, cable.subject)
    for ref, subject in _TEST_DATA:
        yield check, cable_by_id(ref), subject


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

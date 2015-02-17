# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against 05DHAKA4483.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import ok_, eq_
from cablemap.core import cable_by_id


def test_issue():
    cable = cable_by_id('05DHAKA4483')
    assert cable
    ok_(cable.is_partial)
    eq_(u'Media Reaction: Iraq Constitution Bangladesh-U.S. Bilateral 9/11 anniversary; Dhaka', cable.subject)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

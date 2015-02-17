# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against 06ISLAMABAD5723.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import ok_, eq_
from cablemap.core import cable_by_id


def test_issue():
    cable = cable_by_id('06ISLAMABAD5723')
    assert cable
    ok_(not cable.is_partial)
    eq_(u'DEMARCHE DELIVERED: NEVADA TEST SITE', cable.subject)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

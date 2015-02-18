# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against 07YEREVAN202.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id


def test_issue():
    cable = cable_by_id('07YEREVAN202')
    assert cable
    eq_(u'CUSTOMS GIANT FALLS AMID RUMORS OF SMUGGLING AND CORRUPTION', cable.subject)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

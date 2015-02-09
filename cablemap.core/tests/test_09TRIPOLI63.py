# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against 09TRIPOLI63.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import ok_
from cablemap.core import cable_by_id


def test_issue():
    cable = cable_by_id('09TRIPOLI63')
    assert cable
    print cable.subject
    ok_(u'RISKY BUSINESS? AMERICAN CONSTRUCTION FIRM ENTERS JOINT VENTURE WITH GOL' in cable.subject)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

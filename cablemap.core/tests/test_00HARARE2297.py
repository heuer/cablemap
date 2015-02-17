# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests against 00HARARE2297.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_, ok_
from cablemap.core import cable_by_id


def test_issue():
    cable = cable_by_id('00HARARE2297')
    ok_(cable)
    ok_(cable.is_partial, 'Expected is_partial == True')
    signers = tuple(cable.signed_by)
    eq_(1, len(signers))
    eq_(u'MCDONALD', signers[0])



if __name__ == '__main__':
    import nose
    nose.core.runmodule()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against issue #12.
<https://github.com/heuer/cablemap/issues/#issue/12>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

def test_issue12_manama():
    cable = cable_by_id('08MANAMA492')
    eq_(u'VZCZCXRO5008', cable.transmission_id)
    eq_(u'08MANAMA492', cable.reference_id)
    eq_(u'08MANAMA492', cable.canonical_id)
    cable = cable_by_id('08ECTION01OF02MANAMA492')
    eq_(u'VZCZCXRO4772', cable.transmission_id)
    eq_(u'08ECTION01OF02MANAMA492', cable.reference_id)
    eq_(u'08MANAMA492', cable.canonical_id)

def test_issue12_saopaulo():
    cable = cable_by_id('08SAOPAULO335')
    eq_(u'VZCZCXRO3989', cable.transmission_id)
    eq_(u'08SAOPAULO335', cable.reference_id)
    eq_(u'08SAOPAULO335', cable.canonical_id)
    cable = cable_by_id('08SCTION02OF02SAOPAULO335')
    eq_(u'VZCZCXRO3727', cable.transmission_id)
    eq_('08SCTION02OF02SAOPAULO335', cable.reference_id)
    eq_(u'08SAOPAULO335', cable.canonical_id)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against issue #25.
<https://github.com/heuer/cablemap/issues/25>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

def test_issue25():
    cable = cable_by_id('09NAIROBI1938')
    refs = [ref.value for ref in cable.references if ref.is_cable()]
    eq_([u'08STATE81854', u'09NAIROBI1830', u'09NAIROBI1859', u'09NAIROBI1831'], refs)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

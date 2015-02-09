# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Test against issue #5.
<https://github.com/heuer/cablemap/issues/#issue/5>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id


def test_issue5():
    #
    # Note: The issue lists
    #   (B) Sao Paulo 215;
    #   (C) 05 Sao Paulo 975
    #
    # but the cable changed to:
    #   REF: A) Sao Paulo 319 B) Sao Paulo 278
    #
    # (2011-07-15)
    #
    cable = cable_by_id('06SAOPAULO348')
    assert cable
    refs = [ref.value for ref in cable.references if ref.is_cable()]
    assert u'06SAOPAULO319' in refs
    assert u'06SAOPAULO278' in refs
    eq_([u'PGOV', u'PHUM', u'KCRM', u'SOCI', u'SNAR', u'ASEC', u'BR'], cable.tags)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

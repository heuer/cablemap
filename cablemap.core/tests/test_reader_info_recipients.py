# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests INFO recipient parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.models import Recipient
from cablemap.core.reader import parse_info_recipients

_TEST_DATA = (
    # input string, optional reference_id, expected

    # 08STATE23763
    ('''FM SECSTATE WASHDC
TO PAGE 02        STATE   023763  071504Z
AMEMBASSY NEW DELHI PRIORITY
INFO MISSILE TECHNOLOGY CONTROL REGIME COLLECTIVE PRIORITY''',
     [Recipient(None, u'MISSILE TECHNOLOGY CONTROL REGIME COLLECTIVE', u'PRIORITY')]),
    ('''TO AMEMBASSY NEW DELHI PRIORITY
INFO RUEHTH/AMEMBASSY ATHENS 0121
RUEUITH/DET 1 39LG ANKARA TU''',
     [Recipient(u'RUEHTH', u'AMEMBASSY ATHENS', mcn=u'0121'),
      Recipient(u'RUEUITH', u'DET 1 39LG ANKARA TU')]),
    # 08STATE125686
    ('''R 270230Z NOV 08
FM SECSTATE WASHDC
INFO AMEMBASSY PANAMA''',
     [Recipient(None, u'AMEMBASSY PANAMA')]),
    ('''INFO AMEMBASSY PANAMA''',
     [Recipient(None, u'AMEMBASSY PANAMA')]),
    ('''INFO RUEHTH/AMEMBASSY ATHENS 0121
RHMFIUU/39OS INCIRLIK AB TU''',
     [Recipient(u'RUEHTH', u'AMEMBASSY ATHENS', mcn=u'0121'),
      Recipient(u'RHMFIUU', u'39OS INCIRLIK AB TU')]),
    ('''INFO XMT FOOBAR''',
     []),
    # 08STATE50524
    ('''TO AMEMBASSY BEIJING IMMEDIATE
INFO PAGE 02        STATE   050524  131535Z
AMEMBASSY BAGHDAD PRIORITY''',
     [Recipient(None, u'AMEMBASSY BAGHDAD', u'PRIORITY')]),
    # 89STATE401887.
    ('''O P 190243Z DEC 89
FM SECSTATE WASHDC
TO ALL AMERICAN REPUBLIC DIPLOMATIC POSTS IMMEDIATE
ALL OECD CAPITALS
AMEMBASSY MOSCOW IMMEDIATE
AMEMBASSY TOKYO IMMEDIATE
AMEMBASSY MANAGUA
INFO ALL DIPLOMATIC AND CONSULAR POSTS PRIORITY
XMT USINT HAVANA''',
     [Recipient(None, u'ALL DIPLOMATIC AND CONSULAR POSTS', u'PRIORITY', excluded=[u'USINT HAVANA'])]),

)


def test_recipients():
    def check(header, expected):
        eq_(expected, parse_info_recipients(header))
    for header, expected in _TEST_DATA:
        yield check, header, expected

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

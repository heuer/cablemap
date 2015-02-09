# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests recipient parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.models import Recipient
from cablemap.core.reader import parse_recipients

_TEST_DATA = (
    # input string, optional reference_id, expected

    # 09STATE15113
    ('''P 182318Z FEB 09
FM SECSTATE WASHDC
TO PAGE 02        STATE   015113  182333Z 
ALL DIPLOMATIC POSTS COLLECTIVE PRIORITY
AMEMBASSY TRIPOLI PRIORITY''',
    [Recipient(None, u'ALL DIPLOMATIC POSTS COLLECTIVE', u'PRIORITY'),
     Recipient(None, u'AMEMBASSY TRIPOLI', u'PRIORITY')]),
    # 89STATE403378
    ('''O 201405Z DEC 89
FM SECSTATE WASHDC
TO SPECIAL EMBASSY PROGRAM NIACT IMMEDIATE
AMCONSUL LENINGARD NIACT IMMEDIATE''',
    [Recipient(None, u'SPECIAL EMBASSY PROGRAM', u'NIACT IMMEDIATE'),
     Recipient(None, u'AMCONSUL LENINGARD', u'NIACT IMMEDIATE')]),
    # 09BAKU179
    ('''P 061232Z MAR 09
FM AMEMBASSY BAKU
TO SECSTATE WASHDC PRIORITY 0872''',
     [Recipient(None, u'SECSTATE WASHDC', u'PRIORITY', u'0872')]),
    # 08BEIJING332
    ('''FM AMEMBASSY BEIJING
TO RUEHC/SECSTATE WASHDC IMMEDIATE 4696
INFO RUEHOO/CHINA POSTS COLLECTIVE''',
     [Recipient(u'RUEHC', u'SECSTATE WASHDC', u'IMMEDIATE', u'4696')]),
    # 08STATE23763
    ('''FM SECSTATE WASHDC
TO PAGE 02        STATE   023763  071504Z
AMEMBASSY NEW DELHI PRIORITY
INFO MISSILE TECHNOLOGY CONTROL REGIME COLLECTIVE PRIORITY''',
     [Recipient(None, u'AMEMBASSY NEW DELHI', u'PRIORITY')]),
    # Example from 5 FAH-2 H-321.9 Format Line 9 (FL9): Addressee Exemptions (XMT Prosign)
    (u'''FM AMEMBASSY FOOBAR
TO RUEHC/SECSTATE WASHDC IMMEDIATE 3355
RUEHX/EUROPEAN POLITICAL COLLECTIVE
XMT/AMEMBASSY SOFIA
AMEMBASSY BUCHAREST''',
     [Recipient(u'RUEHC', u'SECSTATE WASHDC', u'IMMEDIATE', u'3355'),
      Recipient(u'RUEHX', u'EUROPEAN POLITICAL COLLECTIVE',
                excluded=[u'AMEMBASSY SOFIA', u'AMEMBASSY BUCHAREST'])]),
    # Variation of the previous test
    (u'''FM AMEMBASSY FOOBAR
TO RUEHC/SECSTATE WASHDC IMMEDIATE 3355
RUEHX/EUROPEAN POLITICAL COLLECTIVE
XMT AMEMBASSY SOFIA
AMEMBASSY BUCHAREST''',
     [Recipient(u'RUEHC', u'SECSTATE WASHDC', u'IMMEDIATE', u'3355'),
      Recipient(u'RUEHX', u'EUROPEAN POLITICAL COLLECTIVE',
                excluded=[u'AMEMBASSY SOFIA', u'AMEMBASSY BUCHAREST'])]),
)


def test_recipients():
    def check(header, expected):
        eq_(expected, parse_recipients(header))
    for header, expected in _TEST_DATA:
        yield check, header, expected

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
)


def test_recipients():
    def check(header, expected):
        eq_(expected, parse_recipients(header))
    for header, expected in _TEST_DATA:
        yield check, header, expected

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

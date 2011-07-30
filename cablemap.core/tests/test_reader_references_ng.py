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
Tests references parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.reader import parse_references
from cablemap.core.models import Reference
from cablemap.core.constants import REF_KIND_CABLE as CABLE, REF_KIND_EMAIL as EMAIL

def cable(value, enum=None):
    return Reference(value, CABLE, enum)

def mail(value, enum=None):
    return Reference(value, EMAIL, enum)

_TEST_DATA = (
    # input string, year, expected

    # 09DUBLIN524
    ('''REF: LAKHDHIR E-MAIL 12/01/09 ''',
     2009,
     [Reference(u'LAKHDHIR E-MAIL 12/01/09', EMAIL)]),
    # 08DUBLIN382
    ('''REF: INGALLS (S/CT) E-MAIL OF 04/15/2008 ''',
     2008,
     [Reference(u'INGALLS (S/CT) E-MAIL OF 04/15/2008', EMAIL)]),
    # 07TALLINN375
    ('\nREF: A) TALLINN 366 B) LEE-GOLDSTEIN EMAIL 05/11/07 \nB) TALLINN 347 ', 2007,
     [Reference(u'07TALLINN366', CABLE, u'A'),
      Reference(u'LEE-GOLDSTEIN EMAIL 05/11/07', EMAIL, u'B'),
      Reference(u'07TALLINN347', CABLE, u'B')]),
    # 07STATE156011
    ('  REF: LA PAZ 2974', 2007,
     [Reference(u'07LAPAZ2974', CABLE)]),
    #08RIYADH1134
    ('\nREF: A. SECSTATE 74879 \n     B. RIYADH 43 \n',
     2008,
     [Reference(u'08STATE74879', CABLE, u'A'),
      Reference(u'08RIYADH43', CABLE, u'B')]),
    # 09LONDON2697
    ('''REF: A. REF A STATE 122214 B. REF B LONDON 2649 C. REF C LONDON 2638 ''',
     2009,
     [cable(u'09STATE122214', u'A'),
      cable(u'09LONDON2649', u'B'),
      cable(u'09LONDON2638', u'C')]),
    # 04BRASILIA2863
    ('''REF: A. BRASILIA 2799 AND 2764 ¶B. PORT AU PRINCE 2325 ''',
     2004,
     [cable(u'04BRASILIA2799', u'A'),
      cable(u'04BRASILIA2764', u'A'),
      cable(u'04PORTAUPRINCE2325', u'B')]),
     
)

def test_parse_references():
    def check(content, year, expected):
        eq_(expected, parse_references(content, year))
    for content, year, expected in _TEST_DATA:
        yield check, content, year, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

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
from cablemap.core import constants

def cable(value, enum=None):
    return Reference(value, constants.REF_KIND_CABLE, enum)

def mail(value, enum=None):
    return Reference(value, constants.REF_KIND_EMAIL, enum)

def fam(value, enum=None):
    return Reference(value, constants.REF_KIND_FAM, enum)

def tel(value, enum=None):
    return Reference(value, constants.REF_KIND_TEL, enum)

_TEST_DATA = (
    # input string, year, expected

    # 09DUBLIN524
    (u'''REF: LAKHDHIR E-MAIL 12/01/09 ''',
     2009,
     [mail(u'LAKHDHIR E-MAIL 12/01/09')]),
    # 08DUBLIN382
    (u'''REF: INGALLS (S/CT) E-MAIL OF 04/15/2008 ''',
     2008,
     [mail(u'INGALLS (S/CT) E-MAIL OF 04/15/2008')]),
    # 07TALLINN375
    (u'\nREF: A) TALLINN 366 B) LEE-GOLDSTEIN EMAIL 05/11/07 \nB) TALLINN 347 ', 2007,
     [cable(u'07TALLINN366', u'A'),
      mail(u'LEE-GOLDSTEIN EMAIL 05/11/07', u'B'),
      cable(u'07TALLINN347', u'B')]),
    # 07STATE156011
    (u'  REF: LA PAZ 2974', 2007,
     [cable(u'07LAPAZ2974')]),
    #08RIYADH1134
    (u'\nREF: A. SECSTATE 74879 \n     B. RIYADH 43 \n',
     2008,
     [cable(u'08STATE74879', u'A'),
      cable(u'08RIYADH43', u'B')]),
    # 09LONDON2697
    (u'''REF: A. REF A STATE 122214 B. REF B LONDON 2649 C. REF C LONDON 2638 ''',
     2009,
     [cable(u'09STATE122214', u'A'),
      cable(u'09LONDON2649', u'B'),
      cable(u'09LONDON2638', u'C')]),
    # 04BRASILIA2863
    (u'''REF: A. BRASILIA 2799 AND 2764 ¶B. PORT AU PRINCE 2325 ''',
     2004,
     [cable(u'04BRASILIA2799', u'A'),
      cable(u'04BRASILIA2764', u'A'),
      cable(u'04PORTAUPRINCE2325', u'B')]),
    # 09SAOPAULO332
    (u'''Ref: 9 FAM Appendix K, 406 (6)''',
     2009,
     [fam(u'9 FAM Appendix K, 406 (6)')]),
    # 10SANAA317
    (u'''SUBJECT: (S/NF) SPIKE IN NATIONAL SECURITY-RELATED ARREST
CASES STRAINS POST,S RESOURCES

REF: A. SANAA 71
¶B. SANAA 151
¶C. SANAA 173
¶D. SANAA 230
¶E. SANAA 289
¶F. 09 SANAA 720
¶G. SANAA 202
¶H. MITCHELL/SIMS TELCON 02/16/2010
¶I. MITCHELL/SIMS EMAIL 02/16/2010
¶J. SANAA 214

Classified By: Ambassador
''',
     2010,
     [cable(u'10SANAA71', u'A'), cable(u'10SANAA151', u'B'), cable(u'10SANAA173', u'C'),
      cable(u'10SANAA230', u'D'), cable(u'10SANAA289', u'E'), cable(u'09SANAA720', u'F'),
      cable(u'10SANAA202', u'G'), tel(u'MITCHELL/SIMS TELCON 02/16/2010', u'H'),
      mail(u'MITCHELL/SIMS EMAIL 02/16/2010', u'I'), cable(u'10SANAA214', u'J')]),
    # 09LONDON2697
    (u'''REF: A. REF A STATE 122214 B. REF B LONDON 2649 C. REF C LONDON 2638 ''',
     2009,
     [cable(u'09STATE122214', u'A'), cable(u'09LONDON2649', u'B'), cable(u'09LONDON2638', u'C')]),
    # 86BRASILIA13835
    (u'''SUBJECT:  THE BRAZILIAN CONNECTION WITH IRAN AND 
THE CONTRAS 
 
REFS: (A)BRASILIA 13511, (B)BRASILIA 4799 
 
1.  (U)''',
     1986,
    [cable(u'86BRASILIA13511', u'A'), cable(u'86BRASILIA4799', u'B')]),
)

def test_parse_references():
    def check(content, year, expected):
        eq_(expected, parse_references(content, year))
    for content, year, expected in _TEST_DATA:
        yield check, content, year, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

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

def book(value, enum=None):
    return Reference(value, constants.REF_KIND_BOOK, enum)

def tel(value, enum=None):
    return Reference(value, constants.REF_KIND_TEL, enum)

def report(value, enum=None):
    return Reference(value, constants.REF_KIND_REPORT, enum)

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
     [book(u'9 FAM Appendix K, 406 (6)')]),
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
    # 09CAIRO2390
    (u'''REF: E-mails J. Speaks-K. Allen ''',
     2009,
     [mail(u'E-mails J. Speaks-K. Allen')]),
    # 05OTTAWA2105
    (u'''Ref: [A] State 188314, 259032, [B] Ottawa 2285 ''',
     2005,
     [cable(u'05STATE188314', u'A'), cable(u'05OTTAWA2285', u'B')]),
    # No cable
    (u'''REF: 08 STATE 1234; E-Mail Tralala; 05 STATE 1234; 06 STATE 1234''',
     2008,
     [cable(u'08STATE1234'), mail(u'E-Mail Tralala'), cable('05STATE1234'),
      cable(u'06STATE1234')]),
    # No cable
    (u'''REF: E-Mail Tralala; 05 STATE 1234; 06 STATE 1234''',
     2008,
     [mail(u'E-Mail Tralala'), cable('05STATE1234'),
      cable(u'06STATE1234')]),
    # No cable
    (u'''REF: 05 STATE 1234; 06 STATE 1234; E-Mail Tralala ''',
     2008,
     [cable('05STATE1234'), cable(u'06STATE1234'),
      mail(u'E-Mail Tralala')]),
    # 03COLOMBO2183
    (u'''Refs:  (A) State 348254 
-      (B) State 348253 -      (C) Colombo 2179, and previous ''',
     2003,
     [cable(u'03STATE348254', u'A'), cable(u'03STATE348253', u'B'),
      cable(u'03COLOMBO2179', u'C')]),
    # 04BRASILIA2680
    (u'''REF:   A) BRASILIA 2605, B) BRASILIA 2447, C) RIO 
 
DE JANEIRO 1291 ''',
     2004,
     [cable(u'04BRASILIA2605', u'A'), cable(u'04BRASILIA2447', u'B'),
      cable(u'04RIODEJANEIRO1291', u'C')]),
    # 05PANAMA555
    (u'''REF: A. 04 STATE 273089 
     ¶B. 04 PANAMA 02153 
     ¶C. PANAMA 00338 
     ¶D. 04 PANAMA 00548 
     ¶E. 04 PANAMA 00148 
     ¶F. 2004 HUMAN RIGHTS REPORT FOR PANAMA 
     ¶G. PANAMA 00390 
     ¶H. 04 PANAMA 02589 
     ¶I. PANAMA 00088 
     ¶J. 04 PANAMA 02613 ''',
     2005,
     [cable(u'04STATE273089', u'A'),
      cable(u'04PANAMA2153', u'B'), cable(u'05PANAMA338', u'C'),
      cable(u'04PANAMA548', u'D'), cable(u'04PANAMA148', u'E'),
      report(u'2004 HUMAN RIGHTS REPORT FOR PANAMA', u'F'),
      cable(u'05PANAMA390', u'G'), cable(u'04PANAMA2589', u'H'),
      cable(u'05PANAMA88', u'I'), cable(u'04PANAMA2613', u'J'),]),
    # 04BRASILIA1635
    (u'''REFS :  (A) 03 Brasilia 3939 
 
        (B) 03 Brasilia 3867 
        (C) 03 Brasilia 3347 
        (D) 03 Brasilia 1192 ''',
     2004,
     [cable(u'03BRASILIA3939', u'A'), cable(u'03BRASILIA3867', u'B'),
      cable(u'03BRASILIA3347', u'C'), cable(u'03BRASILIA1192', u'D'),]),
    # 05BRASILIA1466
    (u'''REF: A. STATE 43965 
     ¶B. BRASILIA 1207 
     ¶C. BRASILIA 1035 
     ¶D. BRASILIA 1017 
     ¶E. BRASILIA 660 
     ¶F. BRASILIA 415 
     ¶G. BRASILIA 223 
     ¶H. USDEL SECRETARY TELEGRAMS 000005/000007/00004 
     ¶I. (S/NF) TD-314/21795-05 11 APRIL 2005 
     ¶J. (S/NF) TD-314/21753-05 11 APRIL2005. ''',
    2005,
     [cable(u'05STATE43965', u'A'), cable(u'05BRASILIA1207', u'B'),
      cable(u'05BRASILIA1035', u'C'), cable(u'05BRASILIA1017', u'D'),
      cable(u'05BRASILIA660', u'E'), cable(u'05BRASILIA415', u'F'),
      cable(u'05BRASILIA223', u'G'),
      report(u'(S/NF) TD-314/21795-05 11 APRIL 2005', u'I'),
      report(u'(S/NF) TD-314/21753-05 11 APRIL2005.', u'J'),]),
    # 03KATHMANDU2366
    (u'''SUBJECT: NEPAL:  AMBASSADOR RELAYS CONCERNS ABOUT 
ACTIVITIES OF INDIAN INTELLIGENCE AGENTS 
 
REF: A. REF: KATHMANDU 2282 
     ¶B. KATHMANDU 2298 

Classified By: AM''',
     2003,
     [cable(u'03KATHMANDU2282', u'A'), cable('03KATHMANDU2298', 'B')]),
    # 10TRIPOLI116
    (u'''TAGS: PGOV EPET ECON LY EFIN

SUBJECT: SHOKRI GHANEM OUTLINES PLANS FOR LIBYA'S NATIONAL OIL CORPORATION REF: 09 TRIPOLI 862 TRIPOLI 00000116 001.2 OF 003 CLASSIFIED BY: Gene Cretz, Ambassador, U.S. Embassy Tripoli, U.S. Department of State. REASON: 1.4 (b), (d)

¶1. (C)''',
    2010,
     [cable('09TRIPOLI862')]),
    # 05TAIPEI4305
    (u'''E.O. 12958:N/A 
TAGS: EWWT ETRD ECON TW
SUBJECT: Port of Kaohsiung Sixth Container Terminal Faces 
New Obstacles 
 
Ref:  Ref A) Taipei 3393 B) Taipei 03793 C) Taipei 03856 D) 
 
Taipei 03196 E) Taipei 03197 F) Taipei 03525 
 
1. (U) ''',
     2005,
     [cable('05TAIPEI3393', 'A'), cable('05TAIPEI3793', 'B'),
      cable('05TAIPEI3856', 'C'), cable('05TAIPEI3196', 'D'),
      cable('05TAIPEI3197', 'E'), cable('05TAIPEI3525', 'F')]),
    # 07HONGKONG2339
    (u'''REF: A) USDOC 06988 B) EXP.LIC. D328589 C) HK 
03591 D) HK 07053 E) HK 04648 ''',
     2007,
     [cable('07USDOC6988', 'A'), cable(u'07HONGKONG3591', 'C'),
      cable(u'07HONGKONG7053', 'D'), cable(u'07HONGKONG4648', 'E')]),
    # 07HONGKONG2480
    (u'''REF: A) USDOC 05667 B)HK05511 ''',
     2007,
     [cable(u'07USDOC5667', 'A'), cable('07HONGKONG5511', 'B')]),
    # 02HARARE81
    (u'''REFS: A) STATE (01) 201265, B) STATE (01) 213042,C) 
 
STATE 02034 
''',
     2002,
     [cable(u'01STATE201265', u'A'), cable(u'01STATE213042', 'B'),
      cable(u'02STATE2034', 'C')]),
    # 07HANOI73
    (u'''REF: A) HO CHI MINH 10 B) 06 HCMC 1497 AND PREVIOUS ''',
     2007,
     [cable(u'07HOCHIMINHCITY10', u'A'), cable(u'06HOCHIMINHCITY1497', 'B')]),
     
)

def test_parse_references():
    def check(content, year, expected):
        eq_(expected, parse_references(content, year))
    for content, year, expected in _TEST_DATA:
        yield check, content, year, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

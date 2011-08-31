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
    # 07BAGHDAD3708
    (u'''REF: BAGHDAD #3565 ''',
     2007,
     [cable(u'07BAGHDAD3565')]),
    # 00ATHENS1501
    (u'''REF: 09 STATE 96625; A. A)STATE 70789; B. B) SEOUL 1144 
C. C) SINGAPORE 675; D. D) THE HAGUE 4750; E. E) NAIROBI 1812 
F. F) ADDIS 1556; G. G) STATE 87385; H. H) STATE 58996 
 ''',
     2000,
     [cable(u'09STATE96625'),
      cable(u'00STATE70789', u'A'), cable(u'00SEOUL1144', u'B'),
      cable(u'00SINGAPORE675', u'C'), cable(u'00THEHAGUE4750', u'D'),
      cable(u'00NAIROBI1812', 'E'), cable(u'00ADDIS1556', u'F'),
      cable(u'00STATE87385', u'G'), cable(u'00STATE58996', u'H')]),
    # 04DUBLIN1645
    (u'''REF: SECSTATE 232089 & USUN 2336 ''',
     2004,
     [cable(u'04STATE232089'), cable(u'04USUNNEWYORK2336')]),
    # 05PARIS8123
    (u'''REF: Paris 7472 and 7677 ''',
     2005,
     [cable(u'05PARIS7572'), cable(u'05PARIS7677')]),
    # 06GUANGZHOU15376
    (u'''Ref: A) GUANGZHOU 11657 and 7743, 12155, 13381 B) 
GUANGZHOU 14712 C) BEIJING 00565, D) GUANGZHOU 13381 '''
     2006,
     [cable(u'06GUANGZHOU11657', u'A'), cable(u'06GUANGZHOU7743', 'A'),
      cable(u'06GUANGZHOU12155', u'A'), cable(u'06GUANGZHOU13381', u'A'),
      cable(u'06GUANGZHOU14712', u'B'), cable(u'06BEIJING565', u'C'),
      cable(u'06GUANGZHOU13381', u'D')]),
    # 06MANILA3065
    (u'''REF: A. MANILA 2969 
     ¶B. 2962 AND PREVIOUS 
 ''',
     2006,
     [cable(u'06MANILA2969', 'A'), cable(u'06MANILA2969', u'B')]),
    # 06QUITO1920
    (u'''REF: A. QUITO 4525-91 
 
     B. QUITO 1735 
     C. QUITO 1905-03 
     D. QUITO 0579 
     E. QUITO 1973-91''',
     2006,
     [cable(u'91QUITO4525', u'A'), cable(u'06QUITO1735', u'B'),
      cable(u'03QUITO1905', u'C'), cable(u'06QUITO579', u'D'),
      cable(u'91QUITO1973', u'E')]),
    # 06ULAANBAATAR881
    (u'''Ref: 870 Ulaanbaatar ''',
     2006,
     [cable(u'06ULAANBAATAR870')]),
    # 07AMMAN1801
    (u'''A. REF AMMAN 222 
     B. 06 AMMAN 4685 
     C. 06 AMMAN 2145 ''',
     2007,
     [cable(u'07AMMAN222', u'A'), cable(u'06AMMAN4685', u'B'),
      cable(u'06AMMAN2145', u'C')]),
    # 07MOSCOW1811
    (u'''REF: A. ST. PETERSBURG 75 
      B. MOSCOW 510 ''',
     2007,
     [cable(u'07STPETERSBURG75', u'A'), cable(u'07MOSCOW510', u'B')]),
    # 08STATE1988
    (u'''REF: PRAGUE 849, PRAGUE, 1228, STATE 1484761 ''',
     2008,
     [cable(u'08PRAGUE849'), cable(u'08PRAGUE1228'), cable(u'08STATE1484761')]),
    # 08COTONOU369
    (u'''REF: COTON0U 348 ''',
     2008,
     [cable(u'08COTONOU348')]),
    # 08KABUL85
    (u'''Ref: A - Kabul 28 ''',
     2008,
     [cable(u'08KABUL28', u'A')]),
    # 07KABUL1033
    (u'''Refs:  A) Kabul 936/935; B) Kabul 692/317/274/162; C) 06 Kabul 
5353/5194/4319 and previous 
 ''',
     2007,
     [cable(u'07KABUL936', u'A'), cable(u'07KABUL935', u'A'),
      cable(u'07KABUL692', u'B'), cable(u'07KABUL317', u'B'),
      cable(u'07KABUL274', u'B'), cable(u'07KABUL162', u'B'),
      cable(u'06KABUL5353', u'C'), cable(u'06KABUL5194', u'C'),
      cable(u'06KABUL4319', u'C')]),
    # 09PANAMA176
    (u'''REF: A. A: PANAMA 00789/08 
     B. B: PANAMA 00930/08
     ''',
     2009,
     [cable(u'08PANAMA798', u'A'), cable(u'08PANAMA930', u'B')]),
    # 02KATHMANDU496
    (u'''REFS: A) 377 KATHMANDU, B) 01 KATHMANDU 2383, C) 01 
KATHMANDU 2292 '''
     2002,
     [cable(u'02KATHMANDU377', u'A'), cable(u'01KATHMANDU2383', u'B'),
      cable(u'01KATHMANDU2292', u'C')]),
    # 02ABUJA1194
    (u'''REF: REFERENCE: 01 ABUJA 997 ''',
     2002,
     [cable(u'01ABUJA997')]),
    # 02AMMAN2228
    (u'''REF: A. SECSTATE 51937 B. AMMAN 5049-01 ''',
     2002,
     [cable(u'02STATE51937', u'A'), cable(u'01AMMAN5049', u'B')]),
    # 02ABUJA2651
    (u'''REF: (A) LAGOS O1512, (B) LAGOS 01545, (C) LAGOS 
01583, (D) Lagos 1678 ''',
     2002,
     [cable(u'02LAGOS1512', u'A'), cable(u'02LAGOS1545', u'B'),
      cable(u'02LAGOS1583', u'C'), cable(u'02LAGOS1678', u'D')]),
    # 02AMMAN5966
    (u'''REF: AMMAN 07718 99, AMMAN 05986 00, AMMAN 07718 01 ''',
     2002,
     [cable(u'99AMMAN7718'), cable(u'00AMMAN5986'), cable(u'01AMMAN7718')]),
    # 02ROME5601
    (u'''REF: UNCLASS USDA FAS 57863 ''',
     2002,
     [cable(u'02USDAFAS57863'),]),
    # 02COLOMBO2314
    (u'''Refs:  (A) Colomobo 2304 
 
-      (B) State 240035 
-      (C) State 240015 '''
     2002,
     [cable(u'02COLOMBO2304', u'A'), cable(u'02STATE240035', u'B'),
      cable(u'02STATE240015', u'C')]),
    # 03KUWAIT2545
    (u'''REF: KUWAIT (C)02293 ''',
     2003,
     [cable(u'03KUWAIT2293')]),
    # 03COLOMBO1516
    (u'''REF: COLOMBO CABLES 0266 AND 02259 (2002)''',
     2003,
     [cable(u'03COLOMBO266'), cable(u'02COLOMBO2259')]),
    # 03ANKARA6322
    (u'''REF: A) 6307 B) STATE 285773 ''',
     2003,
     [cable(u'03ANKARA6307', u'A'), cable(u'03STATE285773')]),
     
)

def test_parse_references():
    def check(content, year, expected):
        eq_(expected, parse_references(content, year))
    for content, year, expected in _TEST_DATA:
        yield check, content, year, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

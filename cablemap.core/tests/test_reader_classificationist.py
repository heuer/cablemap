# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2012 -- Lars Heuer <heuer[at]semagia.com>
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
Tests classificationist parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.reader import parse_classificationist

_TEST_DATA = (
    (u'10TOKYO397', u'Marc Wall', u'''FIELD

REF: STATE 015541

Classified By: Acting Deputy Chief of Mission Marc Wall for Reasons 1.4
 (b) and (d)

¶1. (C) SUM'''),
    (u'10GENEVA249', u'Rose E. Gottemoeller', u'''REF: 10 GENEVA 231 (SFO-GVA-VIII-088) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) '''),
    (u'10GENEVA247', u'Rose E. Gottemoeller', u'''REF: 10 GENEVA 245 (SFO-GVA-VIII-086) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) ¶1. (U) This '''),
    (u'10UNVIEVIENNA77', u'Glyn T. Davies', u'''Classified By: Ambassador Glyn T. Davies for reasons 1.4 b and d '''),
    (u'10WARSAW117', u'F. Daniel Sainz', u'''Classified By: Political Counselor F. Daniel Sainz for Reasons 1.4 (b) and (d) '''),
    (u'10STATE16019', u'Karin L. Look', u'''Classified By: Karin L. Look, Acting ASSISTANT SECRETARY, VCI. Reason: 1.4 (b) and (d).'''),
    (u'10LILONGWE59', u'Bodde Peter', u'''CLASSIFIED BY: Bodde Peter, Ambassador; REASON: 1.4(B) '''),
    (u'95ZAGREB4339', u'ROBERT P. FINN', u'''
1.  (U)  CLASSIFIED BY ROBERT P. FINN, DEPUTY CHIEF OF
MISSION.  REASON: 1.5 (D)
 '''),
    (u'95DAMASCUS5748', u'CHRISTOPHER W.S. ROSS', u'''SUBJECT:  HAFIZ AL-ASAD: LAST DEFENDER OF ARABS

1. CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY:
CHRISTOPHER W.S. ROSS, AMBASSADOR.  REASON: 1.5 (D) .

2. SUMMAR'''),
    (u'95TELAVIV17504', None, u'''
1.  CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY SECTION 1.5 (B)
AND (D).  NIACT PRECEDENCE BECAUSE OF GOVERNMENT CRISIS IN
ISRAEL.

2.  SU'''),
    (u'95RIYADH5221', u'THEODORE KATTOUF', u'''
1.  CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY DCM
THEODORE KATTOUF - 1.5 B,D.

2.  (C)'''),
    (u'96ADDISABABA1545', u'JEFFREY JACOBS', u'''
1.  (U)  CLASSIFIED BY POLOFF JEFFREY JACOBS, 1.5 (D).

2.  (C)'''),
    (u'96AMMAN2094', u'ROBERT BEECROFT', u'''
1. (U)  CLASSIFIED BY CHARGE ROBERT BEECROFT; REASON 1.5 (D).

2. (C) '''),
    (u'96STATE86789', u'MARY BETH LEONARD', u'''
1.  CLASSIFIED BY AF/C - MARY BETH LEONARD, REASON 1.5
(D). '''),
    (u'96NAIROBI6573', u'TIMOTHY CARNEY', u'''
1.  CLASSIFIED BY AMBASSADOR TO SUDAN TIMOTHY CARNEY.
REASON 1.5(D).
 '''),
    (u'96RIYADH2406', u'THEODORE KATTOUF', u'''SUBJECT:  CROWN PRINCE ABDULLAH THE DIPLOMAT

1.  (U) CLASSIFIED BY CDA THEODORE KATTOUF, REASON 1.5.D.

2. '''),
    (u'96RIYADH2696', u'THEODORE KATTOUF', u'''
1.  (U)  CLASSIFIED BY CHARGE D'AFFAIRES THEODORE
KATTOUF: 1.5 B, D.
 '''),
    (u'96ISLAMABAD5972', u'THOMAS W. SIMONS, JR.', u'''
1.  (U) CLASSIFIED BY THOMAS W. SIMONS, JR., AMBASSADOR.
REASON:  1.5 (B), (C) AND (D).
 '''),
    (u'96ISLAMABAD5972', u'Thomas W. Simons, Jr.', u'''
1.  (U) CLASSIFIED BY THOMAS W. SIMONS, JR., AMBASSADOR.
REASON:  1.5 (B), (C) AND (D).
 ''', True),
    (u'96STATE183372', u'LEE 0. COLDREN', u''' 
1.  (U) CLASSIFIED BY LEE 0. COLDREN, DIRECTOR, SA/PAB, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 '''),
    (u'96STATE183372', u'Lee O. Coldren', u''' 
1.  (U) CLASSIFIED BY LEE 0. COLDREN, DIRECTOR, SA/PAB, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 ''', True),
    (u'96ASHGABAT2612', u'TATIANA C. GFOELLER', u''' 
1.  (U) CLASSIFIED BY CHARGE TATIANA C. GFOELLER. 
REASON:  1.5 D. 
 '''),
    (u'96BOGOTA8773', u'S.K. ABEYTA', u''' 
1.  CLASSIFIED BY POL/ECONOFF. S.K. ABEYTA.  REASON:  1.5(D) 
 '''),
    (u'96STATE194868', u'E. GIBSON LANPHER, JR.', u''' 
1.   (U) CLASSIFIED BY E. GIBSON LANPHER, JR., ACTING 
ASSISTANT SECRETARY OF STATE FOR SOUTH ASIAN AFFAIRS, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 '''),
    (u'96JAKARTA7841', u'ED MCWILLIAMS', u''' 
1.  (U) CLASSIFIED BY POL COUNSELOR ED MCWILLIAMS; 
REASON 1.5(D) 
 '''),
    (u'96JERUSALEM3094', u'EDWARD G. ABINGTON, JR.', u''' 
1.  CLASSIFIED BY CONSUL GENERAL EDWARD G. ABINGTON, JR.  REASON 
1.5 (B) AND (D). 
 '''),
    (u'96BOGOTA10967', u'S.K. ABEYTA', u''' 
1.  (U)  CLASSIFIED BY POL/ECONOFF S.K. ABEYTA.  REASON 1.5(D). 
 '''),
    (u'04MUSCAT2112', u'Richard L. Baltimore, III', u''' 
Classified By: Ambassador Richard L. Baltimore, III. 
Reasons: 1.4 (b) and (d). 
 '''),
    (u'04MUSCAT2112', u'Richard L. Baltimore, III', u''' 
Classified By: Ambassador Richard L. Baltimore, III. 
Reasons: 1.4 (b) and (d). 
 ''', True),
    (u'05OTTAWA1975', u'Patricia Kim-Scott', u''' 
Classified By: Pol/Mil Officer Patricia Kim-Scott.  Reason E.O. 12958, 
1.4 (b) and (d). 
 '''),
    (u'05BOGOTA6208', u'William B. Wood', u''' 
Classified By: Ambassador William B. Wood; reasons 1.4 
(b) and (d) 
 '''),
    (u'05TAIPEI2839', u'Douglas Paal', u''' 
Classified By: AIT Director Douglas Paal, Reason(s): 1.4 (B/D). 
 '''),
    (u'05DHAKA3073', u'D.C. McCullough', u''' 
Classified By: A/DCM D.C. McCullough, reason para 1.4 (b) 
 '''),
    (u'09NAIROBI1132', u'Jessica Davis Ba', u''' 
Classified By: Pol/Econ Officer Jessica Davis Ba for reasons 1.4(b) and 
 (d) 
 '''),
    (u'08ROME1541', u'Liz Dibble', u''' 
Classified By: Classified by DCM Liz Dibble for reasons 1.4 (b) and 
(d). 
 '''),
    (u'06BAGHDAD2082', u'DANIEL SPECKHARD', ur''' 
Classified By: CHARGE D\'AFFAIRES DANIEL SPECKHARD FOR REASONS 1.4 (A), 
(B) AND (D) 
 '''),
    (u'05ANKARA4653', u'Nancy McEldowney', u''' 
Classified By: (U) CDA Nancy McEldowney; E.O. 12958, reasons 1.4 (b,d) 
 '''),
    (u'05QUITO2057', u'LARRY L. MEMMOTT', u''' 
Classified By: ECON LARRY L. MEMMOTT, REASONS 1.4 (B,D) 
 '''),
    (u'06HONGKONG3559', u'LAURENT CHARBONNET', u''' 
CLASSIFIED BY: ACTING DEPUTY PRINCIPAL OFFICER LAURENT CHARBONNET.  REA 
SONS: 1.4 (B,D) 
 '''),
    (u'09BAGHDAD791', u'Patricia Butenis', u''' 
Classified By: Charge d\' Affairs Patricia Butenis for reasons 1.4 (b) a 
nd (d) 
 '''),
    (u'06OSLO19', u'Christopher W. Webster', u''' 
Classified By: Charge d\'Affaires a.i. Christopher W. Webster, 
reason 1.4 (b) and (d) 
 '''),
    (u'08BEIJING3386', u'Aubrey Carlson', u''' 
Classified By: Political Section Minister Counselor Aubrey Carlson.  Re 
asons 1.4 (b/d). 
 '''),
    (u'09MOSCOW2393', u'Susan M. Elliott', u''' 
Classified By: Political Minister Counselor Susan M. Elliott for reason 
s:  1.4 (b), (d). 
 '''),
    (u'10BRUSSELS66', u'Christopher R. Davis', u''' 
Classified By: Political Minister-Counselor Christopher R. Davis for re 
ason 1.4 (b/d) 
 '''),
    (u'06BEIJING22125', u'ROBERT LUKE', u''' 
Classified By: (C) CLASSIFIED BY MINISTER COUNSELOR FOR ECONOMIC AFFAIR 
S ROBERT LUKE; REASON 1.4 (B) AND (D). 
 '''),
    (u'07CAIRO622', u'William R. Stewart', u''' 
Classified by:  Minister Counselor for Economic and 
Political Affairs William R. Stewart for reasons 1.4(b) and 
(d). 
 '''),
    (u'07BAGHDAD1188', u'Daniel Speckhard', u''' 
Classified By: Charge Affaires Daniel Speckhard.  Reasons: 1.4 (b) and 
(d). 
 '''),
    (u'08PARIS1131', u'STUART DWYER', u''' 
Classified By: ECONCOUNS STUART DWYER FOR REASONS 1.4 B AND D 
 '''),
    (u'08ATHENS985', u'Jeff Hovenier', u''' 
Classified By: A/Political Counselor Jeff Hovenier for 
1.4 (b) and (d) 
 '''),
    (u'09BEIJING2690', u'William Weinstein', u''' 
Classified By: This message classified by Econ Minister Counselor 
William Weinstein for reasons 1.4 (b), (d) and (e). 
 '''),
    (u'06VILNIUS945', u'Rebecca Dunham', u''' 
Classified By: Political and Economic Section Chief Rebecca Dunham for 
reasons 1.4 (b) and (d) 
 '''),
    (u'07BAGHDAD2781', u'Howard Keegan', u''' 
Classified By: Kirkuk PRT Team Leader Howard Keegan for reason 1.4 (b) 
and(d). 
 '''),
    (u'09HARARE864', u'Donald Petterson', u''' 
Classified By: Charge d\'affaires, a.i. Donald Petterson for reason 1.4 
(b). 
 '''),
    (u'04MANAMA525', u'Robert S. Ford', u''' 
Classified By: Charge de Affaires Robert S. Ford for reasons 
1.4 (b) and (d). 
 '''),
    (u'08STATE56778', u'Patricia A. McNerney', u''' 
Classified By: ISN Acting Assistant Secretary 
Patricia A. McNerney, Reasons 1.4 b, c, and d 
 '''),
    (u'07BRUSSELS1462', u'Larry Wohlers', u''' 
Classified By: USEU Political Minister Counselor Larry Wohlers 
for reasons 1.4 (b) and (d). 
 '''),
    (u'09KABUL2261', u'Hoyt Yee', u''' 
Classified By: Interagency Provincial Affairs Deputy Coordinator Hoyt Y 
ee for reasons 1.4 (b) and (d) 
 '''),
    (u'09KABUL1233', u'Patricia A McNerney', u''' 
Classified By: PRT and Sub-National Governance Acting Director Patricia 
 A McNerney for reasons 1.4 (b) and (d) 
 '''),
    (u'09BRUSSELS1288', u'CHRISTOPHER DAVIS', u''' 
Classified By: CLASSIFIED BY USEU MCOUNSELOR CHRISTOPHER DAVIS, FOR REA 
 
SONS 1.4 (B) AND (D) 
 '''),
    (u'06TAIPEI3165', u'Stephen M. Young', u''' 
Classified By: Classified by AIT DIR Stephen M. Young. 
Reasons:  1.4 b, d. 
 '''),
    (u'07BRUSSELS1208', u'Courtney Nemroff', u''' 
Classified By: Institutional Affairs Unit Chief Courtney Nemroff for re 
asons 1.4 (b) & (d) 
 '''),
    (u'05CAIRO8602', u'Michael Corbin', u''' 
Classified by ECPO Minister-Counselour Michael Corbin for 
reasons 1.4 (b) and (d). 
 '''),
    (u'09MADRID1210', u'Arnold A. Chacon', u''' 
Classified By: Charge d'Affaires, a.i., Arnold A. Chacon 
 
1.(C) Summary:  In his meetings with Spanish officials, 
Special Envoy for Eurasian Energy'''),
)


def test_parse_classificationist():
    def check(cable_id, expected, content, normalize):
        eq_(expected, parse_classificationist(content, normalize))
    for testcase in _TEST_DATA:
        if len(testcase) == 3:
            cable_id, expected, content = testcase
            normalize = False
        else:
            cable_id, expected, content, normalize = testcase
        yield check, cable_id, expected, content, normalize


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

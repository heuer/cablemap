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

_TEST_DATA = (
    # input string, year, optional reference_id, expected

    # 07TBILISI1732
    ('\nREF: A. TBILISI 1605  B. TBILISI 1352  C. TBILISI 1100  D. 06 TBILISI 2601  E. 06 TBILISI 2590  F. 06 TBILISI 2425  G. 06 TBILISI 2390  H. 06 TBILISI 1532  I. 06 STATE 80908  J. 06 TBILISI 1064  K. 06 TBILISI 0619  L. 06 TBILISI 0397  M. 06 MOSCOW 0546  N. 06 TBILISI 0140  O. 05 TBILISI 3171',
     2007, [u'07TBILISI1605', u'07TBILISI1352', u'07TBILISI1100', u'06TBILISI2601', u'06TBILISI2590', u'06TBILISI2425', u'06TBILISI2390', u'06TBILISI1532', u'06STATE80908', u'06TBILISI1064', u'06TBILISI619', u'06TBILISI397', u'06MOSCOW546', u'06TBILISI140', u'05TBILISI3171']),
    # 08PARIS1698
    ('''
REF: A. PARIS 1501
B. PARIS 1568
C. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832
0617 08)
D. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832
0626 08) ''', 2008,
     [u'08PARIS1501', u'08PARIS1568']),
    # 08PARIS1501
    ('\nREF: A. 05 PARIS 5459 \nB. 06 PARIS 5733', 2008,
     [u'05PARIS5459', u'06PARIS5733']),
    # 07TALLINN375
    ('\nREF: A) TALLINN 366 B) LEE-GOLDSTEIN EMAIL 05/11/07 \nB) TALLINN 347 ', 2007,
     [u'07TALLINN366', u'07TALLINN347']),
    # 07TRIPOLI943
    ('\nREF: A) STATE 135205; B) STATE 127608; C) JOHNSON-STEVENS/GODFREY E-MAIL 10/15/07; D) TRIPOLI 797; E) TRIPOLI 723 AND PREVIOUS', 2007,
     [u'07STATE135205', u'07STATE127608', u'07TRIPOLI797', u'07TRIPOLI723']),
    # 07STATE156011
    ('  REF: LA PAZ 2974', 2007, [u'07LAPAZ2974']),
    # 05PARIS7835
    ('\nREF: A. (A) PARIS 7682 AND PREVIOUS ', 2005, [u'05PARIS7682']),
    # 05PARIS7835
    ('\nREF: A. (A) PARIS 7682 AND PREVIOUS \n\nB. (B) EMBASSY PARIS DAILY REPORT FOR OCTOBER 28 - \nNOVEMBER 16 (PARIS SIPRNET SITE) \nC. (C) PARIS 7527 ', 2005,
     [u'05PARIS7682', u'05PARIS7527']),
    # 09MADRID869
    ('\nSUBJECT: UPDATES IN SPAIN’S INVESTIGATIONS OF RUSSIAN MAFIA \nREF: A. OSC EUP20080707950031  B. OSC EUP20081019950022  C. OSC EUP20090608178005  D. MADRID 286  E. OSC EUP20050620950076  F. OSC EUP20080708950049  G. OSC EUP20081029950032  H. OSC EUP 20061127123001\nMADRID 00000869 001.2 OF 004\n', 2009,
     [u'09MADRID286']),
    # 07STATE152317
    ('\nREF: (A)STATE 071143, (B)STATE 073601, (C)STATE 72896, (D)BEIJING \n5361, (E) STATE 148514', 2007,
     [u'07STATE71143', u'07STATE73601', u'07STATE72896', u'07BEIJING5361', u'07STATE148514']),
    # 08MANAGUA573
    ('\nREF: A. MANAGUA 520 \nB. MANAGUA 500 \nC. MANAGUA 443 \nD. MANAGUA 340 \nE. MANAGUA 325 \nF. MANAGUA 289 \nG. MANAGUA 263 \nH. MANAGUA 130 \nI. 2007 MANAGUA 2135 \nJ. 2007 MANAGUA 1730 \nK. 2007 MANAGUA 964 \nL. 2006 MANAGUA 2611 ', 2008,
     [u'08MANAGUA520', u'08MANAGUA500', u'08MANAGUA443', u'08MANAGUA340', u'08MANAGUA325', u'08MANAGUA289', u'08MANAGUA263', u'08MANAGUA130', u'07MANAGUA2135', u'07MANAGUA1730', u'07MANAGUA964', u'06MANAGUA2611']),
    # 66BUENOSAIRES2481
    ('\n REF: STATE 106206 CIRCULAR; STATE CA-3400 NOV 2, 1966 ', 1966, [u'66STATE106206']),
    #04MADRID4063
    ('\nREF: EMBASSY MADRID E-MAIL TO EUR/WE OF OCTOBER 14\n', 2004, []),
    #08RIYADH1134
    ('\nREF: A. SECSTATE 74879 \n     B. RIYADH 43 \n', 2008, [u'08STATE74879', u'08RIYADH43']),
    #08RIODEJANEIRO165
    ('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\n\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ', 2008,
     [u'08RIODEJANEIRO138', u'08RIODEJANEIRO44']),
    ('\nREF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008,
    [u'08STATE54183', u'07BRASILIA1868', u'08STATE57700', u'07STATE17940']),
    # 08BRASILIA806
    ('\nPROGRAM REF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008,
     [u'08STATE54183', u'07BRASILIA1868', u'08STATE57700', u'07STATE17940']),
    # 06SAOPAULO276
    ('\nCARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA REF: (A) 05 SAO PAULO 405; (B) 05 SAO PAULO 402 (C) 02 BRASILIA 2670', 2006,
     [u'05SAOPAULO405', u'05SAOPAULO402', u'02BRASILIA2670']),
    # 08BERLIN1387
    ('\nREF: A. BERLIN 1045\nB. SECDEF MSG DTG 301601z SEP 08', 2008, [u'08BERLIN1045']),
    #09NAIROBI1938
    ('\nREF: A. 08 STATE 81854\n\n\nS e c r e t nairobi 001938', 2009, [u'08STATE81854']),
    # 02ROME1196
    ('\nREF: A. STATE 40721\n CONFIDENTIAL\\nPAGE 02 ROME 01196 01 OF 02 082030Z  B. ROME 1098  C. ROME 894  D. MYRIAD POST-DEPARTMENT E-MAILS FROM 10/01-02/02  E. ROME 348\nCLASSIFIED BY: POL', 2002,
     [u'02STATE40721', u'02ROME1098', u'02ROME894', u'02ROME348']),
    # 10TRIPOLI167
    ('\nREF: TRIPOLI 115\n\n1.(SBU) This is an action request; please see para 4.\n\n', 2010, [u'10TRIPOLI115']),
    # 06BRASILIA882
    ('SUBJECT: ENERGY INSTALLATIONS REF: BRASILIA 861', 2006, [u'06BRASILIA861']),
    # 08MOSCOW864
    ("TAGS: EPET ENRG ECON PREL PGOV RS\nSUBJECT: WHAT'S BEHIND THE RAIDS ON TNK-BP AND BP REF: A. MOSCOW 816 B. MOSCOW 768 C. 07 MOSCOW 3054 Classified By: Ambassador William J. Burns for Reasons 1.4 (b/d)\n", 2008,
     [u'08MOSCOW816', u'08MOSCOW768', u'07MOSCOW3054']),
    # 08TRIPOLI402
    ('REF: A) TRIPOLI 199, B) TRIPOLI 227 TRIPOLI 00000402 \n\n001.2 OF 003 ', 2008, '08TRIPOLI402',
      [u'08TRIPOLI199', u'08TRIPOLI227']),
    # 08LONDON2627
    ('''
E.O. 12958: N/A TAGS: AMGT

SUBJECT: UK COUNTRY CLEARANCE IS GRANTED TO STAMILIO, LTC DODSON AND LTCOL HAVRANEK REF: SECDEF R162245Z OCT 08

1.Embassy London is pleased to grant country clearance to Mr. Mark Stamilio, LTCOL John Havranek, and LTC James Dodson to visit London October 19-20 to attend working level meetings on ISAF detention policies and practices.

2. ---------------- Visit Officer ---------------- 

XXXXXXXXXXXX If calling from within the UK replace 44 with 0, if calling from landline to landline within London, dial only the last eight digits.

3. Confirmed reservations are held for Stamilio, Havranek and Dodson at Marriott Grosvernor Square.The rate is within per diem. The confirmation number are: Stamilio - 84274267, Havranek, 84274449, and Dodson, 84274523. London Marriott Grosvenor Square, Grosvenor Square, London W1A 4AW. Telephone number is (44)(0)20 7493-1232 Fax number is (44)(0)20 7491-3201. If calling from within the UK replace 44 with 0; if calling from landline within London, dial only the last eight digits.

4.Carry
''', 2008, []),
    # 08BRASILIA429
    ('''
SUBJECT: THOUGHTS ON THE VISIT OF DEFENSE MINISTER JOBIM TO WASHINGTON 

REF: A. A) BRASILIA 236 B. B) OSD REPORT DTG 251847Z MAR 08 C. C) BRASILIA 175 
Classified By: Ambassador Clifford Sobel. 
Reason: 1.5 d 
''', 2008, [u'08BRASILIA236', u'08BRASILIA175']),
    # 09PARIS1039
    ('''
SUBJECT: FRANCE’S POSITION ON NUCLEAR ISSUES IN THE RUN-UP 
TO THE NPT REVCON

REF: A. PARIS POINTS JULY 15  B. PARIS POINTS JULY 6  C. PARIS POINTS APRIL 10  D. PARIS 1025

Classified By:
''', 2009, [u'09PARIS1025']),
    # 08BERLIN1387
    ('''
SUBJECT: GERMANY: BUNDESTAG SET TO RENEW A BEEFED-UP ISAF
MANDATE AND A SCALED-DOWN OEF COUNTERPART

REF: A. BERLIN 1045 
¶B. SECDEF MSG DTG 301601z SEP 08

Classified By: CHARGE D'AFFAIRES''',
     2008,
     [u'08BERLIN1045']),
    # 08STATE15220
    ('''
Subject: (s) further scheming by german firm to export
test chamber to iranian ballistic missile program

Ref: a. 05 state 201650

B. 05 berlin 3726
c. 05 state 211408
d. 05 berlin 3954
e. 06 state 36325
f. 06 berlin 674
g. 06 state 62278
h. 06 berlin 1123
i. 06 state 70328
j. 06 berlin 1229
k. 06 berlin 1550
l. Mtcr poc 201/2006 - may 16 2006
m. 07 state 75839
n. 07 berlin 1137
o. 07 state 108420
p. 07 berlin 002163
q. 07 state 166482
r. 07 berlin 2216

Classified By: ISN/MTR DIRECTOR PAM DURHAM
for reasons 1.4 (b), (d).
''', 2008,
     [u'05STATE201650', u'05BERLIN3726', u'05STATE211408', u'05BERLIN3954', u'06STATE36325', u'06BERLIN674', u'06STATE62278', u'06BERLIN1123', u'06STATE70328', u'06BERLIN1229', u'06BERLIN1550', u'07STATE75839', u'07BERLIN1137', u'07STATE108420', u'07BERLIN2163', u'07STATE166482', u'07BERLIN2216']),
    # 09PARIS504
    ('''SUBJECT: DRC/ROC/NIGER: FRENCH PRESIDENCY'S READOUT OF 
SARKOZY'S MARCH 26-27 VISITS 

REF: A. PARIS 399 
B. KINSHASA 291 
C. BRAZZAVILLE 101 
D. NIAMEY 234 
E. 08 PARIS 1501 
F. 08 PARIS 1568 
G. 08 PARIS 1698 

Classified By: Political Minister-Counselor Kathleen Allegrone, 1.4 (b/ 
d). ''',
     2009,
     [u'09PARIS399', u'09KINSHASA291', u'09BRAZZAVILLE101', u'09NIAMEY234', u'08PARIS1501', u'08PARIS1568', u'08PARIS1698']),

)

def test_parse_references():
    def check(content, year, reference_id, expected):
        eq_(parse_references(content, year, reference_id), expected)
    for test in _TEST_DATA:
        reference_id = None
        if len(test) == 4:
           content, year, reference_id, expected = test
        else:
           content, year, expected = test
        yield check, content, year, reference_id, expected

_TRIPOLI_TESTS = {
'08TRIPOLI564': (
"""
RESIGN SOON 
 
REF: TRIPOLI 227  TRIPOLI 00000564  001.2 OF 002   CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy - Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (S/NF)
""", 2008, [u'08TRIPOLI227']),
'08TRIPOLI494': (
"""
E.O. 12958: DECL:  6/18/2018 
TAGS: PGOV PREL PHUM PINR LY
SUBJECT: JOURNALIST JAILED FOR CRITICIZING GOVERNMENT'S 
POORLY-COORDINATED DEVELOPMENT PROJECTS  CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary:  A respected [...]"""
, 2008, []),
'08TRIPOLI574': (
"""
SUBJECT: U.K. VISIT TO RABTA CHEMICAL WEAPONS PRODUCTION FACILITY 
 
REF: TRIPOLI 466  CLASSIFIED BY: John T. Godfrey, CDA, U.S. Embassy - Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary: T [...]
""", 2008, [u'08TRIPOLI466']),
'08TRIPOLI466': (
"""
TAGS: PARM PREL CWC OPCW CBW CH JA IT LY
SUBJECT: CHEMICAL WEAPONS CONVENTION (CWC): CONVERSION OF THE RABTA CHEMICAL WEAPONS PRODUCTION FACILITY  REF: A) STATE 58476, B) THE HAGUE 482, C) TRIPOLI 119  CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary:  The"""
, 2008, [u'08STATE58476', u'08THEHAGUE482', u'08TRIPOLI119'])
}


def test_malformed_tripoli_cables():
    def check(content, year, reference_id, expected_result):
        assert parse_references(content, year, reference_id) == expected_result
    for ref_id, params in _TRIPOLI_TESTS.iteritems():
        content, year, result = params
        yield check, content, year, ref_id, result


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
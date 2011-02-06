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
Tests subject parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from cablemap.core.reader import parse_subject

_TEST_DATA = (
    ("TAGS: TAG TAG2\\nSUBJECT:  SINGLE LINE SUBJECT \n\nREF: REF 1",  u'SINGLE LINE SUBJECT'),
    ("TAGS: TAG TAG2\\nSUBJECT: SUBJECT WHICH HAS a \nSECOND LINE \n\nREF: REF 1", u'SUBJECT WHICH HAS a SECOND LINE'),
    ("SUBJECT: SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES \nREF: A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\n",
     u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'),
    ("SUBJECT: SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES\nREF: A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\n",
      u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'),
    ("SUBJECT: SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES\nREF A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\n",
     u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'),
    ("SUBJECT SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES\nREF A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\n",
     u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'),
    ("SUBJECT: NEGOTIATIONS \n \n", u'NEGOTIATIONS'),
    ("SUBJECT: A CAUCASUS WEDDING \nClassified By: Deputy Chief of Mission Daniel A. Russell. Reason 1.4 ( b, d)",
     u'A CAUCASUS WEDDING'),
    ("SUBJ: GUINEA - U.S./French Meeting with President Compaore \n\nClassified by Charge d'Affaires",
     u'GUINEA - U.S./French Meeting with President Compaore'),
    ("SUBJECT: UAE FM DISCUSSES TALIBAN FINANCIAL FLOWS AND REINTEGRATION \nWITH AMB. HOLBROOKE AND TREASURY A/S COHEN\nCLASSIFIED BY: Richard",
     u'UAE FM DISCUSSES TALIBAN FINANCIAL FLOWS AND REINTEGRATION WITH AMB. HOLBROOKE AND TREASURY A/S COHEN'),
    ("SUBJECT:  EXTENDED NATIONAL JURISDICTIONS OVER HIGH SEAS \n\nREF: STATE 106206 CIRCULAR; STATE CA-3400 NOV 2, 1966",
     u'EXTENDED NATIONAL JURISDICTIONS OVER HIGH SEAS'),
    ('SUBJECT: (S) GERMANY TAKING ACTION ON SHIPMENT OF ...', False,
       u'(S) GERMANY TAKING ACTION ON SHIPMENT OF ...'),
    ('SUBJECT: (S) GERMANY TAKING ACTION ON SHIPMENT OF ...', True, 
     u'GERMANY TAKING ACTION ON SHIPMENT OF ...'),
    (u'E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu Subject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?\n\n(U) Classifi',
     u'turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?'),
    ("SUBJECT: PART 3 OF 3:  THE LIFE AND TIMES OF SOUTH AFRICA'S \nNEW PRESIDENT\nPRETORIA 00000954 001.2 OF 004\n",
     u"PART 3 OF 3: THE LIFE AND TIMES OF SOUTH AFRICA'S NEW PRESIDENT"),
    ("SUBJECT: ZIM NOTES 11-09-2009 \n----------- \n1. SUMMARY\n----------- \n",
      u'ZIM NOTES 11-09-2009'),
    ("TAGS: PGOV EINV INRB GM\nSUBJECT: GERMANY/BAVARIA: CSU HOPES FOR FRESH START WITH NEW AND\nYOUNGER FACES IN CABINETAND A DYNAMIC SECRETARY GENERAL \n\n",
     u'GERMANY/BAVARIA: CSU HOPES FOR FRESH START WITH NEW AND YOUNGER FACES IN CABINETAND A DYNAMIC SECRETARY GENERAL'),
    ('SUBJECT: ASSISTANT SECRETARY MEETS WITH ZIMBABWE \n CONFIDENTIAL\nPAGE 02 HARA',
     u'ASSISTANT SECRETARY MEETS WITH ZIMBABWE CONFIDENTIAL'),
    ('TAGS ENRG, EUN, ECON, EIND, KGHG, SENV, SW\nSUBJECT: SWEDISH DEPUTY PM URGES SENIOR USG VISITS TO SWEDEN DURING\nEU PRESIDENCY; WANTS TO LAUNCH U.S.-EU ALERNATIVE ENERGY PARTNERSHIP AT U.S.-EU SUMMIT\nThis is an Action request. Please see para 2.\n',
     u'SWEDISH DEPUTY PM URGES SENIOR USG VISITS TO SWEDEN DURING EU PRESIDENCY; WANTS TO LAUNCH U.S.-EU ALERNATIVE ENERGY PARTNERSHIP AT U.S.-EU SUMMIT'),
    ('C O R R E C T E D COPY//SUBJECT LINE//////////////////////////////////\n\nNOFORN\nSIPDIS\n\nEO 12958 DECL: 07/09/2018\nTAGS PREL, PTER, MOPS, IR, PK, AF, CA\n\nSUBJECT: COUNSELOR, CSIS DIRECTOR DISCUSS CT THREATS,\nPAKISTAN, AFGHANISTAN, IRAN\nREF: A. OTTAWA 360 B. OTTAWA 808 C. OTTAWA 850 D. OTTAWA 878\nOTTAWA 00000918 001.2 OF 003\n',
     u'COUNSELOR, CSIS DIRECTOR DISCUSS CT THREATS, PAKISTAN, AFGHANISTAN, IRAN'),
    (u"TAGS OVIP (CLINTON, HILLARY), PGOV, PREL, KDEV, ECON,\nNL, IS, SR\nSUBJECT: (U) Secretary Clinton's July 14 conversation\nwith Dutch Foreign Minister Verhagen\n1. Classified by Bureau Assistant Secretary Philip H. Gordon. Reason: 1.4 (d)\n2. (U) July 14; 2:45 p.m.; Washington, DC.\n3. (SBU) Participants:\n",
     False,
     u"(U) Secretary Clinton's July 14 conversation with Dutch Foreign Minister Verhagen"),
    (u"TAGS OVIP (CLINTON, HILLARY), PGOV, PREL, KDEV, ECON,\nNL, IS, SR\nSUBJECT: (U) Secretary Clinton's July 14 conversation\nwith Dutch Foreign Minister Verhagen\n1. Classified by Bureau Assistant Secretary Philip H. Gordon. Reason: 1.4 (d)\n2. (U) July 14; 2:45 p.m.; Washington, DC.\n3. (SBU) Participants:\n",
     True,
     u"Secretary Clinton's July 14 conversation with Dutch Foreign Minister Verhagen"),
    ('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\n\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ',
     u'AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO'),
    ("SUBJECT: BRAZIL: BLACKOUT -CAUSES AND IMPLICATIONS Classified By: Charge d'Affaires Cherie Jackson, Reasons 1.4 (b) and (d). REFTELS: A) 2008 BRASILIA 672, B) 2008 BRASILIA 593, C)2008 SAO PAULO 260\n",
     u'BRAZIL: BLACKOUT -CAUSES AND IMPLICATIONS'),
    ('SUBJECT: MEMBERS OF CONGRESS DISCUSS BONUSES, BAIL-OUTS AND\nOTHER REFORM MEASURES WITH UK OFFICIALS\n1. (SBU) Summary. Bonuses, regulatory structures',
     u'MEMBERS OF CONGRESS DISCUSS BONUSES, BAIL-OUTS AND OTHER REFORM MEASURES WITH UK OFFICIALS'),
    ('SUBJECT: AARGH! SWEDISH PIRATES SET SAIL FOR BRUSSELS\n1. Summary and Comment: Sweden',
      u'AARGH! SWEDISH PIRATES SET SAIL FOR BRUSSELS'),
    ('SUBJECT: EU JHA INFORMAL MINISTERIAL\n1. Summary. EU Justice and Home...',
     u'EU JHA INFORMAL MINISTERIAL'),
    ('\nSUBJECT: CARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA REF: (A) 05 SAO PAULO 405; (B) 05 SAO PAULO 402 (C) 02 BRASILIA 2670',
      u'CARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA'),
    # 06BRASILIA882
    ('SUBJECT: ENERGY INSTALLATIONS REF: BRASILIA 861', u'ENERGY INSTALLATIONS'),
    # 08MOSCOW864
    ("TAGS: EPET ENRG ECON PREL PGOV RS\nSUBJECT: WHAT'S BEHIND THE RAIDS ON TNK-BP AND BP REF: A. MOSCOW 816 B. MOSCOW 768 C. 07 MOSCOW 3054 Classified By: Ambassador William J. Burns for Reasons 1.4 (b/d)\n",
     u"WHAT'S BEHIND THE RAIDS ON TNK-BP AND BP"),
    # 08TRIPOLI266
    ('SUBJECT: GOL DELAYS RELEASING DETAINED HUMAN RIGHTS ACTIVIST FATHI EL-JAHMI REF: A) TRIPOLI 223, B) TRIPOLI 229 \n',
     u'GOL DELAYS RELEASING DETAINED HUMAN RIGHTS ACTIVIST FATHI EL-JAHMI'),
    # 05BRASILIA1839
    ('''E.O. 12958: N/A 
TAGS: EAIR EINV
SUBJECT: BRAZIL - NEXT STEPS FOR VARIG UNCLEAR REFS: (A) BRASILIA 1608, (B) BRASILIA 1631, (C) BRASILIA 1566 

1. (SBU) Summary.
''',
     u'BRAZIL - NEXT STEPS FOR VARIG UNCLEAR'),
    # 05BRASILIA2806
    ('''CAROLYN COLDREN FAA MIAMI FOR MARK RIOS 
E.O. 12958: N/A 
TAGS: EAIR EINV PGOV ETRD
SUBJECT: BRAZILIAN GOVERNMENT INTERVENES IN VARIG - TOO LITTLE, TOO LATE? REFS: (A) BRASILIA 1839, (B) BRASILIA 1608, (C) BRASILIA 1566 

1. (SBU) Summary.''',
     u'BRAZILIAN GOVERNMENT INTERVENES IN VARIG - TOO LITTLE, TOO LATE?'),
    # 05TASHKENT284
    ('''TAGS ECON PREL PINR UZ 
SUBJECT: GULNORA INC. STRIKES AGAIN 
REFS: A) 04 TASHKENT 3390 B) 04 TASHKENT 2574 and previous

CLASSIFIED BY AMB. JON R. PURNELL, FOR REASONS 1.4 (B, D)

1. (C) ''',
     u'GULNORA INC. STRIKES AGAIN'),
)


def test_parse_subject():
    def check(content, clean, expected):
        assert parse_subject(content, clean=clean) == expected
    for test in _TEST_DATA:
        clean = True
        if len(test) == 3:
            content, clean, expected = test
        else:
            content, expected = test
        yield check, content, clean, expected

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

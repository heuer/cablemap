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
Tests TAGs parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from cablemap.core.reader import parse_tags

_TEST_DATA = (
    ('TAGS: something', [u'SOMETHING']),
    ('TAGS: something\n', [u'SOMETHING']),
    ('TAGS: something\nhere', [u'SOMETHING']),
    ('TAGS: something, \nhere', [u'SOMETHING', u'HERE']),
    (u'TAGS: something,\nhere', [u'SOMETHING', u'HERE']),
    (u'TAGS something', [u'SOMETHING']),
    (u'TAGS something\n', [u'SOMETHING']),
    (u'TAGS something\nhere', [u'SOMETHING']),
    (u'TAGS something, \nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs something', [u'SOMETHING']),
    ('tAgs something\n', [u'SOMETHING']),
    (u'tAgs something\nhere', [u'SOMETHING']),
    (u'tAgs something, \nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs something,\nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs: something', [u'SOMETHING']),
    (u'tAgs: something\n', [u'SOMETHING']),
    (u'tAgs: something\nhere', [u'SOMETHING']),
    (u'tAgs: something, \nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs: something,\nhere', [u'SOMETHING', u'HERE']),
    (u'TAGS: PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'TAGS PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'tags PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'tags: PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'TAGS ECON, PGOV, EFIN, MOPS, PINR, UK',
     [u'ECON', u'PGOV', u'EFIN', u'MOPS', u'PINR', u'UK']),
    (u'TAG PTER, PGOV, ASEC, EFIN, ENRG, KCIP',
     [u'PTER', u'PGOV', u'ASEC', u'EFIN', u'ENRG', u'KCIP']),
    (u'E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu \nSubject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?\n\n(U) Classifi',
     [u'PREL', u'PGOV', u'PINS', u'TU']),
    (u"E.o. 12958: decl: after korean unification\nTags: ovip (steinberg, james b.), prel, parm, pgov, econ,\netra, mnuc, marr, ch, jp, kn, ks, ir\nSubject: deputy secretary steinberg's meeting with xxxxx\nforeign minister he yafei, september 29, 2009",
     [u'OVIP', u'STEINBERG, JAMES B.', u'PREL', u'PARM', u'PGOV', u'ECON', u'ETRA', u'MNUC', u'MARR', u'CH', u'JP', u'KN', u'KS', u'IR']),
    ('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\n\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ',
     [u'ECON', u'EINV', u'ENRG', u'PGOV', u'PBTS', u'MARR', u'BR']),
    #02ROME1196
    ('\nEO 12958 DECL: 03/05/2007\nTAGS PHUM, OPRC, OPRC, OPRC, OPRC, IT, ITPHUM, ITPHUM, ITPHUM, HUMAN RIGHTS\nSUBJECT: AS PREDICTED, ITALY’S HUMAN RIGHTS REPORT\nGENERATES FODDER FOR DOMESTIC POLITICAL MILLS', 
     [u'PHUM', u'OPRC', u'IT', u'ITPHUM', u'HUMAN RIGHTS']),
    # 09STATE11937
    ('E.O. 12958: DECL: 02/05/2019\nTAGS: OVIP CLINTON HILLARY PREL KPAL FR IR RS\nNATO, UK, CN\nSUBJECT: (U) Secreta',
    [u'OVIP', u'CLINTON, HILLARY', u'PREL', u'KPAL', u'FR', u'IR', u'RS', u'NATO', u'UK', u'CN']),
    #09BEIJING2964
    ('TAGS: OVIP STEINBERG JAMES PREL MNUC SN CH KN',
     [u'OVIP', u'STEINBERG, JAMES B.', u'PREL', u'MNUC', u'SN', u'CH', u'KN']),
    # 09SANTIAGO331
    ("E.O. 12958: DECL: 04/07/2019\nTAGS: OVIP BIDEN JOSEPH PREL ECON PGOV SOCI EU\nSUBJECT: VICE PRESIDENT BIDEN'S MARCH 28 MEETING WITH PRIME",
     [u'OVIP', u'BIDEN, JOSEPH', u'PREL', u'ECON', u'PGOV', u'SOCI', u'EU']),
    #08STATE100219
    ('E.O. 12958: DECL: 09/17/2018\nTAGS: OVIP RICE CONDOLEEZZA PREL PHSA SP KV CU\nBL, IS\nSUBJECT: Secretary Rice',
     [u'OVIP', u'RICE, CONDOLEEZZA', u'PREL', u'PHSA', u'SP', u'KV', u'CU', u'BL', u'IS']),
    # 04SANAA2346
    ('TAGS: MASS MOPS OVIP PARM PINR PREL PTER YM COUNTER TERRORISM',
     [u'MASS', u'MOPS', u'OVIP', u'PARM', u'PINR', u'PREL', u'PTER', u'YM', u'COUNTERTERRORISM']),
    # 05TELAVIV1580
    ('TAGS PGOV, PREL, KWBG, IR, IS, COUNTERTERRORISM, GOI EXTERNAL ',
     [u'PGOV', u'PREL', u'KWBG', u'IR', u'IS', u'COUNTERTERRORISM', u'GOI EXTERNAL']),
    ('TAGS PTER MARR, MOPPS',
     [u'PTER', u'MARR', u'MOPS']),
    ('TAGS: IS ISRAELI PALESTINIAN AFFAIRS GOI EXTERNAL',
     [u'IS', u'ISRAELI PALESTINIAN AFFAIRS', u'GOI', u'EXTERNAL']),
    ('TAGS: IS GAZA DISENGAGEMENT ISRAELI PALESTINIAN AFFAIRS',
     [u'IS', u'GAZA DISENGAGEMENT', u'ISRAELI PALESTINIAN AFFAIRS']),
    # 05BRASILIA2675
    ('TAGS: PREL PGOV BR OVIP ZOELLICK ROBERT US',
     [u'PREL', u'PGOV', u'BR', u'OVIP', u'ZOELLICK, ROBERT', u'US']),
    # 07BUENOSAIRES1673
    ('DECL: 08/22/2017 AGS: PGOV, PREL, ECON, SOCI, AR',
     [u'PGOV', u'PREL', u'ECON', u'SOCI', u'AR']),
)

def test_tags():
    def check(content, expected):
        assert parse_tags(content) == expected
    for content, expected in _TEST_DATA:
        yield check, content, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

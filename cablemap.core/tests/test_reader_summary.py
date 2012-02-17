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
Tests summary parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.reader import parse_summary

_TEST_DATA = (
    # 72TEHRAN5055
    ('REF: TEHRAN 4887\n\nSUMMARY: FOLLOWING ASSASSINATION [...].\nEND SUMMARY\n\n1. IN WAKE ',
     u'FOLLOWING ASSASSINATION [...].'),
    # 09BERLIN1197
    ('''Classified By: AMBASSADOR PHILIP D. MURPHY FOR REASONS 1.4 (B) and (D)\n\nSUMMARY\n-------\n\n1. (C) Chancellor Merkel [...].\nEnd Summary.\n\nOVERALL TREND: MAJOR PARTIES IN DECLINE''',
     u'Chancellor Merkel [...].'),
    # 09HAVANA35
    ('''Classified By: COM Jonathan Farrar for reasons 1.4 (b) and (d)\n\n1. (C) SUMMARY: Fidel Castro's [...].\n \nWHAT WE KNO''',
     "Fidel Castro's [...]."),
    # 07SAOPAULO464
    ('''------- SUMMARY -------\n\n1. Pope Benedict XVI's four-day [...] End Summary''',
     u"Pope Benedict XVI\'s four-day [...]"),
    # 07SAOPAULO250
    ('''------- SUMMARY -------\n\n1. Summary: On March 21, Pope Benedict XVI [...] End Summary. ''',
      u'On March 21, Pope Benedict XVI [...]'),
    # 09BERLIN1176
    ('''SUMMARY\n-------\n\n1. (C/NF) This is not a "change" election. [...]. END SUMMARY. ''',
     u'This is not a "change" election. [...].'),
    # 09BRASILIA1300
    ('''1. (U) Paragraphs 2 and 8 contain Mission Brazil action request.\n\n2. (C) Summary and Action Request. With Iranian President [...]. End Summary and Action Request. ''',
     u'With Iranian President [...].'),
    # 09BRASILIA1368
    ('''Summary -------\n\n2. (C) President Lula welcomed [...] End Summary''',
     u'President Lula welcomed [...]'),
    # 05PARIS7682
    ('1. (C) Summary and Comment: Continuing violent unrest in[...]. End Summary and Comment. ',
     u'Continuing violent unrest in[...].'),
    # 09BERLIN1548
    ('''1. (C/NF) Summary: In separate December 1 meetings [...] following way forward:\n\n-- the Interior Ministry [...]\n\nrelationship with Chancellor Merkel. End summary''',
     u'In separate December 1 meetings [...] following way forward:\n-- the Interior Ministry [...]\nrelationship with Chancellor Merkel.'),
    # 10BERLIN164
    ('''Classified By: Classified by Political M-C George Glass for reasons 1.4\n(b,d).\n\n1. (C) German FM Westerwelle told [...]. END SUMMARY.''',
     u'German FM Westerwelle told [...].'),
    # 09BRUSSELS536
    ('''Classified By: USEU EconMinCouns Peter Chase for reasons 1.4 (b), (d), (e).\n\n1. (S//NF) SUMMARY AND COMMENT: During a March 2-3 visit to\n\n2. (C) EU Member States and officials uniformly praised the\n\n3. (C) The content[...]. END SUMMARY AND COMMENT. ''',
     u'During a March 2-3 visit to\nEU Member States and officials uniformly praised the\nThe content[...].'),
    # 10BRASILIA61
    ('''CLASSIFIED BY: Thomas A. Shannon, Ambassador, State, Embassy Brasilia; REASON: 1.4(B), (D)\n1. (C) Summary. During separate [...]. End summary.''',
     u'During separate [...].'),
    # 09TRIPOLI715
    ('''CLASSIFIED BY: Gene A. Cretz, Ambassador, US Embassy Tripoli, Department of State. REASON: 1.4 (b), (d)\n\n1.(C) The August 31 African [...]. End Summary.''',
     u'The August 31 African [...].'),
    # 06TOKYO3567
    ('''OF 002   \n\n1.  Summary: (SBU) Japanese [...]. End Summary \n\n2. ''',
     u'Japanese [...].'),
    # 08THEHAGUE938
    ('''Classified By: Head of Economic Unit Shawn Gray, reasons 1.4 (b), (d)

1. (S) SUMMARY: The Dutch [...]. END
SUMMARY.

2. (S) Econoff delivered ''',
     u'The Dutch [...].'),
    # 08MANAMA492 (08ECTION01OF02MANAMA492)
    ('''1.(C) Summary: The GOB [...]. -------- Training --------

2.(U) Bah''',
     u'The GOB [...].'),
    # 09BRASILIA1300
    ('''Classified By: Charge D'Affaires Lisa Kubiske for reasons 1.4 (b) and ( d). 

1. (U) Paragraphs 2 and 8 contain Mission Brazil action request. 

2. (C) Summary and Action Request. With Iranian President [...] End Summary and Action Request.
''',
     u'With Iranian President [...]'),
    # 08MEXICO2382
    ('''
ISSUES (IWI) VISITS MEXICO

1. On 28 July 2008
[...]. End
Summary.

THE CIVIL SOCIETY PERSPECTIVE
-----------------------------
''',
     u'On 28 July 2008\n[...].'),
    # 05PANAMA1729
    (u'''Classified By: Charge d'Affaires Luis Arreaga for reasons 1.4 (B) AND (
D).

1. (SBU) This message is the first in a three‐part series on
views of the Torrijos administration's performance as it
approaches its September 1 first anniversary.

SUMMARY AND INTRODUCTION
‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐

2. (C) Martin Torrijos's [...]
performance, dashed expectations, and squandered
opportunities. END SUMMARY AND INTRODUCTION.

Great Expectations
‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐''',
     u'''Martin Torrijos's [...]\nperformance, dashed expectations, and squandered\nopportunities.'''),
    # 09STATE119085
    ('''Classified by: David Appleton, Director, 
INR/CCS, Reason: 1.4 (c, d). 
 
SUMMARY AND TABLE OF CONTENTS 
 
1.  (S/NF) [...]

2. [...]

END SUMMARY.

3. [...]''',
    u'''[...]\n[...]'''),
    # 08DHAKA856
    ('''Summary =======

1. (C) Bla bla. End Summary''',
     '''Bla bla.'''),
    # 04PANAMA715
    ('''Summary/Comment: bla bla
bla bla bla.  End Summary/Comment.
''',
    '''bla bla\nbla bla bla.'''),

)


def test_summary():
    def check(content, expected):
        eq_(expected, parse_summary(content))

    for content, expected in _TEST_DATA:
        yield check, content, expected

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

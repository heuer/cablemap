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
Tests cablemap.core.utils.subjectify

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.utils import titlefy

_TEST_DATA = (
    ('MISSILE TECHNOLOGY CONTROL REGIME (MTCR): "BROKERING CONTROLS IN THE UNITED STATES ON DUAL-USE ITEMS"',
     u'Missile Technology Control Regime (MTCR): "Brokering Controls in the United States on Dual-Use Items"'),
    ('germany requests release of xxxxxxxxxxxx nonpaper to the german criminal customs office',
      u'Germany Requests Release of XXXXXXXXXXXX Nonpaper to the German Criminal Customs Office'),
    # 8TRIPOLI227
    ('BACK TO THE FUTURE? QADHAFI CALLS FOR DRAMATIC SOCIO-ECONOMIC CHANGE IN GPC SPEECH',
      u'Back to the Future? Qadhafi Calls for Dramatic Socio-Economic Change in GPC Speech'),
    ("WESTERWELLE'S SURGE CLINCHES BLACK-YELLOW IN GERMANY; MERKEL GAINS SECOND TERM",
      u"Westerwelle's Surge Clinches Black-Yellow in Germany; Merkel Gains Second Term"),
    ('COALITION TESTED AS US-EU TFTP/SWIFT AGREEMENT PASSES ON GERMAN ABSTENTION',
     u'Coalition Tested as US-EU TFTP/SWIFT Agreement Passes on German Abstention'),
    # 09BERLIN1393    
    ("GERMANY'S NEW INTERIOR MINISTER FACES STEEP LEARNING CURVE",
     u"Germany's New Interior Minister Faces Steep Learning Curve"),
    # 09BERLIN1360
    ("THE NEW GERMAN CABINET - AN OVERVIEW",
     u'The New German Cabinet - An Overview'),
    # 09BERLIN1162
    ("GERMANY'S NEXT FOREIGN MINISTER?: THE WORLD ACCORDING TO FDP CHAIRMAN GUIDO WESTERWELLE",
     u"Germany's Next Foreign Minister?: The World According to FDP Chairman Guido Westerwelle"),
    # 10MEXICO141
    (u'Mexico’s Latin American Unity Summit -- Back to the Future?',
     u'Mexico’s Latin American Unity Summit -- Back to the Future?'),
    # 09BAKU744
    ('"LORDS OF THE MOUNTAINS" WILL FIGHT NO MORE FOREVER',
     u'"Lords of the Mountains" Will Fight No More Forever'),
    # 06HAVANA8633
    ('''"IF YOU DON'T HAVE YOUR HEALTH..." (AILMENTS AMONG THE CASTRO CLAN)''',
     u'''"If You Don't Have Your Health..." (Ailments Among the Castro Clan)'''),
    # 08LONDON2899
    (u"COTE D'IVOIRE: UK ON ELECTIONS, DDR, AND RE-ENERGIZING THE PROCESS",
     u"Cote D'Ivoire: UK on Elections, DDR, and Re-Energizing the Process"),
    # 06PARIS5974
    (u'FRENCH ELECTION 2007: NICOLAS SARKOZY -- THE CANDIDATE WHO MIGHT CHANGE FRANCE',
     u'French Election 2007: Nicolas Sarkozy -- The Candidate Who Might Change France'),
    # 08LONDON2542
    (u'PM BROWN DOES THE UNEXPECTED IN ADDRESSING ECONOMIC PROBLEMS',
     u'PM Brown Does the Unexpected in Addressing Economic Problems'),
    # 06BERLIN2546
    ("SPD IN DRIVER'S SEAT FOR BERLIN ELECTION",
     u"SPD in Driver's Seat for Berlin Election"),
    # 07TRIPOLI949
    ('''SLOW PROGRESS ON ITALY-LIBYA COLONIAL COMPENSATION TREATY A SIGN OF GOL'S "CORSAIR MENTALITY"''',
     u'''Slow Progress on Italy-Libya Colonial Compensation Treaty a Sign of GOL's "Corsair Mentality"'''),
    # 09TRIPOLI363
    ('SLA/U CAN NEGOTIATE ONLY WITH ASSURANCES THAT JEM AND KHARTOUM WILL ALSO LAY DOWN ARMS',
     u'SLA/U Can Negotiate Only With Assurances That Jem and Khartoum Will Also Lay Down Arms'),
    # 09LONDON2569
    ('HMG STRESSES U.S.-UK COORDINATION ON AFGHANISTAN STRATEGY',
     u'HMG Stresses U.S.-UK Coordination on Afghanistan Strategy'),
    # 10LONDON76
    ("AFGHANISTAN/YEMEN/IRAN: SENIOR UK-BASED DIPLOMATS DISCUSS AT CHINESE AMB'S FAREWELL DINNER",
     u"Afghanistan/Yemen/Iran: Senior UK-Based Diplomats Discuss at Chinese Amb's Farewell Dinner"),
    # 09LONDON2237
    ("Economists Warn UK's Economic Recovery Is Fragile",
     u"Economists Warn UK's Economic Recovery Is Fragile"),
    # 01VATICAN1261
    ('DROC--VATICAN DEMARCHE',
     u'DROC--Vatican Demarche'),
    # 01STATE176819
    ("AFGHANISTAN'S POLITICAL FUTURE (CORRECTED COPY)",
     u"Afghanistan's Political Future (Corrected Copy)"),
    # 04TASHKENT3180
    ('FIRST DAUGHTER LOLA (KARIMOVA) CUTS LOSE',
     u'First Daughter Lola (Karimova) Cuts Lose'),
    # 07TUNIS1489
    ("THE PNG'ING OF SUHA ARAFAT: MANY RUMORS, FEW FACTS",
     u"The PNG'ing of Suha Arafat: Many Rumors, Few Facts"),
    # 08LONDON1761
    ('CWS/BWC: CLOSE ALLIES MEETING, JUNE 17-18, 2008',
      u'CWS/BWC: Close Allies Meeting, June 17-18, 2008'),
)

def test_titlefy():
    def check(content, expected):
        eq_(expected, titlefy(content))
    for content, expected in _TEST_DATA:
        yield check, content, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

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
This module provides some global constants.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
import re

MIN_ORIGIN_LENGTH = len(u'ROME')
MAX_ORIGIN_LENGTH = len(u'BANDARSERIBEGAWAN')

MIN_SERIAL_LENGTH = 1
MAX_SERIAL_LENGTH = 6

_STATIONS = (
    # A
    'ABIDJAN', 'ABUDHABI', 'ABUJA', 'ACCRA', 'ADDISABABA', 
    'AITTAIPEI', 'ALGIERS', 'AMMAN', 'AMSTERDAM', 'ANKARA', 
    'ASHGABAT', 'ASMARA', 'ASTANA', 'ASUNCION', 'ATHENS', 
    # B
    'BAGHDAD', 'BAKU', 'BAMAKO', 'BANDARSERIBEGAWAN', 'BANGKOK', 
    'BANJUL', 'BARCELONA', 'BASRAH', 'BEIJING', 'BEIRUT', 
    'BELGRADE', 'BERLIN', 'BERN', 'BISHKEK', 'BOGOTA', 
    'BRASILIA', 'BRATISLAVA', 'BRIDGETOWN', 'BRUSSELS', 'BUCHAREST', 
    'BUDAPEST', 'BUENOSAIRES', 'BUJUMBURA', 'BRAZZAVILLE',
    # C
    'CAIRO', 'CANBERRA', 'CAPETOWN', 'CARACAS', 'CASABLANCA', 
    'CHISINAU', 'COLOMBO', 'CONAKRY', 'COPENHAGEN', 'CURACAO', 
    # D
    'DAKAR', 'DAMASCUS', 'DARESSALAAM', 'DHAKA', 'DJIBOUTI', 
    'DOHA', 'DUBAI', 'DUBLIN', 'DUSHANBE', 'DHAHRAN',
    # E
    'EFTOLONDON', 'EFTOTRIPOLI', 
    # F
    'FREETOWN', 
    # G
    'GABORONE', 'GENEVA', 'GUATEMALA', 
    # H
    'HAMBURG', 'HANOI', 'HARARE', 'HAVANA', 'HAMILTON',
    # I
    'IRANRPODUBAI', 'ISLAMABAD', 'ISTANBUL', 'JAKARTA', 
    # J
    'JEDDAH', 'JERUSALEM', 
    # K
    'KABUL', 'KAMPALA', 'KHARTOUM', 'KIEV', 'KIGALI', 
    'KINSHASA', 'KUALALUMPUR', 'KUWAIT', 'KYIV', 
    # L
    'LAGOS', 'LAPAZ', 'LILONGWE', 'LIMA', 'LISBON', 'LONDON', 
    'LUANDA', 'LUXEMBOURG', 
    # M
    'MADRID', 'MANAGUA', 'MANAMA', 'MAPUTO', 'MEXICO', 
    'MINSK', 'MONROVIA', 'MONTERREY', 'MONTEVIDEO', 'MONTREAL', 
    'MOSCOW', 'MUNICH', 'MUSCAT', 
    # N
    'NAIROBI', 'NAPLES', 'NASSAU', 'NEWDELHI', 'NIAMEY',
    # O 
    'OSLO', 'OTTAWA', 'OUAGADOUGOU', 
    # P
    'PANAMA', 'PARAMARIBO', 'PARIS', 'PARTO', 'PESHAWAR', 
    'PHNOMPENH', 'PORTAUPRINCE', 'PRAGUE', 'PRETORIA', 'PRISTINA', 
    # Q
    'QUITO', 
    # R
    'RABAT', 'RANGOON', 'RECIFE', 'REYKJAVIK', 'RIGA', 
     'RIODEJANEIRO', 'RIYADH', 'ROME', 'RPODUBAI', 
    # S 
    'SANAA', 'SANJOSE', 'SANSALVADOR', 'SANTIAGO', 'SANTODOMINGO', 
    'SAOPAULO', 'SARAJEVO', 'SCTION', 'SECTION', 'SEOUL', 
    'SHANGHAI', 'SHENYANG', 'SINGAPORE', 'SKOPJE', 'SOFIA', 
    'STATE', 'STOCKHOLM', 'STRASBOURG', 
    # T
    'TALLINN', 'TASHKENT', 'TBILISI', 'TEGUCIGALPA', 'TEHRAN', 
    'TELAVIV', 'THEHAGUE', 'TOKYO', 'TRIPOLI', 'TUNIS', 
    # U
    'ULAANBAATAR', 'UNVIEVIENNA', 'USNATO', 'USUNNEWYORK',
    # V
    'VATICAN', 'VIENNA', 'VILNIUS', 'VLADIVOSTOK', 
    # W
    'WARSAW', 'WELLINGTON', 'WINDHOEK', 
    # Y
    'YAOUNDE', 'YEREVAN', 
    # Z
    'ZAGREB'
)

REFERENCE_ID_PATTERN = re.compile(r'^([0-9]{2})(%s)([0-9]{%d,%d})$' % ('|'.join(_STATIONS), MIN_SERIAL_LENGTH, MAX_SERIAL_LENGTH), re.UNICODE)

# WikiLeak cable identifiers which are wrong
MALFORMED_CABLE_IDS = {
    '08SCTION02OF02SAOPAULO335': u'08SAOPAULO335',
    '08SECTION01GF02BISHIEK21': u'08BISHKEK1021',
    '09SECTION02OF03QRIPOLI583': u'09TRIPOLI583',
}

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

# Min/max length of station identifiers
MIN_ORIGIN_LENGTH = len(u'ROME')
MAX_ORIGIN_LENGTH = len(u'BANDARSERIBEGAWAN')

# Reference kind constants
REF_KIND_UNKNOWN = 0
REF_KIND_CABLE = 1
REF_KIND_EMAIL = 2
REF_KIND_BOOK = 3
REF_KIND_TEL = 4
REF_KIND_REPORT = 5
REF_KIND_FAX = 6
REF_KIND_MEMO = 7
REF_KIND_MEETING = 8
REF_KIND_WEB = 9

# Min/max cable serial number length
MIN_SERIAL_LENGTH = 1
MAX_SERIAL_LENGTH = 7

# Valid station identifiers
_STATIONS = (
    # A
    u'ABIDJAN', u'ABUDHABI', u'ABUJA', u'ACCRA', u'ADDISABABA', 
    u'AITTAIPEI', u'ALGIERS', u'AMMAN', u'AMSTERDAM', u'ANKARA', 
    u'ASHGABAT', u'ASMARA', u'ASTANA', u'ASUNCION', u'ATHENS',
    u'ADANA', u'ALMATY', u'APIA', u'AUCKLAND', u'ANTANANARIVO',
    u'ALEXANDRIA',
    # B
    u'BAGHDAD', u'BAKU', u'BAMAKO', u'BANDARSERIBEGAWAN', u'BANGKOK', 
    u'BANJUL', u'BARCELONA', u'BASRAH', u'BEIJING', u'BEIRUT', 
    u'BELGRADE', u'BERLIN', u'BERN', u'BISHKEK', u'BOGOTA', 
    u'BRASILIA', u'BRATISLAVA', u'BRIDGETOWN', u'BRUSSELS', u'BUCHAREST', 
    u'BUDAPEST', u'BUENOSAIRES', u'BUJUMBURA', u'BRAZZAVILLE', u'BELIZE',
    u'BELFAST', u'BELMOPAN', u'BONN', u'BANGUI',
    u'BENIN', # found in cable refs
    # C
    u'CAIRO', u'CALCUTTA', u'CANBERRA', u'CAPETOWN', u'CARACAS', 
    u'CASABLANCA', u'CHENNAI', u'CHISINAU', u'CIUDADJUAREZ', u'COLOMBO', 
    u'CONAKRY', u'COPENHAGEN', u'CURACAO', u'CALGARY', u'CHIANGMAI',
    u'CHENGDU', u'COTONOU', u'CDGENEVA',
    u'CDCATLANTAGA', # found in cable refs "Centers for Disease Control and Prevention"
    u'CHARLESTON', # found in cable refs
    u'CDC', # found in cable refs
    # D
    u'DAKAR', u'DAMASCUS', u'DARESSALAAM', u'DHAKA', u'DJIBOUTI', 
    u'DOHA', u'DUBAI', u'DUBLIN', u'DUSHANBE', u'DHAHRAN', u'DILI',
    u'DURBAN', u'DAMASCCUS',
    u'DUSSELDORF', # found in cable refs
    u'USDOJ', # found in cable refs
    # F
    u'FREETOWN', u'FUKUOKA', u'FSINFATC', u'FRANKFURT', u'FLORENCE', u'FESTTWO',
    # G
    u'GABORONE', u'GENEVA', u'GUATEMALA', u'GUADALAJARA', u'GUAYAQUIL',
    u'GUANGZHOU', u'GEORGETOWN', u'GRENADA',
    # H
    u'HAMBURG', u'HANOI', u'HARARE', u'HAVANA', u'HAMILTON', u'HELSINKI', u'HERMOSILLO',
    u'HALIFAX', u'HOCHIMINHCITY', u'HONGKONG', u'HILLAH', u'HYDERABAD',
    # I
    u'IRANRPODUBAI', u'ISLAMABAD', u'ISTANBUL', u'IZMIR',
    # J
    u'JEDDAH', u'JERUSALEM', u'JAKARTA', u'JOHANNESBURG',
    # K
    u'KABUL', u'KAMPALA', u'KATHMANDU', u'KHARTOUM', u'KIEV', u'KIGALI', 
    u'KINSHASA', u'KUALALUMPUR', u'KUWAIT', u'KYIV', u'KOLKATA', u'KINGSTON',
    u'KARACHI', u'KRAKOW', u'KOLONIA', u'KIRKUK', u'KOROR', u'KADUNA',
    # L
    u'LAGOS', u'LAPAZ', u'LAHORE', u'LILONGWE', u'LIMA', u'LISBON', u'LJUBLJANA',
    u'LONDON', u'LUANDA', u'LUXEMBOURG', u'LIBREVILLE', u'LUSAKA', u'LEIPZIG',
    u'LOME', # Found in cable refs
    # M
    u'MALABO', u'MADRID', u'MANAGUA', u'MANAMA', u'MAPUTO', u'MBABANE', u'MEXICO', 
    u'MILAN', u'MINSK', u'MONROVIA', u'MONTERREY', u'MONTEVIDEO', u'MONTREAL', 
    u'MOSCOW', u'MUMBAI', u'MUNICH', u'MUSCAT', u'MELBOURNE', u'MANILA',
    u'MATAMOROS', u'MASERU', u'MOGADISHU', u'MARSEILLE', u'MERIDA', u'MAJURO', u'MOSUL',
    u'MONTEREY', # Found in cable refs
    # N
    u'NAIROBI', u'NAPLES', u'NASSAU', u'NEWDELHI', u'NIAMEY', u'NICOSIA',
    u'NDJAMENA', u'NAHA', u'NUEVOLAREDO', u'NAGOYA', u'NOUAKCHOTT', u'NOGALES',
    # O 
    u'OSLO', u'OTTAWA', u'OUAGADOUGOU', u'OSAKAKOBE',
    # P
    u'PANAMA', u'PARAMARIBO', u'PARIS', u'PARTO', u'PESHAWAR', 
    u'PHNOMPENH', u'PORTAUPRINCE', u'PRAGUE', u'PRETORIA', u'PRISTINA',
    u'PORTLOUIS', u'PORTOFSPAIN', u'PODGORICA', u'PORTMORESBY', u'PERTH',
    u'PONTADELGADA',
    u'PARISFR', # Used for US Mission UNESCO, see also UNESCOPARISFR
    u'PRAIA', # Found in cable references
    # Q
    u'QUITO', u'QUEBEC',
    # R
    u'RABAT', u'RANGOON', u'RECIFE', u'REYKJAVIK', u'RIGA', 
    u'RIODEJANEIRO', u'RIYADH', u'ROME', u'RPODUBAI', 
    # S 
    u'SANAA', u'SANJOSE', u'SANSALVADOR', u'SANTIAGO', u'SANTODOMINGO', 
    u'SAOPAULO', u'SARAJEVO', u'SEOUL', u'SHANGHAI', u'SHENYANG', u'SINGAPORE',
    u'SKOPJE', u'SOFIA', u'STATE', u'STOCKHOLM', u'STRASBOURG', u'STPETERSBURG',
    u'SUVA', u'SAPPORO', u'SECDEF', u'SYDNEY', u'SURABAYA',
    # T
    u'TALLINN', u'TASHKENT', u'TAIPEI', u'TBILISI', u'TEGUCIGALPA', u'TEHRAN', 
    u'TELAVIV', u'THEHAGUE', u'TIJUANA', u'TOKYO', u'TRIPOLI', u'TUNIS',
    u'TORONTO', u'THESSALONIKI', u'TIRANA',
    # U
    u'ULAANBAATAR', u'UNVIEVIENNA', u'USNATO', u'USUNNEWYORK', u'USEUBRUSSELS',
    u'USOSCE', u'UNROME', u'USTRGENEVA',
    u'USDAFAS', # Found in cable references and stands for "U.S. Department of Agriculture"
    u'USDOC', # Found in REFerences and stands for "United States Department of Commerce"
    u'USCBP', # Found in refs and stands for "U.S. Customs and Border Protection"
    u'UNESCOPARISFR', # Same as PARISFR
    # V
    u'VATICAN', u'VIENNA', u'VILNIUS', u'VLADIVOSTOK', u'VALLETTA', u'VANCOUVER',
    u'VIENTIANE',
    # W
    u'WARSAW', u'WELLINGTON', u'WINDHOEK', u'WASHDC',
    u'WHITEHOUSE', # Found in cable refs
    # Y
    u'YAOUNDE', u'YEREVAN', u'YEKATERINBURG',
    # Z
    u'ZAGREB'
)

REFERENCE_ID_PATTERN = re.compile(r'^([0-9]{2})(%s)([0-9]{%d,%d})$' % ('|'.join(_STATIONS), MIN_SERIAL_LENGTH, MAX_SERIAL_LENGTH), re.UNICODE)

# Wrong WikiLeaks cable identifiers
MALFORMED_CABLE_IDS = {
    u'08SCTION02OF02SAOPAULO335': u'08SAOPAULO335',
    u'09SECTION02OF03QRIPOLI583': u'09TRIPOLI583',
    u'08ECTION01OF02MANAMA492': u'08MANAMA492',
}

# Wrong WikiLeaks cable identifiers w/o a valid equivalent
INVALID_CABLE_IDS = {
    # Format:
    # Invalid cable ID: Cable ID which would be correct
    u'09EFTOHELSINKI235': u'09HELSINKI235',
    u'08SECTION01GF02BISHIEK21': u'08BISHKEK1021', # See <http://aebr.home.xs4all.nl/wl/corrupted/corrupted.html>
    u'09SECTION01OF03SANJOSE525': u'09SANJOSE525',
    u'07EFTOOTTAWA1217': u'07OTTAWA1217',
    u'06BRAILIA1079': u'06BRASILIA1079',
    u'07BRASIIA1568': u'07BRASILIA1568',
    u'06EFTOSANAA1621': u'06SANAA1621',
    u'08EFTOPHNOMPENH416': u'08PHNOMPENH416',
    u'09EFTOLONDON2468': u'09LONDON2468',
    u'09EFTOLONDON2884': u'09LONDON2884',
    u'09EFTOLONDON2858': u'09LONDON2858',
    u'08EFTOLONDON2883': u'08LONDON2883',
    u'09EFTOLONDON2187': u'09LONDON2187',
    u'10EFTOLONDON16': u'10LONDON16',
    u'09EFTOLONDON2363': u'09LONDON2363',
    u'09EFTOLONDON2618': u'09LONDON2618',
    u'09EFTOLONDON2240': u'09LONDON2240',
    u'09EFTOLONDON2211': u'09LONDON2211',
    u'09EFTOLONDON2521': u'09LONDON2521',
    u'09EFTOLONDON2688': u'09LONDON2688',
    u'09EFTOLONDON2905': u'09LONDON2905',
    u'09EFTOTRIPOLI704': u'09TRIPOLI704',
    u'09EFTOLONDON2239': u'09LONDON2239',
    u'09BAU339': u'09BAKU339',
    u'09EFTOSANAA433': u'09SANAA433',
    u'10EFTOKABUL597': u'10KABUL597',
    u'09SECION02OF02NAIROBI417': u'09NAIROBI417',
    u'08AITTAIPIE1698': u'08TAIPEI1698',
    u'07SECTION02OF03EIJING483': u'07BEIJING483',
    u'09COPENHAEN13': u'09COPENHAGEN13',
    u'09EFTOASMARA34': u'09ASMARA34',
    u'06EFTOUSUNNEWYORK1560': u'06USUNNEWYORK1560',
    u'08EFTOJAKARTA2073': u'08JAKARTA2073',
    u'06EFTOANKARA4972': u'06ANKARA4972',
    u'08SECTIN03OF03KABUL3036': u'08KABUL3036',
    u'07EFTOATHENS404': u'07ATHENS404',
    u'06EFTOANKARA5010': u'06ANKARA5010',
    u'10EFTOKABUL668': u'10KABUL668',
    u'06EFTOKABUL5893': u'06KABUL5893',
    u'08EFTODAMASCUS487': u'08DAMASCUS487',
    u'06EFTOANKARA5097': u'06ANKARA5097',
    u'08SECTIO01OF02JERUSALEM1847': u'08JERUSALEM1847',
    u'07SECTION01OF03ANKARA365': u'07ANKARA365',
    u'07EFTOSANAA2300': u'07SANAA2300',
    u'07EFTOSANAA588': u'07SANAA588',
    u'06EFTOPORTMORESBY350': u'06PORTMORESBY350',
    u'07EFTOSANAA588': u'07SANAA588',
    u'09AMEMBASSYHANOI1292': u'09HANOI1292',
    u'06EFTOCARACAS943': u'06CARACAS943',
    u'06EFTOCARACAS2252': u'06CARACAS2252',
    u'07EFTOSANAA784': u'07SANAA784',
    u'06EFTOSANAA1996': u'06SANAA1996',
    u'08SECTON01OF02BEIRUT896': u'08BEIRUT896',
    u'06EFTOBAKU1165': u'06BAKU1165',
    u'092OF5': u'09STATE126780', # Unsure about the s/n
}

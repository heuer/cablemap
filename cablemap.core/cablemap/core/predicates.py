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
Predicates to filter cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import absolute_import
import re
from functools import partial
from .c14n import canonicalize_id

_YEAR_ORIGIN_PATTERN = re.compile(r'([0-9]{2})([A-Z\-]+)[0-9]+')

def year_origin_filter(year_predicate=None, origin_predicate=None):
    def accept(cable_id, predicate):
        year, origin = _YEAR_ORIGIN_PATTERN.match(canonicalize_id(cable_id)).groups()
        return predicate(year, origin)
    if year_predicate and origin_predicate:
        return partial(accept, predicate=lambda y, o: year_predicate(y) and origin_predicate(o))
    elif year_predicate:
        return partial(accept, predicate=lambda y, o: year_predicate(y))
    elif origin_predicate:
        return partial(accept, predicate=lambda y, o: origin_predicate(o))
    return lambda cable_id: True

def year_filter(predicate):
    """\

    """
    return year_origin_filter(year_predicate=predicate)

def origin_filter(predicate):
    """\

    """
    return year_origin_filter(origin_predicate=predicate)

def origin_europe(origin):
    """\
    Returns if the origin is located in Europe.

    This holds true for the following countries:
    * Albania
    * Armenia
    * Austria
    * Azerbaijan
    * Belarus
    * Belgium
    * Bulgaria
    * Bosnia and Herzegovina
    * Bulgaria
    * Croatia
    * Cyprus
    * Czech
    * Denmark
    * Estonia
    * Finland
    * France
    * Georgia
    * Germany
    * Greece
    * Hungary
    * Iceland
    * Ireland
    * Italy
    * Kazakhstan
    * Latvia
    * Lithuania
    * Luxembourg
    * Macedonia
    * Malta
    * Moldova
    * Montenegro
    * Netherlands
    * Normway
    * Poland
    * Portugal
    * Romania
    * Russia
    * Serbia
    * Slovakia
    * Slovenia
    * Spain
    * Sweden
    * Switzerland
    * Turkey
    * Ukraine
    * United Kingdom
    * Vatican (Holy See)
    """
    return origin_albania(origin) or origin_armenia(origin) or origin_austria(origin) \
           or origin_azerbaijan(origin) or origin_belarus(origin) or origin_belgium(origin) \
           or origin_bulgaria(origin) or origin_bosnia_and_herzegovina(origin) or origin_bulgaria(origin) \
           or origin_croatia(origin) or origin_cyprus(origin) or origin_czech(origin) \
           or origin_denmark(origin) or origin_estonia(origin) or origin_finland(origin) \
           or origin_france(origin) or origin_georgia(origin) or origin_germany(origin) \
           or origin_greece(origin) or origin_hungary(origin) or origin_iceland(origin) \
           or origin_ireland(origin) or origin_northern_ireland(origin) or origin_italy(origin) \
           or origin_kazakhstan(origin) or origin_latvia(origin) or origin_lithuania(origin) \
           or origin_luxembourg(origin) or origin_macedonia(origin) or origin_malta(origin) \
           or origin_moldova(origin) or origin_montenegro(origin) or origin_netherlands(origin) \
           or origin_norway(origin) or origin_poland(origin) or origin_portugal(origin) \
           or origin_romania(origin) or origin_russia(origin) or origin_serbia(origin) \
           or origin_slovakia(origin) or origin_slovenia(origin) or origin_spain(origin) \
           or origin_sweden(origin) or origin_switzerland(origin) or origin_turkey(origin) \
           or origin_ukraine(origin) or origin_united_kingdom(origin) or origin_vatican(origin)

def origin_north_africa(origin):
    """\
    Returns if the origin is located in North Africa.

    * Algeria
    * Egypt
    * Libya
    * Morocco
    * Sudan
    * Tunisia
    """
    return origin_egypt(origin) or origin_algeria(origin) or origin_libya(origin) \
           or origin_morocco(origin) or origin_sudan(origin) or origin_tunisia(origin)

def origin_west_africa(origin):
    """\
    Returns if the origin is located in West Africa.

    Holds true for the following countries:
    * Benin
    * Burkin Faso
    * Cape Verde
    * Cote d'Ivoire
    * Gambia
    * Ghana
    * Guinea
    * Liberia
    * Mali
    * Mauritania
    * Niger
    * Nigeria
    * Senegal
    * Sierra Leone
    * Togo
    """
    return origin_benin(origin) or origin_burkina_faso(origin) or origin_cape_verde(origin) \
           or origin_cote_divoire(origin) or origin_gambia(origin) or origin_ghana(origin) \
           or origin_guinea(origin) or origin_liberia(origin) or origin_mali(origin) \
           or origin_mauritania(origin) or origin_niger(origin) or origin_nigeria(origin) \
           or origin_senegal(origin) or origin_sierra_leone(origin) or origin_togo(origin)

def origin_central_asia(origin):
    """\
    Returns if the origin is located in Central Asia.

    * Afghanistan
    * Kazakhstan
    * Kyrgyzstan
    * Tajikistan
    * Turkmenistan
    * Uzbekistan
    """
    return origin_afghanistan(origin) or origin_kazakhstan(origin) or origin_kyrgyzstan(origin) \
           or origin_tajikistan(origin) or origin_turkmenistan(origin) or origin_uzbekistan(origin)

def origin_east_asia(origin):
    """\
    Returns if the origin is located in East Asia

    * China
    * Japan
    * Mongolia
    * South Korea
    * Taiwan
    """
    return origin_china(origin) or origin_japan(origin) or origin_mongolia(origin) \
           or origin_south_korea(origin) or origin_taiwan(origin)

def origin_west_asia(origin):
    """\
    Returns if the origin is located in Western Asia.

    * Armenia
    * Azerbaijan
    * Bahrain
    * Cyprus
    * Georgia
    * Iraq
    * Israel
    * Jordan
    * Kuwait
    * Lebanon
    * Oman
    * Qatar
    * Saudi Arabia
    * Syria
    * Turkey
    * United Arab Emirates
    * Yemen
    """
    return origin_armenia(origin) or origin_azerbaijan(origin) or origin_bahrain(origin) \
           or origin_cyprus(origin) or origin_georgia(origin) or origin_georgia(origin) \
           or origin_iraq(origin) or origin_israel(origin) or origin_jordan(origin) \
           or origin_kuwait(origin) or origin_lebanon(origin) or origin_oman(origin) \
           or origin_qatar(origin) or origin_saudi_arabia(origin) or origin_syria(origin) \
           or origin_turkey(origin) or origin_united_arab_emirates(origin) or origin_yemen(origin)

def origin_usdel(origin):
    """\
    Returns if the origin is a U.S. Delegation.
    """
    return origin == u'PARTO'

def origin_afghanistan(origin):
    """\

    """
    return origin == u'KABUL'

def origin_albania(origin):
    """\

    """
    return origin == u'TIRANA'

def origin_algeria(origin):
    """\

    """
    return origin == u'ALGIERS'

def origin_angola(origin):
    """\

    """
    return origin == u'LUANDA'

def origin_argentinia(origin):
    """\

    """
    return origin == u'BUENOSAIRES'

def origin_armenia(origin):
    """\

    """
    return origin == u'YEREVAN'

def origin_australia(origin):
    """\

    """
    return origin in u'MELBOURNE', u'SYDNEY', u'PERTH', u'CANBERRA'

def origin_austria(origin):
    """\

    """
    # Matches U.S. Mission to Vienna and Vienna
    return u'VIENNA' in origin

def origin_azerbaijan(origin):
    """\

    """
    return origin == u'BAKU'

def origin_bahamas(origin):
    """\
    """
    return origin == u'NASSAU'

def origin_bahrain(origin):
    """\

    """
    return origin == u'MANAMA'

def origin_bangladesh(origin):
    """\

    """
    return origin == u'DHAKA'

def origin_barbados(origin):
    """\

    """
    return origin == u'BRIDGETOWN',

def origin_belarus(origin):
    """\

    """
    return origin == u'MINSK'

def origin_belgium(origin):
    """\

    """
    # Matches U.S. Mission to EU, Brussels and Brussels
    return u'BRUSSELS' in origin

def origin_belize(origin):
    """\

    """
    return origin == u'BELMOPAN'

def origin_benin(origin):
    """\

    """
    return origin == u'COTONOU'

def origin_bermuda(origin):
    """\

    """
    return origin == u'HAMILTON'

def origin_bolivia(origin):
    """\

    """
    return origin == u'LAPAZ'

def origin_bosnia_and_herzegovina(origin):
    """\

    """
    return origin == u'SARAJEVO'

def origin_botswana(origin):
    """\

    """
    return origin == u'GABORONE'

def origin_brazil(origin):
    """\

    """
    return origin in (u'BRASILIA', u'SAOPAULO', u'RIODEJANEIRO', u'RECIFE')

def origin_brunei(origin):
    """\

    """
    return origin == u'BANDARSERIBEGAWAN'

def origin_bulgaria(origin):
    """\

    """
    return origin == u'SOFIA'

def origin_burkina_faso(origin):
    """\

    """
    return origin == u'OUAGADOUGOU'

def origin_burma(origin):
    """\

    """
    return origin == u'RANGOON'

def origin_burundi(origin):
    """\

    """
    return origin == u'BUJUMBURA'

def origin_cambodia(origin):
    """\

    """
    return origin == u'PHNOMPENH'

def origin_cameroon(origin):
    """\

    """
    return origin == u'YAOUNDE'

def origin_canada(origin):
    """\

    """
    return origin in (u'CALGARY', u'HALIFAX', u'MONTREAL', u'QUEBEC', u'OTTAWA', u'TORONTO', u'VANCOUVER')

def origin_cape_verde(origin):
    """\

    """
    return origin == u'PRAIA'

def origin_central_african_republic(origin):
    """\

    """
    return origin == u'BANGUI'

def origin_chad(origin):
    """\

    """
    return origin == u'NDJAMENA'

def origin_chile(origin):
    """\

    """
    return origin == u'SANTIAGO'

def origin_china(origin):
    """\

    """
    return origin in (u'BEIJING', u'CHENGDU', u'GUANGZHOU', u'HONGKONG', u'SHANGHAI', u'SHENYANG')

def origin_colombia(origin):
    """\

    """
    return origin == u'BOGOTA'

def origin_costa_rica(origin):
    """\

    """
    return origin == u'SANJOSE'

def origin_cote_divoire(origin):
    """\

    """
    return origin == u'ABIDJAN'

def origin_croatia(origin):
    """\

    """
    return origin == u'ZAGREB'

def origin_cuba(origin):
    """\

    """
    return origin == u'HAVANA'

def origin_curacao(origin):
    """\

    """
    return origin == u'CURACA'

def origin_cyprus(origin):
    """\

    """
    return origin == u'NICOSIA'

def origin_czech(origin):
    """\

    """
    return origin == u'PRAGUE'

def origin_democratic_republic_congo(origin):
    """\

    """
    return origin == u'KINSHASA'

def origin_denmark(origin):
    """\

    """
    return origin == u'COPENHAGEN'

def origin_djibouti(origin):
    """\

    """
    return origin == u'DJIBOUTI'

def origin_dominican_republic(origin):
    """\

    """
    return origin == u'SANTODOMINGO'

def origin_east_timor(origin):
    """\

    """
    return origin == u'DILI'

def origin_ecuador(origin):
    """\

    """
    return origin == u'QUITO'

def origin_egypt(origin):
    """\

    """
    return origin in (u'CAIRO', u'ALEXANDRIA')

def origin_el_salvador(origin):
    """\

    """
    return origin == u'SANSALVADOR'

def origin_equatorial_guinea(origin):
    """\

    """
    return origin == u'MALABO'

def origin_eritrea(origin):
    """\

    """
    return origin == u'ASMARA'

def origin_estonia(origin):
    """\

    """
    return origin == u'TALLINN'

def origin_ethiopia(origin):
    """\

    """
    return origin == u'ADDISABABA'

def origin_micronesia(origin):
    """\

    """
    return origin == u'KOLONIA'

def origin_fiji(origin):
    """\

    """
    return origin == u'SUVA'

def origin_finland(origin):
    """\

    """
    return origin == u'HELSINKI'

def origin_france(origin):
    """\

    """
    return origin in (u'MARSEILLE', u'PARIS', u'STRASBOURG')

def origin_gabon(origin):
    """\

    """
    return origin == u'LIBREVILLE'

def origin_gambia(origin):
    """\

    """
    return origin == u'BANJUL'

def origin_georgia(origin):
    """\

    """
    return origin == u'TBILISI'

def origin_germany(origin):
    """\

    """
    return origin in (u'BONN', u'BERLIN', u'DUSSELDORF', u'FRANKFURT', u'HAMBURG', u'LEIPZIG', u'MUNICH')

def origin_ghana(origin):
    """\

    """
    return origin == u'ACCRA'

def origin_greece(origin):
    """\

    """
    return origin in (u'ATHENS', u'THESSALONIKI')

def origin_grenada(origin):
    """\

    """
    return origin == u'BRIDGETOWN'

def origin_guatemala(origin):
    """\

    """
    return origin == u'GUATEMALA'

def origin_guinea(origin):
    """\

    """
    return origin == u'CONAKRY'

def origin_guyana(origin):
    """\

    """
    return origin == u'GEORGETOWN'

def origin_haiti(origin):
    """\

    """
    return origin == u'PORTAUPRINCE'

def origin_honduras(origin):
    """\

    """
    return origin == u'TEGUCIGALPA'

def origin_hungary(origin):
    """\

    """
    return origin == u'BUDAPEST'

def origin_iceland(origin):
    """\

    """
    return origin == u'REYKJAVIK'

def origin_india(origin):
    """\

    """
    return origin in (u'CHENNAI', u'KOLKATA', u'MUMBAI', u'NEWDELHI')

def origin_indonesia(origin):
    """\

    """
    return origin in (u'JAKARTA', u'SURABAYA')

def origin_iran(origin):
    """\

    """
    return origin in (u'TEHRAN', u'RPODUBAI')

def origin_iraq(origin):
    """\

    """
    return origin == u'BAGHDAD' \
           or u'BASRAH' in origin \
           or u'HILLAH' in origin \
           or u'KIRKUK' in origin \
           or u'MOSUL' in origin

def origin_ireland(origin):
    """\

    """
    return origin == u'DUBLIN'

def origin_israel(origin):
    """\

    """
    return origin in (u'JERUSALEM', u'TELAVIV')

def origin_italy(origin):
    """\

    """
    return origin in (u'FLORENCE', u'MILAN', u'NAPLES') or u'ROME' in origin

def origin_jamaica(origin):
    """\

    """
    return origin == u'KINGSTON'

def origin_japan(origin):
    """\

    """
    return origin in (u'FUKUOKA', u'NAGOYA', u'NAHA', u'OSAKAKOBE', u'SAPPORO', u'TOKYO')

def origin_jordan(origin):
    """\

    """
    return origin == u'AMMAN'

def origin_kazakhstan(origin):
    """\

    """
    return origin in (u'ASTANA', u'ALMATY')

def origin_kenya(origin):
    """\

    """
    return origin == u'NAIROBI'

def origin_kosovo(origin):
    """\

    """
    return origin == u'PRISTINA'

def origin_kuwait(origin):
    """\

    """
    return origin == u'KUWAIT'

def origin_kyrgyzstan(origin):
    """\

    """
    return origin == u'BISHKEK'

def origin_laos(origin):
    """\

    """
    return origin == u'VIENTIANE'

def origin_latvia(origin):
    """\

    """
    return origin == u'RIGA'

def origin_lebanon(origin):
    """\

    """
    return origin == u'BEIRUT'

def origin_lesotho(origin):
    """\

    """
    return origin == u'MASERU'

def origin_liberia(origin):
    """\

    """
    return origin == u'MONROVIA'

def origin_libya(origin):
    """\

    """
    return origin == u'TRIPOLI'

def origin_lithuania(origin):
    """\

    """
    return origin == u'VILNIUS'

def origin_luxembourg(origin):
    """\

    """
    return origin == u'LUXEMBOURG'

def origin_macedonia(origin):
    """\

    """
    return origin == u'SKOPJE'

def origin_madagascar(origin):
    """\

    """
    return origin == u'ANTANANARIVO'

def origin_majuro(origin):
    """\

    """
    return origin == u'MAJURO'

def origin_malawi(origin):
    """\

    """
    return origin == u'LILONGWE'

def origin_malaysia(origin):
    """\

    """
    return origin == u'KUALALUMPUR'

def origin_mali(origin):
    """\

    """
    return origin == u'BAMAKO'

def origin_malta(origin):
    """\

    """
    return origin == u'VALLETTA'

def origin_mauritania(origin):
    """\

    """
    return origin == u'NOUAKCHOTT'

def origin_mauritius(origin):
    """\

    """
    return origin == u'PORTLOUIS'

def origin_mexico(origin):
    """\

    """
    return origin in (u'CIUDADJUAREZ', u'GUADALAJARA', u'HERMOSILLO',
                      u'MATAMOROS', u'MERIDA', u'MEXICO', u'MONTERREY', u'NOGALES',
                      u'NUEVOLAREDO', u'TIJUANA')

def origin_moldova(origin):
    """\

    """
    return origin == u'CHISINAU'

def origin_mongolia(origin):
    """\

    """
    return origin == u'ULAANBAATAR'

def origin_montenegro(origin):
    """\

    """
    return origin == u'PODGORICA'

def origin_morocco(origin):
    """\

    """
    return origin in (u'CASABLANCA', u'RABAT')

def origin_mozambique(origin):
    """\

    """
    return origin == u'MAPUTO'

def origin_namibia(origin):
    """\

    """
    return origin == u'WINDHOEK'

def origin_nepal(origin):
    """\

    """
    return origin == u'KATHMANDU'

def origin_netherlands(origin):
    """\

    """
    return origin in (u'AMSTERDAM', u'THEHAGUE')

def origin_new_zealand(origin):
    """\

    """
    return origin in (u'AUCKLAND', u'WELLINGTON')

def origin_nicaragua(origin):
    """\

    """
    return origin == u'MANAGUA'

def origin_niger(origin):
    """\

    """
    return origin == u'NIAMEY'

def origin_nigeria(origin):
    """\

    """
    return origin in (u'ABUJA', u'KADUNA', u'LAGOS')

def origin_usnato(origin):
    """\

    """
    return origin == u'USNATO'

def origin_northern_ireland(origin):
    """\

    """
    return origin == u'BELFAST'

def origin_norway(origin):
    """\

    """
    return origin == u'OSLO'

def origin_oman(origin):
    """\

    """
    return origin == u'MUSCAT'

def origin_pakistan(origin):
    """\

    """
    return origin in (u'KARACHI', u'LAHORE', u'PESHAWAR', u'ISLAMABAD')

def origin_palau(origin):
    """\

    """
    return origin == u'KOROR'

def origin_panama(origin):
    """\

    """
    return origin == u'PANAMA'

def origin_papua_new_guinea(origin):
    """\

    """
    return origin == u'PORTMORESBY'

def origin_paraguay(origin):
    """\

    """
    return origin == u'ASUNCION'

def origin_peru(origin):
    """\

    """
    return origin == u'LIMA'

def origin_philippines(origin):
    """\

    """
    return origin == u'MANILA'

def origin_poland(origin):
    """\

    """
    return origin in (u'KRAKOW', u'WARSAW')

def origin_portugal(origin):
    """\

    """
    return origin in (u'LISBON', u'PONTADELGADA')

def origin_qatar(origin):
    """\

    """
    return origin == u'QATAR'

def origin_republic_congo(origin):
    """\

    """
    return origin == u'BRAZZAVILLE'

def origin_romania(origin):
    """\

    """
    return origin == u'BUCHAREST'

def origin_russia(origin):
    """\

    """
    return origin in (u'MOSCOW', u'STPETERSBURG', u'VLADIVOSTOK', u'YEKATERINBURG')

def origin_rwanda(origin):
    """\

    """
    return origin == u'KIGALI'

def origin_samoa(origin):
    """\

    """
    return origin == u'APIA'

def origin_saudi_arabia(origin):
    """\

    """
    return origin in (u'DHAHRAN', u'JEDDAH', u'RIYADH')

def origin_senegal(origin):
    """\

    """
    return origin == u'DAKAR'

def origin_serbia(origin):
    """\

    """
    return origin == u'BELGRADE'

def origin_sierra_leone(origin):
    """\

    """
    return origin == u'FREETOWN'

def origin_singapore(origin):
    """\

    """
    return origin == u'SINGAPORE'

def origin_slovakia(origin):
    """\

    """
    return origin == u'BRATISLAVA'

def origin_slovenia(origin):
    """\

    """
    return origin == u'LJUBLJANA'

def origin_somalia(origin):
    """\

    """
    return origin == u'MOGADISHU'

def origin_south_africa(origin):
    """\

    """
    return origin in (u'CAPETOWN', u'DURBAN', u'JOHANNESBURG', u'PRETORIA')

def origin_south_korea(origin):
    """\

    """
    return origin == u'SEOUL'

def origin_spain(origin):
    """\

    """
    return origin in (u'MADRID', u'BARCELONA')

def origin_sri_lanka(origin):
    """\

    """
    return origin == u'COLOMBO'

def origin_sudan(origin):
    """\

    """
    return origin == u'KHARTOUM'

def origin_suriname(origin):
    """\

    """
    return origin == u'PARAMARIBO'

def origin_swaziland(origin):
    """\

    """
    return origin == u'MBABANE'

def origin_sweden(origin):
    """\

    """
    return origin == u'STOCKHOLM'

def origin_switzerland(origin):
    """\

    """
    return origin == u'BERN'

def origin_syria(origin):
    """\

    """
    return origin == u'DAMASCUS'

def origin_taiwan(origin):
    """\

    """
    return u'TAIPEI' in origin

def origin_tajikistan(origin):
    """\

    """
    return origin == u'DUSHANBE'

def origin_tanzania(origin):
    """\

    """
    return origin == u'DARESSALAAM'

def origin_thailand(origin):
    """\

    """
    return origin in (u'BANGKOK', u'CHIANGMAI')

def origin_togo(origin):
    """\

    """
    return origin == u'LOME'

def origin_trinidad_and_tobago(origin):
    """\

    """
    return origin == u'PORTOFSPAIN'

def origin_tunisia(origin):
    """\

    """
    return origin == u'TUNIS'

def origin_turkey(origin):
    """\

    """
    return origin in (u'ADANA', u'ANKARA', u'ISTANBUL', u'IZMIR')

def origin_turkmenistan(origin):
    """\

    """
    return origin == u'ASHGABAT'

def origin_uganda(origin):
    """\

    """
    return origin == u'KAMPALA'

def origin_ukraine(origin):
    """\

    """
    return origin in (u'KYIV', u'KIEV')

def origin_united_arab_emirates(origin):
    """\

    """
    return origin in (u'ABUDHABI', u'DUBAI')

def origin_united_kingdom(origin):
    """\

    """
    return origin == u'LONDON'

def origin_uruguay(origin):
    """\

    """
    return origin == u'MONTEVIDEO'

def origin_uzbekistan(origin):
    """\

    """
    return origin == u'TASHKENT'

def origin_vatican(origin):
    """\

    """
    return origin == u'VATICAN'

def origin_venezuela(origin):
    """\

    """
    return origin == u'CARACAS'

def origin_vietnam(origin):
    """\

    """
    return origin in (u'HANOI', u'HOCHIMINHCITY')

def origin_yemen(origin):
    """\

    """
    return origin == u'SANAA'

def origin_zambia(origin):
    """\

    """
    return origin == u'LUSAKA'

def origin_zimbabwe(origin):
    """\

    """
    return origin == u'HARARE'


if __name__ == '__main__':
    import doctest
    doctest.testmod()

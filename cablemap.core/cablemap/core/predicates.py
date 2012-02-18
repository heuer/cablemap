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

    `origin`
        The origin to check.
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

    Holds true for the following countries:
        * Algeria
        * Egypt
        * Libya
        * Morocco
        * Sudan
        * Tunisia

    `origin`
        The origin to check.
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

    `origin`
        The origin to check.
    """
    return origin_benin(origin) or origin_burkina_faso(origin) or origin_cape_verde(origin) \
           or origin_cote_divoire(origin) or origin_gambia(origin) or origin_ghana(origin) \
           or origin_guinea(origin) or origin_liberia(origin) or origin_mali(origin) \
           or origin_mauritania(origin) or origin_niger(origin) or origin_nigeria(origin) \
           or origin_senegal(origin) or origin_sierra_leone(origin) or origin_togo(origin)

def origin_central_asia(origin):
    """\
    Returns if the origin is located in Central Asia.

    Holds true for the following countries:
        * Afghanistan
        * Kazakhstan
        * Kyrgyzstan
        * Tajikistan
        * Turkmenistan
        * Uzbekistan

    `origin`
        The origin to check.
    """
    return origin_afghanistan(origin) or origin_kazakhstan(origin) or origin_kyrgyzstan(origin) \
           or origin_tajikistan(origin) or origin_turkmenistan(origin) or origin_uzbekistan(origin)

def origin_east_asia(origin):
    """\
    Returns if the origin is located in East Asia

    Holds true for the following countries:
        * China
        * Japan
        * Mongolia
        * South Korea
        * Taiwan

    `origin`
        The origin to check.
    """
    return origin_china(origin) or origin_japan(origin) or origin_mongolia(origin) \
           or origin_south_korea(origin) or origin_taiwan(origin)

def origin_west_asia(origin):
    """\
    Returns if the origin is located in Western Asia.

    Holds true for the following countries:
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

    `origin`
        The origin to check.
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

    `origin`
        The origin to check.
    """
    return origin == u'PARTO'

def origin_afghanistan(origin):
    """\
    Returns if the origin is Afghanistan.

    `origin`
        The origin to check.
    """
    return origin == u'KABUL'

def origin_albania(origin):
    """\
    Returns if the origin is Albania.

    `origin`
        The origin to check.
    """
    return origin == u'TIRANA'

def origin_algeria(origin):
    """\
    Returns if the origiin is Algeria.

    `origin`
        The origin to check.
    """
    return origin == u'ALGIERS'

def origin_angola(origin):
    """\
    Returns if the origin is Angola.

    `origin`
        The origin to check.
    """
    return origin == u'LUANDA'

def origin_argentinia(origin):
    """\
    Returns if the origin is Argentinia.

    `origin`
        The origin to check.
    """
    return origin == u'BUENOSAIRES'

def origin_armenia(origin):
    """\
    Returns if the origin is Armenia.

    `origin`
        The origin to check.
    """
    return origin == u'YEREVAN'

def origin_australia(origin):
    """\
    Returns if the origin is Australia.

    `origin`
        The origin to check.
    """
    return origin in u'MELBOURNE', u'SYDNEY', u'PERTH', u'CANBERRA'

def origin_austria(origin):
    """\

    """
    # Matches U.S. Mission to Vienna and Vienna
    return u'VIENNA' in origin

def origin_azerbaijan(origin):
    """\
    Returns if the origin is Azerbaijan.

    `origin`
        The origin to check.
    """
    return origin == u'BAKU'

def origin_bahamas(origin):
    """\
    """
    return origin == u'NASSAU'

def origin_bahrain(origin):
    """\
    Returns if the origin is Bahrain.

    `origin`
        The origin to check.
    """
    return origin == u'MANAMA'

def origin_bangladesh(origin):
    """\
    Returns if the origin is Bangladesh.

    `origin`
        The origin to check.
    """
    return origin == u'DHAKA'

def origin_barbados(origin):
    """\
    Returns if the origin is Barbados.

    `origin`
        The origin to check.
    """
    return origin == u'BRIDGETOWN',

def origin_belarus(origin):
    """\
    Returns if the origin is Belarus.

    `origin`
        The origin to check.
    """
    return origin == u'MINSK'

def origin_belgium(origin):
    """\

    """
    # Matches U.S. Mission to EU, Brussels and Brussels
    return u'BRUSSELS' in origin

def origin_belize(origin):
    """\
    Returns if the origin is Belize.

    `origin`
        The origin to check.
    """
    return origin == u'BELMOPAN'

def origin_benin(origin):
    """\
    Returns if the origin is Benin.

    `origin`
        The origin to check.
    """
    return origin == u'COTONOU'

def origin_bermuda(origin):
    """\
    Returns if the origin is Bermuda.

    `origin`
        The origin to check.
    """
    return origin == u'HAMILTON'

def origin_bolivia(origin):
    """\
    Returns if the origin is Bolivia.

    `origin`
        The origin to check.
    """
    return origin == u'LAPAZ'

def origin_bosnia_and_herzegovina(origin):
    """\
    Returns if the origin is Bosnia and Herzegovina.

    `origin`
        The origin to check.
    """
    return origin == u'SARAJEVO'

def origin_botswana(origin):
    """\
    Returns if the origin is Botswana.

    `origin`
        The origin to check.
    """
    return origin == u'GABORONE'

def origin_brazil(origin):
    """\
    Returns if the origin is Brazil.

    `origin`
        The origin to check.
    """
    return origin in (u'BRASILIA', u'SAOPAULO', u'RIODEJANEIRO', u'RECIFE')

def origin_brunei(origin):
    """\
    Returns if the origin is Brunei.

    `origin`
        The origin to check.
    """
    return origin == u'BANDARSERIBEGAWAN'

def origin_bulgaria(origin):
    """\
    Returns if the origin is Bulgaria.

    `origin`
        The origin to check.
    """
    return origin == u'SOFIA'

def origin_burkina_faso(origin):
    """\
    Returns if the origin is Burkina Faso.

    `origin`
        The origin to check.
    """
    return origin == u'OUAGADOUGOU'

def origin_burma(origin):
    """\
    Returns if the origin is Burma.

    `origin`
        The origin to check.
    """
    return origin == u'RANGOON'

def origin_burundi(origin):
    """\
    Returns if the origin is Burundi.

    `origin`
        The origin to check.
    """
    return origin == u'BUJUMBURA'

def origin_cambodia(origin):
    """\
    Returns if the origin is Cambodia.

    `origin`
        The origin to check.
    """
    return origin == u'PHNOMPENH'

def origin_cameroon(origin):
    """\
    Returns if the origin is Cameroon.

    `origin`
        The origin to check.
    """
    return origin == u'YAOUNDE'

def origin_canada(origin):
    """\
    Returns if the origin is Canada.

    `origin`
        The origin to check.
    """
    return origin in (u'CALGARY', u'HALIFAX', u'MONTREAL', u'QUEBEC', u'OTTAWA', u'TORONTO', u'VANCOUVER')

def origin_cape_verde(origin):
    """\
    Returns if the origin is Cape Verde.

    `origin`
        The origin to check.
    """
    return origin == u'PRAIA'

def origin_central_african_republic(origin):
    """\
    Returns if the origin is Central African Republic.

    `origin`
        The origin to check.
    """
    return origin == u'BANGUI'

def origin_chad(origin):
    """\
    Returns if the origin is Chad.

    `origin`
        The origin to check.
    """
    return origin == u'NDJAMENA'

def origin_chile(origin):
    """\
    Returns if the origin is Chile.

    `origin`
        The origin to check.
    """
    return origin == u'SANTIAGO'

def origin_china(origin):
    """\
    Returns if the origin is China.

    `origin`
        The origin to check.
    """
    return origin in (u'BEIJING', u'CHENGDU', u'GUANGZHOU', u'HONGKONG', u'SHANGHAI', u'SHENYANG')

def origin_colombia(origin):
    """\
    Returns if the origin is Colombia.

    `origin`
        The origin to check.
    """
    return origin == u'BOGOTA'

def origin_costa_rica(origin):
    """\
    Returns if the origin is Costa Rica.

    `origin`
        The origin to check.
    """
    return origin == u'SANJOSE'

def origin_cote_divoire(origin):
    """\
    Returns if the origin is Cote d'Ivoire.

    `origin`
        The origin to check.
    """
    return origin == u'ABIDJAN'

def origin_croatia(origin):
    """\
    Returns if the origin is Croatia.

    `origin`
        The origin to check.
    """
    return origin == u'ZAGREB'

def origin_cuba(origin):
    """\
    Returns if the origin is Cuba.

    `origin`
        The origin to check.
    """
    return origin == u'HAVANA'

def origin_curacao(origin):
    """\
    Returns if the origin is Curacao.

    `origin`
        The origin to check.
    """
    return origin == u'CURACA'

def origin_cyprus(origin):
    """\
    Returns if the origin is Cyprus.

    `origin`
        The origin to check.
    """
    return origin == u'NICOSIA'

def origin_czech(origin):
    """\
    Returns if the origin is Czech.

    `origin`
        The origin to check.
    """
    return origin == u'PRAGUE'

def origin_democratic_republic_congo(origin):
    """\
    Returns if the origin is Democratic Republic Congo.

    `origin`
        The origin to check.
    """
    return origin == u'KINSHASA'

def origin_denmark(origin):
    """\
    Returns if the origin is Denmark.

    `origin`
        The origin to check.
    """
    return origin == u'COPENHAGEN'

def origin_djibouti(origin):
    """\
    Returns if the origin is Djibouti.

    `origin`
        The origin to check.
    """
    return origin == u'DJIBOUTI'

def origin_dominican_republic(origin):
    """\
    Returns if the origin is Dominican Republic.

    `origin`
        The origin to check.
    """
    return origin == u'SANTODOMINGO'

def origin_east_timor(origin):
    """\
    Returns if the origin is East Timor.

    `origin`
        The origin to check.
    """
    return origin == u'DILI'

def origin_ecuador(origin):
    """\
    Returns if the origin is Ecuador.

    `origin`
        The origin to check.
    """
    return origin == u'QUITO'

def origin_egypt(origin):
    """\
    Returns if the origin is Egypt.

    `origin`
        The origin to check.
    """
    return origin in (u'CAIRO', u'ALEXANDRIA')

def origin_el_salvador(origin):
    """\
    Returns if the origin is El Salvador.

    `origin`
        The origin to check.
    """
    return origin == u'SANSALVADOR'

def origin_equatorial_guinea(origin):
    """\
    Returns if the origin is Equatorial Guinea.

    `origin`
        The origin to check.
    """
    return origin == u'MALABO'

def origin_eritrea(origin):
    """\
    Returns if the origin is Eritrea.

    `origin`
        The origin to check.
    """
    return origin == u'ASMARA'

def origin_estonia(origin):
    """\
    Returns if the origin is Estonia.

    `origin`
        The origin to check.
    """
    return origin == u'TALLINN'

def origin_ethiopia(origin):
    """\
    Returns if the origin is Ethiopia.

    `origin`
        The origin to check.
    """
    return origin == u'ADDISABABA'

def origin_micronesia(origin):
    """\
    Returns if the origin is Micronesia.

    `origin`
        The origin to check.
    """
    return origin == u'KOLONIA'

def origin_fiji(origin):
    """\
    Returns if the origin is Fiji.

    `origin`
        The origin to check.
    """
    return origin == u'SUVA'

def origin_finland(origin):
    """\
    Returns if the origin is Finland.

    `origin`
        The origin to check.
    """
    return origin == u'HELSINKI'

def origin_france(origin):
    """\
    Returns if the origin is France.

    `origin`
        The origin to check.
    """
    return origin in (u'MARSEILLE', u'PARIS', u'STRASBOURG')

def origin_gabon(origin):
    """\
    Returns if the origin is Gabon.

    `origin`
        The origin to check.
    """
    return origin == u'LIBREVILLE'

def origin_gambia(origin):
    """\
    Returns if the origin is Gambia.

    `origin`
        The origin to check.
    """
    return origin == u'BANJUL'

def origin_georgia(origin):
    """\
    Returns if the origin is Georgia.

    `origin`
        The origin to check.
    """
    return origin == u'TBILISI'

def origin_germany(origin):
    """\
    Returns if the origin is Germany.

    `origin`
        The origin to check.
    """
    return origin in (u'BONN', u'BERLIN', u'DUSSELDORF', u'FRANKFURT', u'HAMBURG', u'LEIPZIG', u'MUNICH')

def origin_ghana(origin):
    """\
    Returns if the origin is Ghana.

    `origin`
        The origin to check.
    """
    return origin == u'ACCRA'

def origin_greece(origin):
    """\
    Returns if the origin is Greece.

    `origin`
        The origin to check.
    """
    return origin in (u'ATHENS', u'THESSALONIKI')

def origin_grenada(origin):
    """\
    Returns if the origin is Grenada.

    `origin`
        The origin to check.
    """
    return origin == u'BRIDGETOWN'

def origin_guatemala(origin):
    """\
    Returns if the origin is Guatemala.

    `origin`
        The origin to check.
    """
    return origin == u'GUATEMALA'

def origin_guinea(origin):
    """\
    Returns if the origin is Guinea.

    `origin`
        The origin to check.
    """
    return origin == u'CONAKRY'

def origin_guyana(origin):
    """\
    Returns if the origin is Guyana.

    `origin`
        The origin to check.
    """
    return origin == u'GEORGETOWN'

def origin_haiti(origin):
    """\
    Returns if the origin is Haiti.

    `origin`
        The origin to check.
    """
    return origin == u'PORTAUPRINCE'

def origin_honduras(origin):
    """\
    Returns if the origin is Honduras.

    `origin`
        The origin to check.
    """
    return origin == u'TEGUCIGALPA'

def origin_hungary(origin):
    """\
    Returns if the origin is Hungary.

    `origin`
        The origin to check.
    """
    return origin == u'BUDAPEST'

def origin_iceland(origin):
    """\
    Returns if the origin is Iceland.

    `origin`
        The origin to check.
    """
    return origin == u'REYKJAVIK'

def origin_india(origin):
    """\
    Returns if the origin is India.

    `origin`
        The origin to check.
    """
    return origin in (u'CHENNAI', u'KOLKATA', u'MUMBAI', u'NEWDELHI')

def origin_indonesia(origin):
    """\
    Returns if the origin is Indonesia.

    `origin`
        The origin to check.
    """
    return origin in (u'JAKARTA', u'SURABAYA')

def origin_iran(origin):
    """\
    Returns if the origin is Iran.

    `origin`
        The origin to check.
    """
    return origin in (u'TEHRAN', u'RPODUBAI')

def origin_iraq(origin):
    """\
    Returns if the origin is Iraq.

    `origin`
        The origin to check.
    """
    return origin == u'BAGHDAD' \
           or u'BASRAH' in origin \
           or u'HILLAH' in origin \
           or u'KIRKUK' in origin \
           or u'MOSUL' in origin

def origin_ireland(origin):
    """\
    Returns if the origin is Ireland.

    `origin`
        The origin to check.
    """
    return origin == u'DUBLIN'

def origin_israel(origin):
    """\
    Returns if the origin is Israel.

    `origin`
        The origin to check.
    """
    return origin in (u'JERUSALEM', u'TELAVIV')

def origin_italy(origin):
    """\
    Returns if the origin is Italy.

    `origin`
        The origin to check.
    """
    return origin in (u'FLORENCE', u'MILAN', u'NAPLES') or u'ROME' in origin

def origin_jamaica(origin):
    """\
    Returns if the origin is Jamaica.

    `origin`
        The origin to check.
    """
    return origin == u'KINGSTON'

def origin_japan(origin):
    """\
    Returns if the origin is Japan.

    `origin`
        The origin to check.
    """
    return origin in (u'FUKUOKA', u'NAGOYA', u'NAHA', u'OSAKAKOBE', u'SAPPORO', u'TOKYO')

def origin_jordan(origin):
    """\
    Returns if the origin is Jordan.

    `origin`
        The origin to check.
    """
    return origin == u'AMMAN'

def origin_kazakhstan(origin):
    """\
    Returns if the origin is Kazakhstan.

    `origin`
        The origin to check.
    """
    return origin in (u'ASTANA', u'ALMATY')

def origin_kenya(origin):
    """\
    Returns if the origin is Kenya.

    `origin`
        The origin to check.
    """
    return origin == u'NAIROBI'

def origin_kosovo(origin):
    """\
    Returns if the origin is Kosovo.

    `origin`
        The origin to check.
    """
    return origin == u'PRISTINA'

def origin_kuwait(origin):
    """\
    Returns if the origin is Kuwait.

    `origin`
        The origin to check.
    """
    return origin == u'KUWAIT'

def origin_kyrgyzstan(origin):
    """\
    Returns if the origin is Kyrgyzstan.

    `origin`
        The origin to check.
    """
    return origin == u'BISHKEK'

def origin_laos(origin):
    """\
    Returns if the origin is Laos.

    `origin`
        The origin to check.
    """
    return origin == u'VIENTIANE'

def origin_latvia(origin):
    """\
    Returns if the origin is Latvia.

    `origin`
        The origin to check.
    """
    return origin == u'RIGA'

def origin_lebanon(origin):
    """\
    Returns if the origin is Lebanon.

    `origin`
        The origin to check.
    """
    return origin == u'BEIRUT'

def origin_lesotho(origin):
    """\
    Returns if the origin is Lesotho.

    `origin`
        The origin to check.
    """
    return origin == u'MASERU'

def origin_liberia(origin):
    """\
    Returns if the origin is Liberia.

    `origin`
        The origin to check.
    """
    return origin == u'MONROVIA'

def origin_libya(origin):
    """\
    Returns if the origin is Libya.

    `origin`
        The origin to check.
    """
    return origin == u'TRIPOLI'

def origin_lithuania(origin):
    """\
    Returns if the origin is Lithuania.

    `origin`
        The origin to check.
    """
    return origin == u'VILNIUS'

def origin_luxembourg(origin):
    """\
    Returns if the origin is Luxembourg.

    `origin`
        The origin to check.
    """
    return origin == u'LUXEMBOURG'

def origin_macedonia(origin):
    """\
    Returns if the origin is Macedonia.

    `origin`
        The origin to check.
    """
    return origin == u'SKOPJE'

def origin_madagascar(origin):
    """\
    Returns if the origin is Madagascar.

    `origin`
        The origin to check.
    """
    return origin == u'ANTANANARIVO'

def origin_majuro(origin):
    """\
    Returns if the origin is Majuro.

    `origin`
        The origin to check.
    """
    return origin == u'MAJURO'

def origin_malawi(origin):
    """\
    Returns if the origin is Malawi.

    `origin`
        The origin to check.
    """
    return origin == u'LILONGWE'

def origin_malaysia(origin):
    """\
    Returns if the origin is Malaysia.

    `origin`
        The origin to check.
    """
    return origin == u'KUALALUMPUR'

def origin_mali(origin):
    """\
    Returns if the origin is Mali.

    `origin`
        The origin to check.
    """
    return origin == u'BAMAKO'

def origin_malta(origin):
    """\
    Returns if the origin is Malta.

    `origin`
        The origin to check.
    """
    return origin == u'VALLETTA'

def origin_mauritania(origin):
    """\
    Returns if the origin is Mauritania.

    `origin`
        The origin to check.
    """
    return origin == u'NOUAKCHOTT'

def origin_mauritius(origin):
    """\
    Returns if the origin is Mauritius.

    `origin`
        The origin to check.
    """
    return origin == u'PORTLOUIS'

def origin_mexico(origin):
    """\
    Returns if the origin is Mexico.

    `origin`
        The origin to check.
    """
    return origin in (u'CIUDADJUAREZ', u'GUADALAJARA', u'HERMOSILLO',
                      u'MATAMOROS', u'MERIDA', u'MEXICO', u'MONTERREY', u'NOGALES',
                      u'NUEVOLAREDO', u'TIJUANA')

def origin_moldova(origin):
    """\
    Returns if the origin is Moldova.

    `origin`
        The origin to check.
    """
    return origin == u'CHISINAU'

def origin_mongolia(origin):
    """\
    Returns if the origin is Mongolia.

    `origin`
        The origin to check.
    """
    return origin == u'ULAANBAATAR'

def origin_montenegro(origin):
    """\
    Returns if the origin is Montenegro.

    `origin`
        The origin to check.
    """
    return origin == u'PODGORICA'

def origin_morocco(origin):
    """\
    Returns if the origin is Morocco.

    `origin`
        The origin to check.
    """
    return origin in (u'CASABLANCA', u'RABAT')

def origin_mozambique(origin):
    """\
    Returns if the origin is Mozambique.

    `origin`
        The origin to check.
    """
    return origin == u'MAPUTO'

def origin_namibia(origin):
    """\
    Returns if the origin is Namibia.

    `origin`
        The origin to check.
    """
    return origin == u'WINDHOEK'

def origin_nepal(origin):
    """\
    Returns if the origin is Nepal.

    `origin`
        The origin to check.
    """
    return origin == u'KATHMANDU'

def origin_netherlands(origin):
    """\
    Returns if the origin is Netherlands.

    `origin`
        The origin to check.
    """
    return origin in (u'AMSTERDAM', u'THEHAGUE')

def origin_new_zealand(origin):
    """\
    Returns if the origin is New Zealand.

    `origin`
        The origin to check.
    """
    return origin in (u'AUCKLAND', u'WELLINGTON')

def origin_nicaragua(origin):
    """\
    Returns if the origin is Nicaragua.

    `origin`
        The origin to check.
    """
    return origin == u'MANAGUA'

def origin_niger(origin):
    """\
    Returns if the origin is Niger.

    `origin`
        The origin to check.
    """
    return origin == u'NIAMEY'

def origin_nigeria(origin):
    """\
    Returns if the origin is Nigeria.

    `origin`
        The origin to check.
    """
    return origin in (u'ABUJA', u'KADUNA', u'LAGOS')

def origin_usnato(origin):
    """\
    Returns if the origin is US NATO.

    `origin`
        The origin to check.
    """
    return origin == u'USNATO'

def origin_northern_ireland(origin):
    """\
    Returns if the origin is Northern Ireland.

    `origin`
        The origin to check.
    """
    return origin == u'BELFAST'

def origin_norway(origin):
    """\
    Returns if the origin is Norway.

    `origin`
        The origin to check.
    """
    return origin == u'OSLO'

def origin_oman(origin):
    """\
    Returns if the origin is Oman.

    `origin`
        The origin to check.
    """
    return origin == u'MUSCAT'

def origin_pakistan(origin):
    """\
    Returns if the origin is Pakistan.

    `origin`
        The origin to check.
    """
    return origin in (u'KARACHI', u'LAHORE', u'PESHAWAR', u'ISLAMABAD')

def origin_palau(origin):
    """\
    Returns if the origin is Palau.

    `origin`
        The origin to check.
    """
    return origin == u'KOROR'

def origin_panama(origin):
    """\
    Returns if the origin is Panama.

    `origin`
        The origin to check.
    """
    return origin == u'PANAMA'

def origin_papua_new_guinea(origin):
    """\
    Returns if the origin is Papua New Guinea.

    `origin`
        The origin to check.
    """
    return origin == u'PORTMORESBY'

def origin_paraguay(origin):
    """\
    Returns if the origin is Paraguay.

    `origin`
        The origin to check.
    """
    return origin == u'ASUNCION'

def origin_peru(origin):
    """\
    Returns if the origin is Peru.

    `origin`
        The origin to check.
    """
    return origin == u'LIMA'

def origin_philippines(origin):
    """\
    Returns if the origin is Philippines.

    `origin`
        The origin to check.
    """
    return origin == u'MANILA'

def origin_poland(origin):
    """\
    Returns if the origin is Poland.

    `origin`
        The origin to check.
    """
    return origin in (u'KRAKOW', u'WARSAW')

def origin_portugal(origin):
    """\
    Returns if the origin is Portugal.

    `origin`
        The origin to check.
    """
    return origin in (u'LISBON', u'PONTADELGADA')

def origin_qatar(origin):
    """\
    Returns if the origin is Qatar.

    `origin`
        The origin to check.
    """
    return origin == u'QATAR'

def origin_republic_congo(origin):
    """\
    Returns if the origin is Republic Congo.

    `origin`
        The origin to check.
    """
    return origin == u'BRAZZAVILLE'

def origin_romania(origin):
    """\
    Returns if the origin is Romania.

    `origin`
        The origin to check.
    """
    return origin == u'BUCHAREST'

def origin_russia(origin):
    """\
    Returns if the origin is Russia.

    `origin`
        The origin to check.
    """
    return origin in (u'MOSCOW', u'STPETERSBURG', u'VLADIVOSTOK', u'YEKATERINBURG')

def origin_rwanda(origin):
    """\
    Returns if the origin is Rwanda.

    `origin`
        The origin to check.
    """
    return origin == u'KIGALI'

def origin_samoa(origin):
    """\
    Returns if the origin is Samoa.

    `origin`
        The origin to check.
    """
    return origin == u'APIA'

def origin_saudi_arabia(origin):
    """\
    Returns if the origin is Saudi Arabia.

    `origin`
        The origin to check.
    """
    return origin in (u'DHAHRAN', u'JEDDAH', u'RIYADH')

def origin_senegal(origin):
    """\
    Returns if the origin is Senegal.

    `origin`
        The origin to check.
    """
    return origin == u'DAKAR'

def origin_serbia(origin):
    """\
    Returns if the origin is Serbia.

    `origin`
        The origin to check.
    """
    return origin == u'BELGRADE'

def origin_sierra_leone(origin):
    """\
    Returns if the origin is Sierra Leone.

    `origin`
        The origin to check.
    """
    return origin == u'FREETOWN'

def origin_singapore(origin):
    """\
    Returns if the origin is Singapore.

    `origin`
        The origin to check.
    """
    return origin == u'SINGAPORE'

def origin_slovakia(origin):
    """\
    Returns if the origin is Slovakia.

    `origin`
        The origin to check.
    """
    return origin == u'BRATISLAVA'

def origin_slovenia(origin):
    """\
    Returns if the origin is Slovenia.

    `origin`
        The origin to check.
    """
    return origin == u'LJUBLJANA'

def origin_somalia(origin):
    """\
    Returns if the origin is Somalia.

    `origin`
        The origin to check.
    """
    return origin == u'MOGADISHU'

def origin_south_africa(origin):
    """\
    Returns if the origin is South Africa.

    `origin`
        The origin to check.
    """
    return origin in (u'CAPETOWN', u'DURBAN', u'JOHANNESBURG', u'PRETORIA')

def origin_south_korea(origin):
    """\
    Returns if the origin is South Korea.

    `origin`
        The origin to check.
    """
    return origin == u'SEOUL'

def origin_spain(origin):
    """\
    Returns if the origin is Spain.

    `origin`
        The origin to check.
    """
    return origin in (u'MADRID', u'BARCELONA')

def origin_sri_lanka(origin):
    """\
    Returns if the origin is Sri Lanka.

    `origin`
        The origin to check.
    """
    return origin == u'COLOMBO'

def origin_sudan(origin):
    """\
    Returns if the origin is Sudan.

    `origin`
        The origin to check.
    """
    return origin == u'KHARTOUM'

def origin_suriname(origin):
    """\
    Returns if the origin is Suriname.

    `origin`
        The origin to check.
    """
    return origin == u'PARAMARIBO'

def origin_swaziland(origin):
    """\
    Returns if the origin is Swaziland.

    `origin`
        The origin to check.
    """
    return origin == u'MBABANE'

def origin_sweden(origin):
    """\
    Returns if the origin is Sweden.

    `origin`
        The origin to check.
    """
    return origin == u'STOCKHOLM'

def origin_switzerland(origin):
    """\
    Returns if the origin is Switzerland.

    `origin`
        The origin to check.
    """
    return origin == u'BERN'

def origin_syria(origin):
    """\
    Returns if the origin is Syria.

    `origin`
        The origin to check.
    """
    return origin == u'DAMASCUS'

def origin_taiwan(origin):
    """\
    Returns if the origin is Taiwan.

    `origin`
        The origin to check.
    """
    return u'TAIPEI' in origin

def origin_tajikistan(origin):
    """\
    Returns if the origin is Tajikistan.

    `origin`
        The origin to check.
    """
    return origin == u'DUSHANBE'

def origin_tanzania(origin):
    """\
    Returns if the origin is Tanzania.

    `origin`
        The origin to check.
    """
    return origin == u'DARESSALAAM'

def origin_thailand(origin):
    """\
    Returns if the origin is Thailand.

    `origin`
        The origin to check.
    """
    return origin in (u'BANGKOK', u'CHIANGMAI')

def origin_togo(origin):
    """\
    Returns if the origin is Togo.

    `origin`
        The origin to check.
    """
    return origin == u'LOME'

def origin_trinidad_and_tobago(origin):
    """\
    Returns if the origin is Trinidad and Tobago.

    `origin`
        The origin to check.
    """
    return origin == u'PORTOFSPAIN'

def origin_tunisia(origin):
    """\
    Returns if the origin is Tunisia.

    `origin`
        The origin to check.
    """
    return origin == u'TUNIS'

def origin_turkey(origin):
    """\
    Returns if the origin is Turkey.

    `origin`
        The origin to check.
    """
    return origin in (u'ADANA', u'ANKARA', u'ISTANBUL', u'IZMIR')

def origin_turkmenistan(origin):
    """\
    Returns if the origin is Turkmenistan.

    `origin`
        The origin to check.
    """
    return origin == u'ASHGABAT'

def origin_uganda(origin):
    """\
    Returns if the origin is Uganda.

    `origin`
        The origin to check.
    """
    return origin == u'KAMPALA'

def origin_ukraine(origin):
    """\
    Returns if the origin is Ukraine.

    `origin`
        The origin to check.
    """
    return origin in (u'KYIV', u'KIEV')

def origin_united_arab_emirates(origin):
    """\
    Returns if the origin is United Arab Emirates.

    `origin`
        The origin to check.
    """
    return origin in (u'ABUDHABI', u'DUBAI')

def origin_united_kingdom(origin):
    """\
    Returns if the origin is United Kingdom.

    `origin`
        The origin to check.
    """
    return origin == u'LONDON'

def origin_uruguay(origin):
    """\
    Returns if the origin is Uruguay.

    `origin`
        The origin to check.
    """
    return origin == u'MONTEVIDEO'

def origin_uzbekistan(origin):
    """\
    Returns if the origin is Uzbekistan.

    `origin`
        The origin to check.
    """
    return origin == u'TASHKENT'

def origin_vatican(origin):
    """\
    Returns if the origin is Vatican.

    `origin`
        The origin to check.
    """
    return origin == u'VATICAN'

def origin_venezuela(origin):
    """\
    Returns if the origin is Venezuela.

    `origin`
        The origin to check.
    """
    return origin == u'CARACAS'

def origin_vietnam(origin):
    """\
    Returns if the origin is Vietnam.

    `origin`
        The origin to check.
    """
    return origin in (u'HANOI', u'HOCHIMINHCITY')

def origin_yemen(origin):
    """\
    Returns if the origin is Yemen.

    `origin`
        The origin to check.
    """
    return origin == u'SANAA'

def origin_zambia(origin):
    """\
    Returns if the origin is Zambia.

    `origin`
        The origin to check.
    """
    return origin == u'LUSAKA'

def origin_zimbabwe(origin):
    """\
    Returns if the origin is Zimbabwe.

    `origin`
        The origin to check.
    """
    return origin == u'HARARE'


if __name__ == '__main__':
    import doctest
    doctest.testmod()

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
Canonicalization utility functions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import absolute_import
import re
from . constants import MALFORMED_CABLE_IDS, INVALID_CABLE_IDS

_STATION_C14N = {
    u'AUBJA': u'ABUJA',
    u'RANGON': u'RANGOON',
    u'TEGUC': u'TEGUCIGALPA',
    u'TEGUZ': u'TEGUCIGALPA',
    u'KATHAMNDU': u'KATHMANDU',
    u'KATHMANUD': u'KATHMANDU',
    u'NARIOBI': u'NAIROBI',
    u'ABDIDJAN': u'ABIDJAN',
    u'JERSUALEM': u'JERUSALEM',
    u'JERUSALM': u'JERUSALEM',
    u'KINSHSA': u'KINSHASA',
    u'ABIDJDAN': u'ABIDJAN',
    u'DUESSELDORF': u'DUSSELDORF',
    u'JAK': u'JAKARTA',
    u'PETERSBURG': u'STPETERSBURG',
    u'TBLISI': u'TBILISI',
    u'KHARTOUNM': u'KHARTOUM',
    u'KHARTOM': u'KHARTOUM',
    u'CALCUTT': u'CALCUTTA',
    u'CAL': u'CALCUTTA',
    u'DAM': u'DAMASCUS',
    u'ANTAN': u'ANTANANARIVO',
    u'TANA': u'ANTANANARIVO',
    u'ANTANANARI': u'ANTANANARIVO',
    u'ATENS': u'ATHENS',
    u'ASHGABT': u'ASHGABAT',
    u'LJBULJANA': u'LJUBLJANA',
    u'LJUBJLANA': u'LJUBLJANA',
    u'COTON0U': u'COTONOU',
    u'FREEETOWN': u'FREETOWN',
    u'ATLANTA': u'CDCATLANTAGA',
    u'ATLANGAGA': u'CDCATLANTAGA',
    u'ATLANTAGA': u'CDCATLANTAGA',
    u'CDCATLANTA': u'CDCATLANTAGA',
    u'CDC': u'CDCATLANTAGA',
    u'CDCATLANTAGAUSA': u'CDCATLANTAGA',
    u'ADDIS': u'ADDISABABA',
    u'ADDISABAB': u'ADDISABABA',
    u'ANK': u'ANKARA',
    u'ANAKRA': u'ANKARA',
    u'ANARA': u'ANKARA',
    u'USUNESCOPARISFR': u'UNESCOPARISFR',
    u'PARISFR': u'UNESCOPARISFR',
    u'UNVIE': u'UNVIEVIENNA',
    u'UNVIEVIEN': u'UNVIEVIENNA',
    u'UNVIENNA': 'UNVIEVIENNA',
    u'STAT': u'STATE',
    u'STAE': u'STATE',
    u'TATE': u'STATE',
    u'STATAE': u'STATE',
    u'SECSTATE': u'STATE',
    u'SECTSTATE': u'STATE',
    u'SECTATE': u'STATE',
    u'SECTATWASHDC': u'STATE',
    u'SECSTATEWASHDC': u'STATE',
    u'SECSATATE': u'STATE',
    u'SATTE': u'STATE',
    u'SECDEFWASH': u'SECDEF',
    u'WASHDC': u'STATE',
    u'USNATOANDUSNATO': u'USNATO', # 07REYKJAVIK85: REFS: Hodgson emails to Duguid/Pulaski/USNATO and USNATO 00184 
    u'RIO': u'RIODEJANEIRO',
    u'RIODEJAN': u'RIODEJANEIRO',
    u'RIODEJANIERO': u'RIODEJANEIRO',
    u'RIODEJANERIO': u'RIODEJANEIRO',
    u'PORT-OF-SPAIN': u'PORTOFSPAIN',
    u'POS': u'PORTOFSPAIN',
    u'PAUP': u'PORTAUPRINCE',
    u'PAP': u'PORTAUPRINCE',
    u'PORT-AU-PRINCE': u'PORTAUPRINCE',
    u'PORTA': u'PORTAUPRINCE',
    u'SANJSE': u'SANJOSE',
    u'PANANA': u'PANAMA',
    u'PANAM': u'PANAMA',
    u'MADRIDSP': u'MADRID',
    u'SURBAYA': u'SURABAYA',
    u'DAR': u'DARESSALAAM',
    u'BRUSSELSBE': u'BRUSSELS',
    u'USEUBRUSS': u'USEUBRUSSELS',
    u'USEU': u'USEUBRUSSELS',
    u'USUN': u'USUNNEWYORK',
    u'USUNNY': u'USUNNEWYORK',
    u'USUNNEYORK': u'USUNNEWYORK',
    u'NEWYORK': u'USUNNEWYORK',
    u'USUNNEW': u'USUNNEWYORK',
    u'HALIF': u'HALIFAX',
    u'KUALALUMP': u'KUALALUMPUR',
    u'KL': u'KUALALUMPUR',
    u'WELLINGOTN': u'WELLINGTON',
    u'WELLLINGTON': u'WELLINGTON',
    u'BKK': u'BANGKOK',
    u'KINSTON': u'KINGSTON',
    u'BISHTEK': u'BISHKEK',
    u'VAT': u'VATICAN',
    u'SAOPAUO': u'SAOPAULO',
    u'SAOPAUL': u'SAOPAULO',
    u'SCOPAULO': u'SAOPAULO',
    u'PAULO': u'SAOPAULO',
    u'SAOPULO': u'SAOPAULO',
    u'HAGUE': u'THEHAGUE',
    u'PHNOMPEN': u'PHNOMPENH',
    u'PHNOMPEHN': u'PHNOMPENH',
    u'MVD': u'MONTEVIDEO',
    u'TRIPOLII': u'TRIPOLI',
    u'BRASILA': u'BRASILIA',
    u'BRAZIL': u'BRASILIA',
    u'BRASIIA': u'BRASILIA',
    u'BRAZILIA': u'BRASILIA',
    u'BRASIILIA': u'BRASILIA',
    u'MEXICOCITY': u'MEXICO',
    u'MEX': u'MEXICO',
    u'BA': u'BUENOSAIRES',
    u'BUENSOAIRES': u'BUENOSAIRES',
    u'BUENOSAIREDS': u'BUENOSAIRES',
    u'BUENESAIRES': u'BUENOSAIRES',
    u'BUENOSAIRE': u'BUENOSAIRES',
    u'BSB': u'BANDARSERIBEGAWAN',
    u'BANDAR': u'BANDARSERIBEGAWAN',
    u'BANDARSERI': u'BANDARSERIBEGAWAN',
    u'USDA': u'USDAFAS',
    u'USDAFASWASHDC': u'USDAFAS',
    u'USDOCWASHDC': u'USDOC',
    u'DEPTOFCOMMERCE': u'USDOC',
    u'DOC': u'USDOC',
    u'USCUSTOMSA': u'USCBP',
    u'BEIJINJG': u'BEIJING',
    u'BEIJIG': u'BEIJING',
    u'BEIJINGCH': u'BEIJING',
    u'MANAUGUA': u'MANAGUA',
    u'MANAUGA': u'MANAGUA',
    u'TGG': u'TEGUCIGALPA',
    u'QUEBECCITY': u'QUEBEC',
    u'ASUN': u'ASUNCION',
    u'BASRA': u'BASRAH',
    u'TALLIN': u'TALLINN',
    u'SDO': u'SANTODOMINGO',
    u'SANTODOMINIGO': u'SANTODOMINGO',
    u'SD': u'SANTODOMINGO',
    u'0TTAWA': u'OTTAWA',
    u'SANTIAG': u'SANTIAGO',
    u'DELHI': u'NEWDELHI',
    u'NEWDEHLI': u'NEWDELHI',
    u'HCMC': u'HOCHIMINHCITY',
    u'HCM': u'HOCHIMINHCITY',
    u'HOCHIMINH': u'HOCHIMINHCITY',
    u'HOCHIMIN': u'HOCHIMINHCITY',
    u'TAIPEI': u'AITTAIPEI',
    u'HK': u'HONGKONG',
    u'MUMB': u'MUMBAI',
    u'DEPTOFJUST': u'USDOJ',
          
}

_C14N_PATTERN = re.compile(r'[0-9]{2}([0A-Z\-]+)[0-9]+')

def canonicalize_origin(origin):
    """\

    """
    origin = origin.replace(u'USMISSION', u'') \
                     .replace(u'AMEMBASSY', u'') \
                     .replace(u'EMBASSY', u'').strip()
    return _STATION_C14N.get(origin, origin)

def canonicalize_id(reference_id):
    """\
    Returns the canonicalized form of the provided reference_id.

    WikiLeaks provides some malformed cable identifiers. If the provided `reference_id`
    is not valid, this method returns the valid reference identifier equivalent.
    If the reference identifier is valid, the reference id is returned unchanged.

    Note: The returned canonicalized identifier may not be a valid WikiLeaks identifier
    anymore. In most cases the returned canonical form is identical to the WikiLeaks
    identifier, but for malformed cable identifiers like "09SECTION01OF03SANJOSE525"
    it is not (becomes "09SANJOSE525").

    `reference_id`
        The cable identifier to canonicalize
    """
    rid = MALFORMED_CABLE_IDS.get(reference_id, None) or INVALID_CABLE_IDS.get(reference_id, None)
    if rid:
        return rid
    m = _C14N_PATTERN.match(reference_id)
    if m:
        origin = m.group(1)
        return reference_id.replace(origin, canonicalize_origin(origin))
    return reference_id

_SIGNER_C14N = {
    u'ADDELTON': u'ADDLETON',
    u'ALLGEIR': u'ALLGEIER',
    u'BURGUARDT': u'BURGHARDT',
    u'BURHGARDT': u'BURGHARDT',
    u'AEASTHAM': u'EASTHAM',
    u'ZUNIA-BROWN': u'ZUNIGA-BROWN',
    u'RICCIARONDE': u'RICCIARDONE',
    u'RICCIARDNE': u'RICCIARDONE',
    u'RICCIARDON': u'RICCIARDONE',
    u'RICCARDONE': u'RICCIARDONE',
    u'RANNENBERGER': u'RANNEBERGER',
    u'DERSQ': u'DERSE',
    u'YOVANOVICTCH': u'YOVANOVITCH',
    u'YAVANOVITCH': u'YOVANOVITCH',
    u'YAMAMOT': u'YAMAMOTO',
    u'YAMAMATO': u'YAMAMOTO',
    u'ROONEYF': u'ROONEY',
    u'DGTEITELBAUM': u'TEITELBAUM',
    u'FOLMSBEEPA': u'FOLMSBEE',
    u'MCCORMIC': u'MCCORMICK',
    u'MCCOMICK': u'MCCORMICK',
    u'WAR': u'WARE',
    u'SCOBY': u'SCOBEY',
    u'SCBEY': u'SCOBEY',
    u'SOBEY': u'SCOBEY',
    u'GUTMQ': u'GUTMAN',
    u'SULLVIAN': u'SULLIVAN',
    u'JSMITH': u'SMITH',
    u'STAPELTON': u'STAPLETON',
    u'ERNANDEZ': u'FERNANDEZ',
    u'FENRNANDEZ': u'FERNANDEZ',
    u'FERNANDEJ': u'FERNANDEZ',
    u'FREELEY': u'FEELEY',
    u'JEWEL': u'JEWELL',
    u'DANILOVIH': u'DANILOVICH',
    u'RWANG': u'WANG',
    u'SYOUNG': u'YOUNG',
    u'SHLICHER': u'SCHLICHER',
    u'BERYLE': u'BEYRLE',
    u'BYERLE': u'BEYRLE',
    u'CULBERSTON': u'CULBERTSON',
    u'MICHALK': u'MICHALAK',
    u'GITENSTIEN': u'GITENSTEIN',
    u'TUTTTLE': u'TUTTLE',
    u'WHITEY': u'WHITNEY',
    u'CAINE': u'CAIN',
    u'EIKENBERRRY': u'EIKENBERRY',
    u'EIKENBERY': u'EIKENBERRY',
    u'KHALILZHAD': u'KHALILZAD',
    u'WMONROE': u'MONROE',
    u'WILKENS': u'WILKINS',
    u'WILKINDS': u'WILKINS',
    u'GIRARD-DICRLO': u'GIRARD-DICARLO',
    u'FRRAR': u'FARRAR',
    u'RJONES': u'JONES',
    u'OUISMAN': u'OURISMAN',
    u'URISMAN': u'OURISMAN',
    u'MOOR': u'MOORE',
    u'ROL': u'KROL',
    u'GAREVELINK': u'GARVELINK',
    u'GAVELINK': u'GARVELINK',
    u'MEESE': u'MEECE',
    u'SCHEIFFER': u'SCHIEFFER',
    u'PRAHARB': u'PRAHAR',
    u'HUGHESMK': u'HUGHES',
    u'PRUNELL': u'PURNELL',
    u'RNORLAND': u'NORLAND',
    u'SEMBLE': u'SEMBLER',
    u'SPOLGI': u'SPOGLI',
    u'THOMPSONJONES': u'THOMPSON-JONES',
    u'KIRY': u'KIRBY',
    u'CHAUDRY': u'CHAUDHRY',
    u'CHAUHDRY': u'CHAUDHRY',
    u'RADSDALE': u'RAGSDALE',
    u'STEPHENON': u'STEPHENSON',
    u'WWAHBA': u'WAHBA',
    u'BRADKTE': u'BRADTKE',
    u'GALBRATIH': u'GALBRAITH',
    u'MCOLEMAN': u'COLEMAN',
    u'CSMCGANN': u'MCGANN',
    u'PERRYJC': u'PERRY',
    u'RNOLAN': u'NOLAN',
    u'MYOVANOVITCH': u'YOVANOVITCH',
    u'PAMLER': u'PALMER',
    u'PALMERALMER': u'PALMER',
    u'DRSE': u'DERSE',
    u'SSUTTON': u'SUTTON',
    u'JACKSN': u'JACKSON',
    u'MUSOMELLI': u'MUSSOMELI',
    u'MUSSOMELLI': u'MUSSOMELI',
    u'JMUSSOMELI': u'MUSSOMELI',
    u'FBCOOK': u'COOK',
    u'LNIGRO': u'NIGRO',
    u'SBREMNER': u'BREMNER',
    u'DUNNTJ': u'DUNN',
    u'RWBULLEN': u'BULLEN',
    u'SANDERSO': u'SANDERSON',
    u'TCARNEY': u'CARNEY',
    u'GLAGPIE': u'GLASPIE',
    u'KHAHILIZAD': u'KHALILZAD',
    u'KHAHILZAD': u'KHALILZAD',
    u'QBUTENIS': u'BUTENIS',
    u'MFMARRANO': u'MARRANO',
    u'HILLASK': u'HILLAS',
    u'HILLASKM': u'HILLAS',
    u'JBIGUS': u'BIGUS',
    u'WILLIAMSONB': u'WILLIAMSON',
    u'CUNNINGHA': u'CUNNINGHAM',
    u'DGRAZE': u'GRAZE',
    u'BRUDVIGLA': u'BRUDVIG',
    u'COUSINE': u'COUSIN',
    u'GLOVERMP': u'GLOVER',
    u'RGREENE': u'GREENE',
    u'GHEHM': u'GHNEHM',
    u'GHENM': u'GHNEHM',
    u'SMSELDOWITZ': u'SELDOWITZ',
    u'MCDNALD': u'MCDONALD',
    u'JSULLIVAN': u'SULLIVAN',
    u'SILLIVAN': u'SULLIVAN',
    u'SHAPIR': u'SHAPIRO',
    u'MMERANTE': u'MERANTE',
    u'NICKOLSON': u'NICHOLSON',
    u'SANDROLONI': u'SANDROLINI',
    u'JVNOYES': u'NOYES',
    u'DBUTCHER': u'BUTCHER',
    u'DBOOTH': u'BOOTH',
    u'DDARNELL': u'DARNELL',
    u'ENWISTLE': u'ENTWISTLE',
    u'SCHREIBER-HUGHES': u'SCHREIBERHUGHES',
    u'LBSCHREIBERHUGHES': u'SCHREIBERHUGHES',
    u'SMBALL': u'BALL',
}

def canonicalize_signer(signer):
    """\
    Returns the canonicalized form of the provided signer's name.

    `signer`
        The signer (a string) to canonicalize
    """
    signer = signer.upper()
    return _SIGNER_C14N.get(signer, signer)

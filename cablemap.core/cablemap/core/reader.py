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
This module extracts information from cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
import re
import logging
import codecs
from constants import MIN_ORIGIN_LENGTH, MAX_ORIGIN_LENGTH
from models import Cable

#
# Cables w/o a subject
#
_CABLES_WITHOUT_SUBJECT = ('06KABUL3934', 
    '08BRASILIA504', '08OSLO585', '09PESHAWAR2', 
    '09MADRID604', '09CARACAS1296', '09SAOPAULO663',
    '02BRASILIA4227', '09BRASILIA953', '10ABUDHABI9',
    '10RIYADH61', '09SAOPAULO660', '07SAOPAULO855',
    '08STOCKHOLM257', '08STOCKHOLM722', '08STOCKHOLM748',
    '08STOCKHOLM781', '09STOCKHOLM64', '09STOCKHOLM237',
    '03BRASILIA698', '04BRASILIA222', '05BRASILIA1567',
    '06SAOPAULO675', '06SAOPAULO910', '06SAOPAULO1197',
    '07SAOPAULO1007', '09BRASILIA1042', '04BRASILIA873',
    '09BRASILIA1262', '06BRASILIA2315', '06BRASILIA971',
    '08BRASILIA806', '05BRASILIA3124', '08BRASILIA1477',
    '09SAOPAULO144', '09RIODEJANEIRO363', '10BRASILIA33',
    '04BRASILIA2803', '05BRASILIA715', '06BRASILIA861',
    '08BRASILIA1253', '09STATE103113', '09BRASILIA1360',
    '02ANKARA8305', '03BRASILIA907', '04BRASILIA2939',
    '05BRASILIA2231', '05PARIS7777', '05BRASILIA3251',
    '06ANKARA331', '06SANTODOMINGO409', '06BRASILIA476',
    '06ANKARA3352', '07BRASILIA572', '08MOSCOW3394',
    '09UNVIEVIENNA192', '09MOSCOW2353', '10ATHENS57',
    '10BERLIN81',
    )

#
# Cables w/o tags
#
_CABLES_WITHOUT_TAGS = ('06KABUL3934', '08BEIJING3662')

#
# Cables without a transmission identifier.
#
_CABLES_WITHOUT_TID = (
    '66BUENOSAIRES2481', '72TEHRAN1164', '72TEHRAN5055', '75TEHRAN2069', 
    '79TEHRAN8980', '86MADRID5480', '88BAGHDAD28', '89PANAMA8545', 
    '90CAPETOWN97', '01PRETORIA1173', '03ABUDHABI2641', '5MOSCOW11807', 
    '05MOSCOW11807', '07STATE152317', '08STATE15220', '08CARACAS420', 
    '08STATE30340', '08STATE50524', '08ISLAMABAD2524', '08KABUL1975',
    '08STATE79112', '08VLADIVOSTOK68', '08STATE90980', '08LONDON2651', 
    '08LONDON2673', '08STATE116392', '08ISLAMABAD3716', '08STATE116943', 
    '08KABUL3176', '08MADRID1359', '09ISLAMABAD10', '09ISLAMABAD24',
    '09KABUL165', '09LUANDA51', '09MEXICO193', '09STATE6423', 
    '09ABUDHABI192', '09ASHGABAT218', '09ASMARA47', '09HAVANA132', 
    '09KHARTOUM249', '09PESHAWAR41', '09STATE11937', '09STATE14070',
    '09STATE15113', '09ASMARA80', '09BAKU179', '09DOHA214',
    '09ISLAMABAD478', '09RIYADH447', '09RIYADH496', '09STATE30049',
    '09LONDON860', '09STATE34394', '09STATE34688', '09STATE37561',
    '09STATE37566', '09CAIRO874', '09RIYADH716', '09STATE52368',
    '09BEIJING1761', '09PORTAUPRINCE575', '09SINGAPORE529', '09STATE62392',
    '09STATE62393', '09STATE62395', '09STATE62397', '09STATE67105',
    '09TRIPOLI475', '09TUNIS399', '09ABUDHABI862', '09LONDON1946',
    '09ULAANBAATAR234', '09ISLAMABAD2185', '09ISLAMABAD2295', '09JEDDAH343',
    '09STATE100153', '09ISLAMABAD2523', '09ISLAMABAD2523', '09MEXICO2882',
    '09MANAMA642', '09SAOPAULO653',
    '09ASMARA429', '10ABUDHABI9', '10SANAA4', '10STATE17263',
    '09VATICAN28', '09VATICAN59', '09STATE63860', '04TASHKENT3180',
    '05TASHKENT284', '05TASHKENT2473', '06LIMA622', '08STOCKHOLM781',
    '09LONDON27', '09STOCKHOLM31', '09STOCKHOLM237', '10LONDON268',
    '08ASMARA543', '06TRIPOLI198', '08STATE23763', '08STATE65820',
    '08KHARTOUM1768', '09USUNNEWYORK306', '09THEHAGUE247', '09BOGOTA2736',
    '09MADRID98', '90BAGHDAD4237', '90BAGHDAD4397', '04BAGHDAD4',
    '06BRASILIA1511', '73TEHRAN2077', '01PARIS11204', '02ANKARA8305',
    '08REYKJAVIK110', '08STATE83144', '08STATE99666', '08REYKJAVIK258',
    '08REYKJAVIK291', '09STATE3943', '09REYKJAVIK41', '09STATE17176',
    '09GENEVA203', '09BERLIN485', '09BERLIN1054', '10STATE9584', 
    '01STATE176819',
    ) # was meant for debugging purposes. Who would expected that long list for the bloody, unimporant transmission ID? :)

_CABLES_WITHOUT_TO = ('09STATE15113',)

def cable_from_file(filename, ignore_errors=False):
    """\
    Returns a cable from the provided file.
    """
    html = codecs.open(filename, 'rb', 'utf-8').read()
    reference_id = None
    slash_idx = filename.rfind('/')
    if not slash_idx > 0:
        raise Exception('Cannot find directory slash in ' + filename)
    slash_idx+=1
    if filename.rfind('.htm') > 0:
        reference_id = filename[slash_idx:filename.rfind('.')]
    else:
        reference_id = filename[slash_idx:]
    return cable_from_html(html, reference_id)

def cable_from_html(html, reference_id, ignore_errors=False):
    """\
    Returns a cable from the provided HTML page.
    """
    def year(y):
        date, time = y.split()
        return date.split('-')[:2]
    file_content = fix_html_content(html, reference_id)
    cable = Cable(reference_id)
    parse_meta(file_content, cable)
    header = get_header_as_text(file_content)
    content =  get_content_as_text(file_content)
    cable.header = header
    cable.content = content
    content_header, content_body = header_body_from_content(content)
    if content_header:
        cable.content_header = content_header
        cable.content_body = content_body
    else:
        content_header = content
    cable.subject = parse_subject(content_header, reference_id, ignore_errors=ignore_errors)
    cable.tags = parse_tags(content_header, reference_id, ignore_errors=ignore_errors)
    cable.references = parse_references(content_header, year(cable.created)[0], reference_id)
    cable.partial = 'This record is a partial extract of the original cable' in header
    if not cable.partial:
        cable.transmission_id = parse_tranmission_id(header, reference_id, ignore_errors=ignore_errors)
        cable.recipients = parse_recipients(header, reference_id)
    cable.info_recipients = parse_info_recipients(header, reference_id)
    cable.nondisclosure_deadline = parse_nondisclosure_deadline(content_header)
    cable.summary = parse_summary(content_body or content, reference_id)
    return cable

def fix_html_content(content, reference_id):
    """\
    Converts ``&#x000A;`` to ``\n`` and fixes the content of some cables.
    """
    content = content.replace(ur'&#x000A;', u'\n')
    # malformed cables
    if reference_id == '10MADRID87':
        content = content.replace(u' \n <\nREF', u' \n\nREF') #10MADRID87
    elif reference_id == '04ANKARA348':
        content = content.replace(u'Subject: turkish p.m. Erdogan goes', u'\nSubject: turkish p.m. Erdogan goes') #04ANKARA348
    elif reference_id == '09STATE30049':
        content = content.replace(u'Secretary Clinton’s March 24, 2009 \n\n', u'Secretary Clinton’s March 24, 2009 \n') #09STATE30049
    elif reference_id == '06BRASILIA882': #TODO: The subject parser should detect that
        content = content.replace(u'ENERGY INSTALLATIONS REF: BRASILIA 861', u'ENERGY INSTALLATIONS \n\nREF: BRASILIA 861')
    return content


_CONTENT_PATTERN = re.compile(ur'(?:<code><pre>)(.+?)(?:</pre></code>)', re.DOTALL|re.UNICODE)

def get_content_as_text(file_content):
    """\
    Returns the cable content as text.
    
    `file_content`
        The HTML file content, c.f. `get_file_content`.
    """
    content = _clean_html(_CONTENT_PATTERN.findall(file_content)[-1])
    return content

def get_header_as_text(file_content):
    """\
    Returns the cable's header as text.
    
    `file_content`
        The HTML file content, c.f. `get_file_content`.
    """
    res = _CONTENT_PATTERN.findall(file_content)
    if len(res) == 2:
        content = res[0]
    elif len(res) == 1:
        return ''
    else:
        raise Exception('Unexpected <code><pre> sections: "%r"' % res)
    return _clean_html(content)


_PILCROW_PATTERN = re.compile(ur'<a[^>]*>¶</a>', re.UNICODE)
_LINK_PATTERN = re.compile(ur'<a[^>]*>', re.UNICODE)
_HTML_TAG_PATTERN = re.compile(r'</?[a-zA-Z]+>')

def _clean_html(html):
    """\
    Removes links (``<a href="...">...</a>``) from the provided HTML input.
    Further, it removes "¶" from the texts.
    """
    content = _PILCROW_PATTERN.sub(u'', html)
    content = _LINK_PATTERN.sub(u'', content)
    content = _HTML_TAG_PATTERN.sub(u'', content)
    return content


_CLASSIFIED_BY_PATTERN = re.compile(r'Classified[ ]+by[^\n]+', re.IGNORECASE)
_FIRST_PARAGRAPH_PATTERN = re.compile(r'\n1. ')
_SUMMARY_PATTERN = re.compile(r'(BEGIN SUMMARY[ ])|(SUMMARY: )')

def header_body_from_content(content):
    """\
    Tries to extract the header and the message from the cable content.

    The header is something like

        UNCLASSIFIED ...
        SUBJECT ...
        REF ...

    while the message begins commonly with a summary

        1. SUMMARY ...
        ...
        10. ...
    
    Returns (header, msg) or (None, None) if the header/message cannot be 
    detected.
    
    `content`
        The "content" part of a cable.
    """
    m = _CLASSIFIED_BY_PATTERN.search(content)
    idx = m and m.end() or 0
    m = _SUMMARY_PATTERN.search(content)
    summary_idx = m and m.start() or None
    m = _FIRST_PARAGRAPH_PATTERN.search(content)
    para_idx = m and m.start() or None
    if summary_idx and para_idx:
        idx = max(idx, min(summary_idx, para_idx))
    elif summary_idx:
        idx = max(summary_idx, idx)
    elif para_idx:
        idx = max(para_idx, idx)
    if idx > 0:
        return content[:idx], content[idx:]
    return None, None


_META_PATTERN = re.compile(r'''<table\s+class\s*=\s*(?:"|')cable(?:"|')\s*>.+?<td>\s*<a.+?>(.+?)</a>.+<td>\s*<a.+?>(.+?)</a>.+<td>\s*<a.+?>(.+?)</a>.+<td>\s*<a.+?>(.+?)</a>.+<td>\s*<a.+?>(.+?)</a>''', re.MULTILINE|re.DOTALL)

def parse_meta(file_content, cable):
    """\
    Extracts the reference id, date/time of creation, date/time of release,
    the classification, and the origin of the cable and assigns the values
    to the provided `cable`.
    """
    end_idx = file_content.rindex("</table>")
    start_idx = file_content.rindex("<table class='cable'>", 0, end_idx)
    m = _META_PATTERN.search(file_content, start_idx, end_idx)
    if not m:
        raise Exception('Cable table not found')
    if len(m.groups()) != 5:
        raise Exception('Unexpected metadata result: "%r"' % m.groups())
    # Table content: 
    # Reference ID | Created | Released | Classification | Origin
    ref, created, released, classification, origin = m.groups()
    if cable.reference_id != ref:
        raise Exception('cable.reference_id != ref. reference_id="%s", ref="%s"' % (cable.reference_id, ref))
    cable.created = created
    cable.released = released
    cable.origin = origin
    # classifications are usually written in upper case, but you never know.. 
    cable.classification = [cls.upper() for cls in classification.split('//')]
    return cable


_TID_PATTERN = re.compile(r'^([A-Z]+[0-9]+)', re.UNICODE)

def parse_tranmission_id(header, reference_id, ignore_errors=False):
    # malformed cable header
    if reference_id == '09STATE119085': # It has a TID, but the header starts with "S E C R E T   STATE   00119085 \nVZCZCXRO1706\nPP RUEHAG"
        return u'VZCZCXRO1706' 
    elif reference_id == '07LONDON4045': # It has a TID, but the header starts with "Cable Text: "
        return u'VZCZCLOI278'
    m = _TID_PATTERN.match(header.replace('Cable Text:', ''))
    if not m:
        if reference_id in _CABLES_WITHOUT_TID:
            return None
        msg = 'No transmission ID found in "%s", header: "%s"' % (reference_id, header)
        if ignore_errors:
            logging.info(msg)
            return None
        else:
            raise Exception(msg)
    return m.group(0)


_NAME2ROUTE = None

_ADDITIONAL_ROUTES = {
    'USMISSION USNATO': 'RUCNDT', # RUCNDT USMISSION USUN NEW YORK NY
    'USMISSION USUN NEW YORK': 'RUCNDT', # see above
    'SECSTATE WASHDC': 'RUEHC',
    'AMEMBASSY GUATEMALA': 'RUEHGT',
    'AMCONSUL LAGOS': 'RUEHOS',
    'AMCONSUL MELBOURNE': 'RUEHBN',
    'AMEMBASSY PANAMA': 'RUEHZP',
    'AMEMBASSY MEXICO': 'RUEHME',
    'AMEMBASSY VATICAN': 'RUEHROV',
    'AMEMBASSY ALMATY': 'RUEHTA', # Used in cables
    'AMEMBASSY QUITO': 'RUEHQT', # Used in cables 
    'AMCONSUL JOHANNESBURG': 'RUEHJO', # "RUEHJO" is used in cables
    'XMT AMCONSUL JOHANNESBURG': 'RUEHJO', #TODO: XMT?!?
    'XMT AMCONSUL STRASBOURG': 'RUEHSR', #TODO: XMT?!?
    'HQ USAFRICOM STUTTGART GE': 'RHWSAFC', # RHWSAFC STR09 SACCS USAFRICOM COMMAND CENTER STUTTGART GE
    'DEPT OF JUSTICE WASHINGTON DC': 'RUEAWJA', # RUEAWJA THRU RUEAWJD DEPT OF JUSTICE WASHINGTON DC
    'DEPARTMENT OF JUSTICE WASHINGTON DC': 'RUEAWJA', # RUEAWJA THRU RUEAWJD DEPT OF JUSTICE WASHINGTON DC
    'NATIONAL SECURITY COUNCIL WASHINGTON DC': 'RHEHNSC',
    'NSC WASHINGTON DC': 'RHEHNSC',
    'AMEMBASSY RIO DE JANEIRO': 'RUEHRI', #  AMCONSUL RIO DE JANEIRO'
    'DIA WASHINGTON DC': 'RHEFJMA', # DIA JMAS WASHINGTON DC
    'HQ USCENTCOM MACDILL AFB FL': 'RUMICEA', #TODO, see below
    'CDR USCENTCOM MACDILL AFB FL': 'RUMICEA',  #TODO: "RUMICEA" = USCENTCOM INTEL CEN MACDILL AFB FL
                                                #      "RUCQSAB" = USSOCOM INTEL MACDILL AFB FL
    'COMSOCCENT MACDILL AFB FL': 'RHMFIUU',
    'HQ USSOCOM MACDILL AFB FL': 'RHMFIUU',
    'USCINCCENT MACDILL AFB FL': 'RUMICEA',  # see above
    'USEU BRUSSELS': 'RUEHNO', # RUEHNO US MISSIONS BRUSSELS BE
    'SECDEF': 'RUEKJCS', # "RUEKJCS" is commonly used in the cables RUEKJCS/SECDEF ...
    'SECDEF WASHINGTON DC': 'RUEKJCS', # "RUEKJCS" is commonly used in the cables RUEKJCS/SECDEF ...
    'DEPT OF HOMELAND SECURITY WASHINGTON DC': 'RHEFHLC', # used in the cables: RHEFHLC/DEPT OF HOMELAND SECURITY WASHINGTON DC
    'HOMELAND SECURITY CENTER WASHINGTON DC': 'RHEFHLC',
    'USMISSION UNVIE VIENNA': 'RUEHUNV', # RUEHUNV USMISSIN UNVIE VIENNA
    'THE WHITE HOUSE WASHINGTON DC': 'RHEHAAA',
    'WHITE HOUSE WASHINGTON DC': 'RHEHAAA',
    'CJCS WASHINGTON DC': 'RUEKJCS',
    # COMUSKOREA
    'COMUSKOREA J': 'RUACAAA',
    'COMUSFK SEOUL KOR': 'RUACAAA',
    'COMUSKOREA SCJS SEOUL KOR': 'RUACAAA',
    # Collective routes extracted from other cables:
    'EUROPEAN POLITICAL COLLECTIVE': 'RUEHZL',
    'EU MEMBER STATES COLLECTIVE': 'RUCNMEM',
    'GULF COOPERATION COUNCIL COLLECTIVE': 'RUEHZM',
    'MERCOSUR COLLECTIVE': 'RUCNMER',
    'IRAN COLLECTIVE': 'RUCNIRA',
    'WESTERN HEMISPHERIC AFFAIRS DIPL POSTS': 'RUEHWH',
    'MOSCOW POLITICAL COLLECTIVE': 'RUEHXD',
    'IRAQ COLLECTIVE': 'RUCNRAQ',
    'ECOWAS COLLECTIVE': 'RUEHZK',
    'ARAB ISRAELI COLLECTIVE': 'RUEHXK',
    'ARAB LEAGUE COLLECTIVE': 'RUEHEE',
    'SOUTHERN AFRICAN DEVELOPMENT COMMUNITY': 'RUCNSAD',
    'SOUTHERN AF DEVELOPMENT COMMUNITY COLLECTIVE': 'RUCNSAD',
    'DARFUR COLLECTIVE': 'RUCNFUR',
    'AFRICAN UNION COLLECTIVE': 'RUEHZO',
    'ALL US CONSULATES IN MEXICO COLLECTIVE': 'RUEHXC',
    'OPEC COLLECTIVE': 'RUEHHH',
    'ALL NATO POST COLLECTIVE': 'RUEHXP',
    'ENVIRONMENT SCIENCE AND TECHNOLOGY COLLECTIVE': 'RUEHZN',
    'AFGHANISTAN COLLECTIVE': 'RUCNAFG',
    'WHA CENTRAL AMERICAN COLLECTIVE': 'RUEHZA',
    'UN SECURITY COUNCIL COLLECTIVE': 'RUEHGG',
    'IGAD COLLECTIVE': 'RUCNIAD',
    'DEA HQS WASHINGTON DC': 'RUEABND',
    'OSD WASHINGTON DC': 'RUEKJCS',
    'HAITI COLLECTIVE': 'RUEHZH',
    'NCTC WASHINGTON DC': 'RUEILB',
    'SOMALIA COLLECTIVE': 'RUCNSOM',
    'CDR USPACOM HONOLULU HI': 'RHHMUNA',
    'HQ USAFRICOM STUTTGART GE': 'RUEWMFD', # Also: 'HQ USAFRICOM STUTTGART GE': 'RUZEFAA',
    'CDR USAFRICOM STUTTGART GE': 'RUEWMFD', # Also: 'HQ USAFRICOM STUTTGART GE': 'RUZEFAA',
    'EUCOM POLAD VAIHINGEN GE': 'RHMCSUU',
    'HQ USEUCOM VAIHINGEN GE': 'RHMCSUU',
    'CDR USEUCOM VAIHINGEN GE': 'RHMCSUU',
    'HQ USSOUTHCOM MIAMI FL': 'RUMIAAA',
    'CDR USSOUTHCOM MIAMI FL': 'RHMFIUU',
    'RWANDA COLLECTIVE': 'RUEHXR',
    'COMNAVBASE GUANTANAMO BAY CU': 'RUCOGCA',
    'NAVINTELOFC GUANTANAMO BAY CU': 'RUCOGCA',
    'MAGHREB COLLECTIVE': 'RUCNMGH',
}

def _route_for_name(name):
    NAME2ROUTE = globals().get('_NAME2ROUTE')
    if not NAME2ROUTE:
        NAME2ROUTE = {}
        import os
        root_dir = os.path.dirname(os.path.abspath(__file__))
        f = open(root_dir + '/routes.txt')
        route_pattern = re.compile('^(R[A-Z]+)(?:[ ]+)(.+)$')
        for l in f:
            m = route_pattern.match(l)
            NAME2ROUTE[m.group(2)] = m.group(1)
        NAME2ROUTE.update(_ADDITIONAL_ROUTES)
        globals()['_NAME2ROUTE'] = NAME2ROUTE
    res = NAME2ROUTE.get(name)
    if not res and name.endswith('WASHDC'):
        res = NAME2ROUTE.get(name.replace('WASHDC', 'WASHINGTON DC'), None)
    return res


_REC_PATTERN = re.compile(r'([A-Z]+/)?([A-Z -]{2,})(?:.*$)', re.MULTILINE|re.UNICODE)

def _route_recipient_from_header(header, reference_id):
    res = []
    for route, recipient in _REC_PATTERN.findall(header):
        if route:
            route = route.replace('/', '')
        if route == 'RHMFISS':
            route = None
        for x in ('PRIORITY', 'IMMEDIATE',
                  'NIACT', #TODO: NIght ACTion (US government immediate action security classification)
                  ):
            recipient = recipient.replace(x, '')
        if reference_id == '09BAKU179':
            recipient = recipient.replace('PIORITY', '')
        recipient = recipient.strip()
        if recipient in ('PAGE', # 08STATE23763
                         'RHMFISS', # Unclassified but Sensitive, MFI residing on the DMS NIPRNET
                         'RHMFIUU', # Secret MFI, residing on the DMS SIPRNET
                        ):
            recipient = None
        if not route and recipient:
            route = _route_for_name(recipient)
        if route or recipient:
            res.append((route, recipient))
    return res


_TO_PATTERN = re.compile(r'(?:\nTO\s+)(.+?)(?=INFO|\Z)', re.DOTALL|re.UNICODE)

def parse_recipients(header, reference_id):
    """\
    Returns the recipients of the cable as (maybe empty) list.
    """
    m = _TO_PATTERN.search(header)
    if not m:
        if reference_id in _CABLES_WITHOUT_TO:
            return []
        raise Exception('No TO header found in "%s"' % header)
    to_header = m.group(1)
    return _route_recipient_from_header(to_header, reference_id)


_INFO_PATTERN = re.compile(r'(?:\nTO\s+.+?\nINFO\s+)(.+?)(?=\Z)', re.DOTALL|re.UNICODE)

def parse_info_recipients(header, reference_id):
    """\
    Returns the informal recipients of the cable as (maybe empty) list.    
    """
    m = _INFO_PATTERN.search(header)
    if not m:
        return []
        #raise Exception('No INFO header found in "%s"' % header)
    to_header = m.group(1)
    return _route_recipient_from_header(to_header, reference_id)
    res = []
    for code, recipient in _REC_PATTERN.findall(to_header):
        for x in ('PRIORITY', 'IMMEDIATE'):
            recipient = recipient.replace(x, '')
        if reference_id == '09BAKU179':
            recipient = recipient.replace('PIORITY', '')
        recipient = recipient.strip()
        if recipient:
            # malformed cables
            if recipient == 'PAGE':
                if reference_id =='08STATE50524':
                    recipient = 'AMEMBASSY BAGHDAD'
                if reference_id == '09STATE37566':
                    recipient = None
            elif recipient == 'XMT AMCONSUL JOHANNESBURG': # '08STATE116943', '09STATE63860', 09STATE67105 
                recipient = None
            elif reference_id == '09ANKARA1594' and recipient == 'DET':
                recipient = None
            elif reference_id in ('10PRISTINA44', '10PRISTINA84') and recipient in ('RUEOBZB', 'CDR'):
                recipient = None
            elif recipient in ('RHMFISS', 'RHMFIUU'): # ANKARA cables like '07ANKARA1091', '07ANKARA1842', '07ANKARA1905', 09ANKARA1594
                recipient = None
            elif reference_id == '10SARAJEVO134' and recipient == 'XMT AMCONSUL STRASBOURG':
                recipient = 'AMCONSUL STRASBOURG'
            elif reference_id == '09PRISTINA148' and recipient == 'CDR':
                recipient = None
        if recipient:
            res.append(recipient.strip())
    return res


_SUBJECT_PATTERN = re.compile(ur'(?:SUBJ(?:ECT)?:?\s+(?!LINE[/]+))(.+?)(?:\Z|\n[ ]*\n|[\s]*[\n][\s]*[\s]*REF:?\s|REF\(S\):?|[\r\n ]+Classified By:?\s|[1-9]\.?[ ]+Classified By|[1-9]\.?[ ]+\(SBU\)|1\.?[ ]Summary|[A-Z]+\s+[0-9]+\s+[0-9]+\.?[0-9]*\s+OF|\-\-\-\-\-*\s+|Friday|PAGE [0-9]+|This is an Action Req|REF:[ ]+\(A\))', re.DOTALL|re.IGNORECASE|re.UNICODE)
_NL_PATTERN = re.compile(ur'[\r\n]+', re.UNICODE|re.MULTILINE)
_WS_PATTERN = re.compile(ur'[ ]{2,}', re.UNICODE)
_BRACES_PATTERN = re.compile(r'^\([^\)]+\)[ ]+| \([A-Z]+\)$', re.IGNORECASE)

def parse_subject(content, reference_id=None, clean=True, ignore_errors=False):
    """\
    Parses and returns the subject of a cable.

    >>> parse_subject("TAGS: TAG TAG2\\nSUBJECT:  SINGLE LINE SUBJECT \\n\\nREF: REF 1")
    u'SINGLE LINE SUBJECT'
    >>> parse_subject("TAGS: TAG TAG2\\nSUBJECT: SUBJECT WHICH HAS a \\nSECOND LINE \\n\\nREF: REF 1")
    u'SUBJECT WHICH HAS a SECOND LINE'
    >>> parse_subject("SUBJECT: SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES \\nREF: A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\\n")
    u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'
    >>> parse_subject("SUBJECT: SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES\\nREF: A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\\n")
    u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'
    >>> parse_subject("SUBJECT: SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES\\nREF A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\\n")
    u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'
    >>> parse_subject("SUBJECT SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES\\nREF A. RIYADH 1579  B. RIYADH 1408  C. RIYADH 1298\\n")
    u'SAG AGREES TO USG STEPS TO PROTECT OIL FACILITIES'
    >>> parse_subject("SUBJECT: NEGOTIATIONS \\n \\n")
    u'NEGOTIATIONS'
    >>> parse_subject("SUBJECT: A CAUCASUS WEDDING \\nClassified By: Deputy Chief of Mission Daniel A. Russell. Reason 1.4 ( b, d)")
    u'A CAUCASUS WEDDING'
    >>> parse_subject("SUBJ: GUINEA - U.S./French Meeting with President Compaore \\n\\nClassified by Charge d\'Affaires")
    u'GUINEA - U.S./French Meeting with President Compaore'
    >>> parse_subject("SUBJECT: UAE FM DISCUSSES TALIBAN FINANCIAL FLOWS AND REINTEGRATION \\nWITH AMB. HOLBROOKE AND TREASURY A/S COHEN\\nCLASSIFIED BY: Richard")
    u'UAE FM DISCUSSES TALIBAN FINANCIAL FLOWS AND REINTEGRATION WITH AMB. HOLBROOKE AND TREASURY A/S COHEN'
    >>> parse_subject("SUBJECT:  EXTENDED NATIONAL JURISDICTIONS OVER HIGH SEAS \\n\\nREF: STATE 106206 CIRCULAR; STATE CA-3400 NOV 2, 1966")
    u'EXTENDED NATIONAL JURISDICTIONS OVER HIGH SEAS'
    >>> parse_subject('SUBJECT: (S) GERMANY TAKING ACTION ON SHIPMENT OF ...', clean=False)
    u'(S) GERMANY TAKING ACTION ON SHIPMENT OF ...'
    >>> parse_subject('SUBJECT: (S) GERMANY TAKING ACTION ON SHIPMENT OF ...', clean=True)
    u'GERMANY TAKING ACTION ON SHIPMENT OF ...'
    >>> parse_subject(u'E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu Subject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?\\n\\n(U) Classifi')
    u'turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?'
    >>> parse_subject("SUBJECT: PART 3 OF 3:  THE LIFE AND TIMES OF SOUTH AFRICA'S \\nNEW PRESIDENT\\nPRETORIA 00000954 001.2 OF 004\\n")
    u"PART 3 OF 3: THE LIFE AND TIMES OF SOUTH AFRICA'S NEW PRESIDENT"
    >>> parse_subject("SUBJECT: ZIM NOTES 11-09-2009 \\n----------- \\n1. SUMMARY\\n----------- \\n")
    u'ZIM NOTES 11-09-2009'
    >>> parse_subject("TAGS: PGOV EINV INRB GM\\nSUBJECT: GERMANY/BAVARIA: CSU HOPES FOR FRESH START WITH NEW AND\\nYOUNGER FACES IN CABINETAND A DYNAMIC SECRETARY GENERAL \\n\\n")
    u'GERMANY/BAVARIA: CSU HOPES FOR FRESH START WITH NEW AND YOUNGER FACES IN CABINETAND A DYNAMIC SECRETARY GENERAL'
    >>> parse_subject('SUBJECT: ASSISTANT SECRETARY MEETS WITH ZIMBABWE \\n CONFIDENTIAL\\nPAGE 02 HARA')
    u'ASSISTANT SECRETARY MEETS WITH ZIMBABWE CONFIDENTIAL'
    >>> parse_subject('TAGS ENRG, EUN, ECON, EIND, KGHG, SENV, SW\\nSUBJECT: SWEDISH DEPUTY PM URGES SENIOR USG VISITS TO SWEDEN DURING\\nEU PRESIDENCY; WANTS TO LAUNCH U.S.-EU ALERNATIVE ENERGY PARTNERSHIP AT U.S.-EU SUMMIT\\nThis is an Action request. Please see para 2.\\n')
    u'SWEDISH DEPUTY PM URGES SENIOR USG VISITS TO SWEDEN DURING EU PRESIDENCY; WANTS TO LAUNCH U.S.-EU ALERNATIVE ENERGY PARTNERSHIP AT U.S.-EU SUMMIT'
    >>> parse_subject('C O R R E C T E D COPY//SUBJECT LINE//////////////////////////////////\\n\\nNOFORN\\nSIPDIS\\n\\nEO 12958 DECL: 07/09/2018\\nTAGS PREL, PTER, MOPS, IR, PK, AF, CA\\n\\nSUBJECT: COUNSELOR, CSIS DIRECTOR DISCUSS CT THREATS,\\nPAKISTAN, AFGHANISTAN, IRAN\\nREF: A. OTTAWA 360 B. OTTAWA 808 C. OTTAWA 850 D. OTTAWA 878\\nOTTAWA 00000918 001.2 OF 003\\n')
    u'COUNSELOR, CSIS DIRECTOR DISCUSS CT THREATS, PAKISTAN, AFGHANISTAN, IRAN'
    >>> parse_subject(u"TAGS OVIP (CLINTON, HILLARY), PGOV, PREL, KDEV, ECON,\\nNL, IS, SR\\nSUBJECT: (U) Secretary Clinton's July 14 conversation\\nwith Dutch Foreign Minister Verhagen\\n1. Classified by Bureau Assistant Secretary Philip H. Gordon. Reason: 1.4 (d)\\n2. (U) July 14; 2:45 p.m.; Washington, DC.\\n3. (SBU) Participants:\\n", clean=False)
    u"(U) Secretary Clinton's July 14 conversation with Dutch Foreign Minister Verhagen"
    >>> parse_subject(u"TAGS OVIP (CLINTON, HILLARY), PGOV, PREL, KDEV, ECON,\\nNL, IS, SR\\nSUBJECT: (U) Secretary Clinton's July 14 conversation\\nwith Dutch Foreign Minister Verhagen\\n1. Classified by Bureau Assistant Secretary Philip H. Gordon. Reason: 1.4 (d)\\n2. (U) July 14; 2:45 p.m.; Washington, DC.\\n3. (SBU) Participants:\\n")
    u"Secretary Clinton's July 14 conversation with Dutch Foreign Minister Verhagen"
    >>> parse_subject('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\\n\\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ')
    u'AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO'
    >>> parse_subject("SUBJECT: BRAZIL: BLACKOUT -CAUSES AND IMPLICATIONS Classified By: Charge d'Affaires Cherie Jackson, Reasons 1.4 (b) and (d). REFTELS: A) 2008 BRASILIA 672, B) 2008 BRASILIA 593, C)2008 SAO PAULO 260\\n")
    u'BRAZIL: BLACKOUT -CAUSES AND IMPLICATIONS'
    >>> parse_subject('SUBJECT: MEMBERS OF CONGRESS DISCUSS BONUSES, BAIL-OUTS AND\\nOTHER REFORM MEASURES WITH UK OFFICIALS\\n1. (SBU) Summary. Bonuses, regulatory structures')
    u'MEMBERS OF CONGRESS DISCUSS BONUSES, BAIL-OUTS AND OTHER REFORM MEASURES WITH UK OFFICIALS'
    >>> parse_subject('SUBJECT: AARGH! SWEDISH PIRATES SET SAIL FOR BRUSSELS\\n1. Summary and Comment: Sweden')
    u'AARGH! SWEDISH PIRATES SET SAIL FOR BRUSSELS'
    >>> parse_subject('SUBJECT: EU JHA INFORMAL MINISTERIAL\\n1. Summary. EU Justice and Home...')
    u'EU JHA INFORMAL MINISTERIAL'
    >>> parse_subject('\\nSUBJECT: CARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA REF: (A) 05 SAO PAULO 405; (B) 05 SAO PAULO 402 (C) 02 BRASILIA 2670')
    u'CARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA'
    """
    m = _SUBJECT_PATTERN.search(content, 0, 1200)
    if not m:
        if reference_id in _CABLES_WITHOUT_SUBJECT:
            return None
        msg = 'No subject found in cable "%s", content: "%s"' % (reference_id, content)
        if ignore_errors:
            logging.warn(msg)
            return None
        else:
            raise Exception(msg)
    res = _NL_PATTERN.sub(' ', m.groups()[0]).strip()
    res = _WS_PATTERN.sub(' ', res)
    res = res.replace(u'&#8217;', u'’') \
                .replace(u'&#8220;', u'“') \
                .replace(u'&#8221;', u'”')
    if clean:
        res = _BRACES_PATTERN.sub('', res)
    if '&#' in res:
        raise Exception('Unreplaced HTML entities in "%s", "%s"' % (res, content))
    return res


# Commonly month/day/year is used, but sometimes year/month/day
_DEADLINE_PATTERN = re.compile(r'(?:E.?O.?\s*12958:?\s*DECL\s*:?\s*)([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})|([0-9]{4}/[0-9]{2}/[0-9]{2})', re.IGNORECASE|re.UNICODE)

def parse_nondisclosure_deadline(content):
    """\
    Returns the non-disclosure deadline if provided.


    >>> parse_nondisclosure_deadline('DEPT FOR WHA/BSC E.O. 12958: DECL: 11/22/2012 ')
    u'2012-11-22'
    >>> parse_nondisclosure_deadline('EO 12958 DECL: 2020/02/23')
    u'2020-02-23'
    >>> parse_nondisclosure_deadline('E.O. 12958: DECL: 11/03/2015')
    u'2015-11-03'
    >>> parse_nondisclosure_deadline('EO 12958 DECL: 12/31/2034')
    u'2034-12-31'
    >>> parse_nondisclosure_deadline('E.O. 12958 DECL: 12/31/2034')
    u'2034-12-31'
    >>> parse_nondisclosure_deadline('E.o. 12958: decl: 07/01/2034')
    u'2034-07-01'
    >>> parse_nondisclosure_deadline(u'E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu Subject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?\\n\\n(U) Classifi')
    u'2014-01-07'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 12/31/2034')
    u'2034-12-31'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 6/30/08')
    u'2008-06-30'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 6/3/08')
    u'2008-06-03'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 06/30/08')
    u'2008-06-30'
    """
    m = _DEADLINE_PATTERN.search(content)
    if not m:
        return None
    p1, p2 = m.groups()
    if p1:
        month, day, year = p1.split('/')
        if len(year) != 4:
            year = 2000 + int(year)
        if len(month) != 2:
            month = '0%s' % month
        if len(day) != 2:
            day = '0%s' % day
    else:
        year, month, day = p2.split('/')
    return u'%s-%s-%s' % (year, month, day)


_MONTHS = (
    'JANUARY',
    'FEBRUARY',
    'MARCH',
    'APRIL',
    'MAY', 
    'JUNE',
    'AUGUST',
    'SEPTEMBER',
    'OCTOBER',
    'NOVEMBER',
    'DECEMBER',
)

_REF_START_PATTERN = re.compile(r'(?:[\nPROGRAM ]*REF|REF\(S\):?\s*)([^\n]+(\n\s*[0-9]+[,\s]+[^\n]+)?)', re.IGNORECASE|re.UNICODE)
_REF_LAST_REF_PATTERN = re.compile(r'(\n[ ]*[A-Z](?:\.(?!O\.|S\.)|\))[^\n]+)', re.IGNORECASE|re.UNICODE)
_REF_PATTERN = re.compile(r'(?:[A-Z](?:\.|\))\s*)?([0-9]{2,4})?(?:\s*)([A-Z ]*[A-Z]+)(?:\s*)([0-9]+)', re.MULTILINE|re.UNICODE|re.IGNORECASE)
_CLASSIFIED_BY_PATTERN = re.compile(r'\n[ ]*Classified\s+By:\s+', re.IGNORECASE|re.UNICODE)

def parse_references(content, year, reference_id=None):
    """\
    Returns the references to other cables as (maybe empty) list.
    
    >>> # <http://wikileaks.ch/cable/2007/07/07TBILISI1732.html>
    >>> parse_references('\\nREF: A. TBILISI 1605  B. TBILISI 1352  C. TBILISI 1100  D. 06 TBILISI 2601  E. 06 TBILISI 2590  F. 06 TBILISI 2425  G. 06 TBILISI 2390  H. 06 TBILISI 1532  I. 06 STATE 80908  J. 06 TBILISI 1064  K. 06 TBILISI 0619  L. 06 TBILISI 0397  M. 06 MOSCOW 0546  N. 06 TBILISI 0140  O. 05 TBILISI 3171', 2007)
    [u'07TBILISI1605', u'07TBILISI1352', u'07TBILISI1100', u'06TBILISI2601', u'06TBILISI2590', u'06TBILISI2425', u'06TBILISI2390', u'06TBILISI1532', u'06STATE80908', u'06TBILISI1064', u'06TBILISI619', u'06TBILISI397', u'06MOSCOW546', u'06TBILISI140', u'05TBILISI3171']
    >>> # <http://213.251.145.96/cable/2008/09/08PARIS1698.html>
    >>> parse_references('\\nREF: A. PARIS 1501 \\nB. PARIS 1568 \\nC. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832 \\n0617 08)\\nD. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832 \\n0626 08) ', 2008)
    [u'08PARIS1501', u'08PARIS1568']
    >>> # <http://wikileaks.ch/cable/2008/08/08PARIS1501.html>
    >>> parse_references('\\nREF: A. 05 PARIS 5459 \\nB. 06 PARIS 5733', 2008)
    [u'05PARIS5459', u'06PARIS5733']
    >>> # <http://wikileaks.ch/cable/2007/06/07TALLINN375.html>
    >>> parse_references('\\nREF: A) TALLINN 366 B) LEE-GOLDSTEIN EMAIL 05/11/07 \\nB) TALLINN 347 ', 2007)
    [u'07TALLINN366', u'07TALLINN347']
    >>> # <http://wikileaks.ch/cable/2007/11/07TRIPOLI943.html>
    >>> parse_references('\\nREF: A) STATE 135205; B) STATE 127608; C) JOHNSON-STEVENS/GODFREY E-MAIL 10/15/07; D) TRIPOLI 797; E) TRIPOLI 723 AND PREVIOUS', 2007)
    [u'07STATE135205', u'07STATE127608', u'07TRIPOLI797', u'07TRIPOLI723']
    >>> # <http://wikileaks.ch/cable/2007/11/07STATE156011.html>
    >>> parse_references('\\nREF: LA PAZ 2974', 2007)
    [u'07LAPAZ2974']
    >>> # <http://213.251.145.96/cable/2005/11/05PARIS7835.html>
    >>> parse_references('\\nREF: A. (A) PARIS 7682 AND PREVIOUS ', 2005)
    [u'05PARIS7682']
    >>> # <http://213.251.145.96/cable/2005/11/05PARIS7835.html>
    >>> parse_references('\\nREF: A. (A) PARIS 7682 AND PREVIOUS \\n\\nB. (B) EMBASSY PARIS DAILY REPORT FOR OCTOBER 28 - \\nNOVEMBER 16 (PARIS SIPRNET SITE) \\nC. (C) PARIS 7527 ', 2005)
    [u'05PARIS7682', u'05PARIS7527']
    >>> # <http://213.251.145.96/cable/2009/08/09MADRID869.html>
    >>> parse_references('\\nSUBJECT: UPDATES IN SPAIN’S INVESTIGATIONS OF RUSSIAN MAFIA \\nREF: A. OSC EUP20080707950031  B. OSC EUP20081019950022  C. OSC EUP20090608178005  D. MADRID 286  E. OSC EUP20050620950076  F. OSC EUP20080708950049  G. OSC EUP20081029950032  H. OSC EUP 20061127123001\\nMADRID 00000869 001.2 OF 004\\n', 2009)
    [u'09MADRID286']
    >>> # <http://wikileaks.ch/cable/2007/11/07STATE152317.html>
    >>> parse_references('\\nREF: (A)STATE 071143, (B)STATE 073601, (C)STATE 72896, (D)BEIJING \\n5361, (E) STATE 148514', 2007)
    [u'07STATE71143', u'07STATE73601', u'07STATE72896', u'07BEIJING5361', u'07STATE148514']
    >>> # <http://213.251.145.96/cable/2008/05/08MANAGUA573.html>
    >>> parse_references('\\nREF: A. MANAGUA 520 \\nB. MANAGUA 500 \\nC. MANAGUA 443 \\nD. MANAGUA 340 \\nE. MANAGUA 325 \\nF. MANAGUA 289 \\nG. MANAGUA 263 \\nH. MANAGUA 130 \\nI. 2007 MANAGUA 2135 \\nJ. 2007 MANAGUA 1730 \\nK. 2007 MANAGUA 964 \\nL. 2006 MANAGUA 2611 ', 2008)
    [u'08MANAGUA520', u'08MANAGUA500', u'08MANAGUA443', u'08MANAGUA340', u'08MANAGUA325', u'08MANAGUA289', u'08MANAGUA263', u'08MANAGUA130', u'07MANAGUA2135', u'07MANAGUA1730', u'07MANAGUA964', u'06MANAGUA2611']
    >>> # 66BUENOSAIRES2481
    >>> parse_references('\\n REF: STATE 106206 CIRCULAR; STATE CA-3400 NOV 2, 1966 ', 1966)
    [u'66STATE106206']
    >>> #04MADRID4063
    >>> parse_references('\\nREF: EMBASSY MADRID E-MAIL TO EUR/WE OF OCTOBER 14\\n', 2004)
    []
    >>> #08RIYADH1134
    >>> parse_references('\\nREF: A. SECSTATE 74879 \\n     B. RIYADH 43 \\n', 2008)
    [u'08STATE74879', u'08RIYADH43']
    >>> #08RIODEJANEIRO165
    >>> parse_references('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\\n\\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ', 2008)
    [u'08RIODEJANEIRO138', u'08RIODEJANEIRO44']
    >>> parse_references('\\nREF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008)
    [u'08STATE54183', u'07BRASILIA1868', u'08STATE57700', u'07STATE17940']
    >>> # 08BRASILIA806
    >>> parse_references('\\nPROGRAM REF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008)
    [u'08STATE54183', u'07BRASILIA1868', u'08STATE57700', u'07STATE17940']
    >>> # 06SAOPAULO276
    >>> parse_references('\\nCARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA REF: (A) 05 SAO PAULO 405; (B) 05 SAO PAULO 402 (C) 02 BRASILIA 2670', 2006)
    [u'05SAOPAULO405', u'05SAOPAULO402', u'02BRASILIA2670']
    >>> # 08BERLIN1387
    >>> parse_references('\\nREF: A. BERLIN 1045\\nB. SECDEF MSG DTG 301601z SEP 08', 2008)
    [u'08BERLIN1045']
    >>> #09NAIROBI1938
    >>> parse_references('\\nREF: A. 08 STATE 81854\\n\\n\\nS e c r e t nairobi 001938', 2009)
    [u'08STATE81854']
    """
    def format_year(y):
        y = str(y)
        if not y:
            y = str(year)
        if len(y) > 2:
            return y[2:]
        return y
    m_start = _REF_START_PATTERN.search(content)
    m_classified = _CLASSIFIED_BY_PATTERN.search(content, m_start and m_start.end() or 0, 1200)
    last_end = m_start and m_start.end() or 0
    max_idx = m_classified and m_classified.start() or 1200
    m_end = _REF_LAST_REF_PATTERN.search(content, last_end, max_idx)
    while m_end:
        last_end = m_end.end()
        m_end = _REF_LAST_REF_PATTERN.search(content, last_end, max_idx)
    res = []
    if m_end and not m_start:
        raise Exception('Found ref end but no start in "%s"' % content)
    if m_start and last_end:
        start = m_start.start(1)
        end = last_end or m_start.end()
        refs = content[start:end].replace('\n', ' ')
        for y, origin, sn in _REF_PATTERN.findall(refs):
            y = format_year(y)
            origin = origin.replace(' ', '').upper()
            if origin in ('RIO', 'RIODEJAN'):
                origin = 'RIODEJANEIRO'
            elif origin == 'SECSTATE':
                origin = 'STATE'
            elif origin in ('SECDEFMSGDTG', 'ZSEP', # 08BERLIN1387
                            'MTCRPOC', #08STATE15220
                            ): 
                continue
            l = len(origin)
            if (l < MIN_ORIGIN_LENGTH or l > MAX_ORIGIN_LENGTH):
                continue
            for month in _MONTHS:
                if month in origin:
                    origin = None
                    break
            if origin \
                and not 'MAIL' in origin \
                and not 'DAILYREPORT' in origin \
                and not 'REASON' in origin \
                and not origin.startswith('OSC') \
                and not origin.startswith('POLITICAL') \
                and not origin.startswith('PARISPOINTS'):
                res.append(u'%s%s%s' % (y, origin, int(sn)))
    return res


_TAGS_PATTERN = re.compile(r'(?:TAGS?:?\s*)(.+)', re.IGNORECASE|re.UNICODE)
_TAGS_CONT_PATTERN = re.compile(r'(?:\n)([a-zA-Z_-]+.+)', re.MULTILINE|re.UNICODE)
_TAGS_CONT_NEXT_LINE_PATTERN = re.compile(r'\n[ ]*[A-Za-z_-]+[ ]*,')
_TAG_PATTERN = re.compile(r'(COUNTER[ ]+TERRORISM)|(CLINTON[ ]+HILLARY)|(STEINBERG[ ]+JAMES)|(BIDEN[ ]+JOSEPH)|(RICE[ ]+CONDOLEEZZA)|([A-Za-z_-]+)|(\([^\)]+\))|(?:,[ ]+)([A-Za-z_-]+[ ][A-Za-z_-]+)', re.UNICODE)

def parse_tags(content, reference_id=None, ignore_errors=False):
    """\
    Returns the TAGS of a cable.
    
    Acc. to the U.S. SD every cable needs at least one tag.
    
    >>> parse_tags('TAGS: something')
    [u'SOMETHING']
    >>> parse_tags('TAGS: something\\n')
    [u'SOMETHING']
    >>> parse_tags('TAGS: something\\nhere')
    [u'SOMETHING']
    >>> parse_tags('TAGS: something, \\nhere')
    [u'SOMETHING', u'HERE']
    >>> parse_tags(u'TAGS: something,\\nhere')
    [u'SOMETHING', u'HERE']
    >>> parse_tags(u'TAGS something')
    [u'SOMETHING']
    >>> parse_tags(u'TAGS something\\n')
    [u'SOMETHING']
    >>> parse_tags(u'TAGS something\\nhere')
    [u'SOMETHING']
    >>> parse_tags(u'TAGS something, \\nhere')
    [u'SOMETHING', u'HERE']
    >>> parse_tags(u'tAgs something')
    [u'SOMETHING']
    >>> parse_tags('tAgs something\\n')
    [u'SOMETHING']
    >>> parse_tags(u'tAgs something\\nhere')
    [u'SOMETHING']
    >>> parse_tags(u'tAgs something, \\nhere')
    [u'SOMETHING', u'HERE']
    >>> parse_tags(u'tAgs something,\\nhere')
    [u'SOMETHING', u'HERE']
    >>> parse_tags(u'tAgs: something')
    [u'SOMETHING']
    >>> parse_tags(u'tAgs: something\\n')
    [u'SOMETHING']
    >>> parse_tags(u'tAgs: something\\nhere')
    [u'SOMETHING']
    >>> parse_tags(u'tAgs: something, \\nhere')
    [u'SOMETHING', u'HERE']
    >>> parse_tags(u'tAgs: something,\\nhere')
    [u'SOMETHING', u'HERE']
    >>> parse_tags(u'TAGS: PREL ECON EFIN ELAB PGOV FR')
    [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']
    >>> parse_tags(u'TAGS PREL ECON EFIN ELAB PGOV FR')
    [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']
    >>> parse_tags(u'tags PREL ECON EFIN ELAB PGOV FR')
    [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']
    >>> parse_tags(u'tags: PREL ECON EFIN ELAB PGOV FR')
    [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']
    >>> parse_tags(u'TAGS ECON, PGOV, EFIN, MOPS, PINR, UK')
    [u'ECON', u'PGOV', u'EFIN', u'MOPS', u'PINR', u'UK']
    >>> parse_tags(u'TAG PTER, PGOV, ASEC, EFIN, ENRG, KCIP')
    [u'PTER', u'PGOV', u'ASEC', u'EFIN', u'ENRG', u'KCIP']
    >>> parse_tags(u'E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu \\nSubject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?\\n\\n(U) Classifi')
    [u'PREL', u'PGOV', u'PINS', u'TU']
    >>> parse_tags(u"E.o. 12958: decl: after korean unification\\nTags: ovip (steinberg, james b.), prel, parm, pgov, econ,\\netra, mnuc, marr, ch, jp, kn, ks, ir\\nSubject: deputy secretary steinberg's meeting with xxxxx\\nforeign minister he yafei, september 29, 2009")
    [u'OVIP', u'STEINBERG, JAMES B.', u'PREL', u'PARM', u'PGOV', u'ECON', u'ETRA', u'MNUC', u'MARR', u'CH', u'JP', u'KN', u'KS', u'IR']
    >>> parse_tags('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\\n\\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ')
    [u'ECON', u'EINV', u'ENRG', u'PGOV', u'PBTS', u'MARR', u'BR']
    >>> #02ROME1196
    >>> parse_tags('\\nEO 12958 DECL: 03/05/2007\\nTAGS PHUM, OPRC, OPRC, OPRC, OPRC, IT, ITPHUM, ITPHUM, ITPHUM, HUMAN RIGHTS\\nSUBJECT: AS PREDICTED, ITALY’S HUMAN RIGHTS REPORT\\nGENERATES FODDER FOR DOMESTIC POLITICAL MILLS')
    [u'PHUM', u'OPRC', u'IT', u'ITPHUM', u'HUMAN RIGHTS']
    >>> # 09STATE11937
    >>> parse_tags('E.O. 12958: DECL: 02/05/2019\\nTAGS: OVIP CLINTON HILLARY PREL KPAL FR IR RS\\nNATO, UK, CN\\nSUBJECT: (U) Secreta')
    [u'OVIP', u'CLINTON, HILLARY', u'PREL', u'KPAL', u'FR', u'IR', u'RS', u'NATO', u'UK', u'CN']
    >>> #09BEIJING2964
    >>> parse_tags('TAGS: OVIP STEINBERG JAMES PREL MNUC SN CH KN')
    [u'OVIP', u'STEINBERG, JAMES B.', u'PREL', u'MNUC', u'SN', u'CH', u'KN']
    >>> # 09SANTIAGO331
    >>> parse_tags("E.O. 12958: DECL: 04/07/2019\\nTAGS: OVIP BIDEN JOSEPH PREL ECON PGOV SOCI EU\\nSUBJECT: VICE PRESIDENT BIDEN'S MARCH 28 MEETING WITH PRIME")
    [u'OVIP', u'BIDEN, JOSEPH', u'PREL', u'ECON', u'PGOV', u'SOCI', u'EU']
    >>> #08STATE100219
    >>> parse_tags('E.O. 12958: DECL: 09/17/2018\\nTAGS: OVIP RICE CONDOLEEZZA PREL PHSA SP KV CU\\nBL, IS\\nSUBJECT: Secretary Rice')
    [u'OVIP', u'RICE, CONDOLEEZZA', u'PREL', u'PHSA', u'SP', u'KV', u'CU', u'BL', u'IS']
    >>> # 04SANAA2346
    >>> parse_tags('TAGS: MASS MOPS OVIP PARM PINR PREL PTER YM COUNTER TERRORISM')
    [u'MASS', u'MOPS', u'OVIP', u'PARM', u'PINR', u'PREL', u'PTER', u'YM', u'COUNTERTERRORISM']
    >>> # 05TELAVIV1580
    >>> parse_tags('TAGS PGOV, PREL, KWBG, IR, IS, COUNTERTERRORISM, GOI EXTERNAL ')
    [u'PGOV', u'PREL', u'KWBG', u'IR', u'IS', u'COUNTERTERRORISM', u'GOI EXTERNAL']
    >>> parse_tags('TAGS PTER MARR, MOPPS')
    [u'PTER', u'MARR', u'MOPS']
    """
    m = _TAGS_PATTERN.search(content)
    if not m:
        if reference_id in _CABLES_WITHOUT_TAGS:
            return []
        msg = 'No TAGS found in cable ID "%r", content: "%s"' % (reference_id, content)
        if ignore_errors:
            logging.warn(msg)
            return []
        else:
            raise Exception(msg)
    tags = m.group(1)
    m2 = None
    if tags.endswith(',') or tags.endswith(', ') or _TAGS_CONT_NEXT_LINE_PATTERN.match(content, m.end(), 1200):
        m2 = _TAGS_CONT_PATTERN.match(content, m.end())
    if m2:
        tags = ' '.join([tags, m2.group(1)])
    res = []
    for t in _TAG_PATTERN.findall(tags):
        tag = ''.join(t).upper().replace(u')', u'').replace(u'(', u'')
        if tag == 'CLINTON HILLARY':
            tag = u'CLINTON, HILLARY'
        elif tag == 'STEINBERG JAMES':
            tag = u'STEINBERG, JAMES B.'
        elif tag == 'BIDEN JOSEPH':
            tag = u'BIDEN, JOSEPH'
        elif tag == 'RICE CONDOLEEZZA':
            tag = u'RICE, CONDOLEEZZA'
        elif tag == 'COUNTER TERRORISM':
            tag = u'COUNTERTERRORISM'
        elif tag == 'PTER MARR': # 07BAKU855
            res.extend(tag.split())
            continue
        elif tag == 'MOPPS': # 09BEIRUT818
            tag = u'MOPS'
        elif tag == 'POGOV': # 09LONDON2222
            tag = u'PGOV'
        elif tag == u'RU': # 09BERLIN1433, 09RIYADH181 etc.
            tag = u'RS'
        elif tag == u'SYR':
            tag = u'SY'
        if tag not in res:
            res.append(tag)
    return res


_END_SUMMARY_PATTERN = re.compile(r'END[ ]+SUMMARY', re.IGNORECASE)
_START_SUMMARY_PATTERN = re.compile(r'(SUMMARY( AND COMMENT)?[ \-\n:\.]*)|(\n1\.[ ]+(\([^\)]+\))?([ ]+summary( and comment)?(:|\.))?)', re.IGNORECASE)
_SUMMARY_PATTERN = re.compile(r'(?:SUMMARY[ \-\n]*)(?::|\.|\s)(.+?)(?=(\n[ ]*\n)|(END[ ]+SUMMARY))', re.DOTALL|re.IGNORECASE|re.UNICODE)
_CLEAN_SUMMARY_WS_PATTERN = re.compile('[ \n]+')
_CLEAN_SUMMARY_PATTERN = re.compile(r'(---+)|(((^[1-9])|(\n[1-9]))\.[ ]+\([^\)]+\)[ ]+)|(^[1-2]. Summary:)|(^[1-2]\.[ ]+)|(^and action request. )|(^and comment. )|(2. (C) Summary, continued:)', re.UNICODE|re.IGNORECASE)

def parse_summary(content, reference_id=None):
    """\
    Extracts the summary from the `content` of the cable.
    
    >>> # 72TEHRAN5055
    >>> parse_summary('REF: TEHRAN 4887\\n\\nSUMMARY: FOLLOWING ASSASSINATION [...].\\nEND SUMMARY\\n\\n1. IN WAKE ')
    u'FOLLOWING ASSASSINATION [...].'
    >>> # 09BERLIN1197
    >>> parse_summary('''Classified By: AMBASSADOR PHILIP D. MURPHY FOR REASONS 1.4 (B) and (D)\\n\\nSUMMARY\\n-------\\n\\n1. (C) Chancellor Merkel [...].\\nEnd Summary.\\n\\nOVERALL TREND: MAJOR PARTIES IN DECLINE''')
    u'Chancellor Merkel [...].'
    >>> # 09HAVANA35
    >>> parse_summary('''Classified By: COM Jonathan Farrar for reasons 1.4 (b) and (d)\\n\\n1. (C) SUMMARY: Fidel Castro's [...].\\n \\nWHAT WE KNO''')
    u"Fidel Castro's [...]."
    >>> # 07SAOPAULO464
    >>> parse_summary('''------- SUMMARY -------\\n\\n1. Pope Benedict XVI's four-day [...] End Summary''')
    u"Pope Benedict XVI\'s four-day [...]"
    >>> # 07SAOPAULO250
    >>> parse_summary('''------- SUMMARY -------\\n\\n1. Summary: On March 21, Pope Benedict XVI [...] End Summary. ''')
    u'On March 21, Pope Benedict XVI [...]'
    >>> # 09BERLIN1176
    >>> parse_summary('''SUMMARY\\n-------\\n\\n1. (C/NF) This is not a "change" election. [...]. END SUMMARY. ''')
    u'This is not a "change" election. [...].'
    >>> # 09BRASILIA1300
    >>> parse_summary('''1. (U) Paragraphs 2 and 8 contain Mission Brazil action request.\\n\\n2. (C) Summary and Action Request. With Iranian President [...]. End Summary and Action Request. ''')
    u'With Iranian President [...].'
    >>> # 09BRASILIA1368
    >>> parse_summary('''Summary -------\\n\\n2. (C) President Lula welcomed [...] End Summary''')
    u'President Lula welcomed [...]'
    >>> # 05PARIS7682
    >>> parse_summary('1. (C) Summary and Comment: Continuing violent unrest in[...]. End Summary and Comment. ')
    u'Continuing violent unrest in[...].'
    >>> # 09BERLIN1548
    >>> parse_summary('''1. (C/NF) Summary: In separate December 1 meetings [...] following way forward:\\n\\n-- the Interior Ministry [...]\\n\\nrelationship with Chancellor Merkel. End summary''')
    u'In separate December 1 meetings [...] following way forward: -- the Interior Ministry [...] relationship with Chancellor Merkel.'
    >>> # 10BERLIN164
    >>> parse_summary('''Classified By: Classified by Political M-C George Glass for reasons 1.4\\n(b,d).\\n\\n1. (C) German FM Westerwelle told [...]. END SUMMARY.''')
    u'German FM Westerwelle told [...].'
    >>> # 09BRUSSELS536
    >>> parse_summary('''Classified By: USEU EconMinCouns Peter Chase for reasons 1.4 (b), (d), (e).\\n\\n1. (S//NF) SUMMARY AND COMMENT: During a March 2-3 visit to\\n\\n2. (C) EU Member States and officials uniformly praised the\\n\\n3. (C) The content[...]. END SUMMARY AND COMMENT. ''')
    u'During a March 2-3 visit to EU Member States and officials uniformly praised the The content[...].'
    >>> # 10BRASILIA61
    >>> parse_summary('''CLASSIFIED BY: Thomas A. Shannon, Ambassador, State, Embassy Brasilia; REASON: 1.4(B), (D)\\n1. (C) Summary. During separate [...]. End summary.''')
    u'During separate [...].'
    """
    summary = None
    m = _END_SUMMARY_PATTERN.search(content)
    if m:
        end_of_summary = m.start()
        m = _START_SUMMARY_PATTERN.search(content, 0, end_of_summary)
        if m:
            summary = content[m.end():end_of_summary]
        else:
            raise Exception('Found "end of summary" but no start in "%s", content: "%s"' % (reference_id, content[:end_of_summary]))
    else:
        m = _SUMMARY_PATTERN.search(content)
        if m:
            summary = content[m.start(1):m.end(1)]
    if summary:
        summary = _CLEAN_SUMMARY_PATTERN.sub(u' ', summary)
        summary = _CLEAN_SUMMARY_WS_PATTERN.sub(u' ', summary)
        summary = summary.strip()
    return summary


if __name__ == '__main__':
    import doctest
    doctest.testmod()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
This module extracts information from cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import absolute_import
import os
import re
import logging
from cablemap.core import consts as consts, c14n
from cablemap.core.consts import REFERENCE_ID_PATTERN, MALFORMED_CABLE_IDS, INVALID_CABLE_IDS

logger = logging.getLogger('cablemap.core.reader')

# Indicates the max. index where the reader tries to detect the subject/TAGS/references
_MAX_HEADER_IDX = 1200

#
# Cables w/o tags
#
_CABLES_WITHOUT_TAGS = (
    '06KABUL3934', '08BEIJING3662', '09ROME878', '09ROME1048', '08ROME451',
    '08ROME525', '04QUITO2502', '04QUITO2879', '05PANAMA1589', '06KABUL5653',
    '07PANAMA400', '07PANAMA946', '01CAIRO5770', '08BRASILIA703', '10ASTANA267',
    )

_CABLES_WITHOUT_TO = (
    '08MONTERREY468', '09TIJUANA1116', '08STATE125686', '06WELLINGTON633',
    '06WELLINGTON652', '08STATE34306', '07SAOPAULO161', '08BRASILIA454',
    '09PHNOMPENH437',
    )

_CABLES_WITH_MALFORMED_SUMMARY = (
    '09CAIRO2133', '06BUENOSAIRES2711', '08BUENOSAIRES1305', '07ATHENS2386',
    '09SOFIA716', '09BUCHAREST354',
    )

_CABLE_ID_SUBJECT_PATTERN = re.compile('^([0-9]+[^:]+):\s(.+)$')

_CABLE_FIXES = {
    '08MANAMA492': # (08ECTION01OF02MANAMA492)
        (r'TORUEHC/SECSTATE', u'TO RUEHC/SECSTATE'),
    '08ECTION01OF02MANAMA492':
        (r'TORUEHC/SECSTATE', u'TO RUEHC/SECSTATE'),
    '08TRIPOLI402':
        (ur'JAMAHIRIYA-STYLE\s+Q: A\) TRIPOLI', u'JAMAHIRIYA-STYLE \nREF: A) TRIPOLI'),
    '07HAVANA252':
        (ur'XXXNEED A MILLION', u'XXX NEED A MILLION'),
    '09BEIJING1176':
        (ur'XXXDISCUSSES', u'XXX DISCUSSES'),
    '09BEIJING2438':
        (ur'NEGOTIATE SE\s+CRETLY', u'NEGOTIATE SECRETLY'),
    '09STATE30049':
        (ur'Secretary Clinton’s March 24, 2009 \n\n', u'Secretary Clinton’s March 24, 2009 \n'),
    '09CAIRO544': # This cable contains a proper SUBJECT: line in some releases and in some not.
        (ur'\nBLOGGERS MOVING', u'\nSUBJECT: BLOGGERS MOVING'),
    '09CAIRO211':
        (r'''EG\nEGYPT'S 54''', u'''EG\nSUBJECT: EGYPT'S 54'''),
    '09CAIRO1468':
        (r'EG\nXXXXXXXXXXXX:', u'EG\nSUBJECT: XXXXXXXXXXXX:'),
    '09BAKU687':
        (ur'IR\nClassified By:', u'''IR
SUBJECT: IRAN: NINJA BLACK BELT MASTER DETAILS USE OF
MARTIAL ARTS CLUBS FOR REPRESSION; xxxxxxxxxxxx

REF: a) BAKU 575

Classified By:'''),
    '08KYIV2414':
        (ur'UP[ ]*\n1.', u'''UP
SUBJECT: UKRAINE: FIRTASH MAKES HIS CASE TO THE USG
REF: A. KYIV 2383 B. KYIV 2294

1.
'''),
    '09CAIRO79':
        (ur'EG\n\nClassified', u"""
SUBJECT: GOE STRUGGLING TO ADDRESS POLICE BRUTALITY

REF: A. 08 CAIRO 2431
B. 08 CAIRO 2430
C. 08 CAIRO 2260
D. 08 CAIRO 783
E. 07 CAIRO 3214
F. 07 CAIRO 2845
"""),
    '09TRIPOLI63':
        ('''LY

CLASSIFIED BY:''', u'''LY

SUBJECT: RISKY BUSINESS? AMERICAN CONSTRUCTION FIRM ENTERS JOINT VENTURE WITH GOL [8466936]

CLASSIFIED BY:'''),
    '06LIMA1452': ('''PE
RUN-OFF''', '''PE
SUBJECT: RUN-OFF'''),
}

def reference_id_from_filename(filename):
    """\
    Extracts the reference identifier from the provided filename.
    """
    reference_id = os.path.basename(filename)
    if reference_id.rfind('.htm') > 0:
        reference_id = reference_id[:reference_id.rfind('.')]
    #TODO: else: raise ValueError('bla bla')?
    return reference_id

_C14N_FIXES = {
    u'ATLANTA': u'CDCATLANTAGA',
    u'ATLANGAGA': u'CDCATLANTAGA',
    u'ATLANTAGA': u'CDCATLANTAGA',
    u'CDCATLANTA': u'CDCATLANTAGA',
    u'USUNESCOPARISFR': u'UNESCOPARISFR',
    u'PARISFR': u'UNESCOPARISFR',
    u'UNVIE': u'UNVIEVIENNA',
    u'STAT': u'STATE',
    u'SECSTATE': u'STATE',
    u'SECTSTATE': u'STATE',
    u'SECTATE': u'STATE',
    u'SECDEFWASH': u'SECDEF',
    u'USNATOANDUSNATO': u'USNATO', # 07REYKJAVIK85: REFS: Hodgson emails to Duguid/Pulaski/USNATO and USNATO 00184 
    u'RIO': u'RIODEJANEIRO',
    u'RIODEJAN': u'RIODEJANEIRO',
    u'RIODEJANIERO': u'RIODEJANEIRO',
    u'RIODEJANERIO': u'RIODEJANEIRO',
    u'PORT-OF-SPAIN': u'PORTOFSPAIN',
    u'PAUP': u'PORTAUPRINCE',
    u'PAP': u'PORTAUPRINCE',
    u'PORT-AU-PRINCE': u'PORTAUPRINCE',
    u'SANJSE': u'SANJOSE',
    u'PANANA': u'PANAMA',
    u'PANAM': u'PANAMA',
    u'MADRIDSP': u'MADRID',
    u'BRUSSELS': u'USEUBRUSSELS',
    u'USEU': u'USEUBRUSSELS',
    u'USUN': u'USUNNEWYORK',
    u'USUNNY': u'USUNNEWYORK',
    u'USUNNEYORK': u'USUNNEWYORK',
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
    u'TRIPOLII': u'TRIPOLI',
    u'BRASILA': u'BRASILIA',
    u'BRAZIL': u'BRASILIA',
    u'BRASIIA': u'BRASILIA',
    u'BRAZILIA': u'BRASILIA',
    u'BRASIILIA': u'BRASILIA',
    u'MEXICOCITY': u'MEXICO',
    u'BA': u'BUENOSAIRES',
    u'BUENSOAIRES': u'BUENOSAIRES',
    u'BUENOSAIREDS': u'BUENOSAIRES',
    u'USDA': u'USDAFAS',
    u'CDCATLANTAGA': u'CDCATLANTA',
    u'USDOCWASHDC': u'USDOC',
    u'USCUSTOMSA': u'USCBP',
    u'BEIJINJG': u'BEIJING',
    u'BEIJINGCH': u'BEIJING',
    u'MANAUGUA': u'MANAGUA',
    u'MANAUGA': u'MANAGUA',
    u'TGG': u'TEGUCIGALPA',
    u'QUEBECCITY': u'QUEBEC',
    u'ASUN': u'ASUNCION',
    u'BASRA': u'BASRAH',
    u'TALLIN': u'TALLINN',
    u'SDO': u'SANTODOMINGO',
    u'TTAWA': u'OTTAWA',
    u'DELHI': u'NEWDELHI',
    u'HCMCI': u'HOCHIMINHCITY',
    u'AITTAIPEI': u'TAIPEI',
              
}
_C14N_PATTERN = re.compile(r'[0-9]{2}(%s)[0-9]+' % '|'.join(_C14N_FIXES.keys()))

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
    if u'EMBASSY' in reference_id:
        return reference_id.replace(u'EMBASSY', u'')
    m = _C14N_PATTERN.match(reference_id)
    if m:
        origin = m.group(1)
        return reference_id.replace(origin, _C14N_FIXES[origin])
    return MALFORMED_CABLE_IDS.get(reference_id, INVALID_CABLE_IDS.get(reference_id, reference_id))

_REFERENCE_ID_FROM_HTML_PATTERN = re.compile('<h3>Viewing cable ([0-9]{2,}[A-Z0-9]+),', re.UNICODE)

def reference_id_from_html(html):
    """\
    Extracts the cable's reference identifier from the provided HTML string.

    `html`
        The HTML page of the cable.
    """
    m = _REFERENCE_ID_FROM_HTML_PATTERN.search(html)
    if m:
        return m.group(1)
    raise ValueError("Cannot extract the cable's reference id")


def fix_content(content, reference_id):
    """\
    Fixes some oddities of cables.

    Some cables contain malformed content which is normalized here.

    This function assumes that &#x000A; has been replaced by ``\n``,
    and pilcrows, HTML links etc. have been removed (see `_clean_html`)

    The (un)changed content is returned.

    `content`
        The text content of the cable
    `reference_id`
        The reference identifier of the cable.


    >>> fix_content('\\nBLOGGERS MOVING', '09CAIRO544')
    u'\\nSUBJECT: BLOGGERS MOVING'
    >>> fix_content('\\nBLOGGERS MOVING', '09UNKNOWNID3122')
    '\\nBLOGGERS MOVING'
    """
    if reference_id in _CABLE_FIXES:
        pattern, repl = _CABLE_FIXES.get(reference_id)
        content = re.sub(pattern, repl, content)
    return content

_CONTENT_PATTERN = re.compile(ur'(?:<code><pre>)(.+?)(?:</pre></code>)', re.DOTALL|re.UNICODE)

def get_content_as_text(file_content, reference_id):
    """\
    Returns the cable content as text.

    This function removes HTML links etc. (c.f. `_clean_html`) and repairs
    the content of the cable if necessary (c.f. `fix_content`).
    
    `file_content`
        The HTML file content, c.f. `get_file_content`.
    `reference_id`
        The reference identifier of the cable.
    """
    return fix_content(_clean_html(_CONTENT_PATTERN.findall(file_content)[-1]), reference_id)


def get_header_as_text(file_content, reference_id):
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
        raise ValueError('Unexpected <code><pre> sections: "%r"' % res)
    return fix_content(_clean_html(content), reference_id)


_LINK_PATTERN = re.compile(ur'<a[^>]*>', re.UNICODE)
_HTML_TAG_PATTERN = re.compile(r'</?[a-zA-Z]+>')
_BACKSLASH_PATTERN = re.compile(r'\\[ ]*\n|\\[ ]*$')

def _clean_html(html):
    """\
    Removes links (``<a href="...">...</a>``) from the provided HTML input.
    Further, it replaces "&#x000A;" with ``\n`` and removes "¶" from the texts.
    """
    content = html.replace(u'&#x000A;', u'\n').replace(u'¶', '')
    content = _LINK_PATTERN.sub(u'', content)
    content = _HTML_TAG_PATTERN.sub(u'', content)
    content = _BACKSLASH_PATTERN.sub(u'\n', content)
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

    while the message begins usually with a summary

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


_META_PATTERN = re.compile(r'''<table.*?class.+?["']cable["']\s*>.+?<a[^>]+>(.+?)</a>.+<td>\s*<a.+?>(.+?)</a>.+<td>\s*<a.+?>(.+?)</a>.+<td>\s*<a.+?>(.+?)</a>''', re.MULTILINE|re.DOTALL)
_MEDIA_URLS_PATTERN = re.compile(r'''<a href=(?:"|')(https?://[^\.]+\.[^"']+)''')

def parse_meta(file_content, cable):
    """\
    Extracts the reference id, date/time of creation, the classification,
    and the origin of the cable and assigns the value to the provided `cable`.
    """
    end_idx = file_content.rindex("</table>")
    start_idx = file_content.rindex("<table class='cable'>", 0, end_idx)
    m = _META_PATTERN.search(file_content, start_idx, end_idx)
    if not m:
        raise ValueError('Cable table not found')
    if len(m.groups()) != 4:
        raise ValueError('Unexpected metadata result: "%r"' % m.groups())
    # Table content: 
    # Reference ID | Created | Classification | Origin
    ref, created, classification, origin = m.groups()
    if cable.reference_id != ref:
        reference_id = MALFORMED_CABLE_IDS.get(ref)
        if reference_id != cable.reference_id:
            reference_id = INVALID_CABLE_IDS.get(ref)
            if reference_id != cable.reference_id:
                raise ValueError('cable.reference_id != ref. reference_id="%s", ref="%s"' % (cable.reference_id, ref))
    cable.created = created
    cable.origin = origin
    # classifications are usually written in upper case, but you never know.. 
    cable.classification = classification.upper()
    # Try to find media IRIs
    start_idx = file_content.rfind(u'Appears in these', start_idx, end_idx)
    if start_idx > 0:
        cable.media_uris = _MEDIA_URLS_PATTERN.findall(file_content, start_idx, end_idx)
    return cable


_TID_PATTERN = re.compile(r'(VZCZ[A-Z]+[0-9]+)', re.UNICODE)

def parse_transmission_id(header, reference_id=None):
    """\
    Returns the transmission ID of the cable. If no transmission identifier was
    found, ``None`` is returned.

    `header`
        The cable's header
    `reference_id`
        The cable's reference ID.
    """
    m = _TID_PATTERN.search(header)
    if not m:
        return None
    return m.group(1)


_REC_PATTERN = re.compile(r'(?:([A-Z]+)/)?([A-Z0-9].+)', re.UNICODE)
_REC_CLEAN_PATTERN = re.compile(r'(PAGE [0-9]+\s+[A-Z]+\s+[0-9]+\s+[0-9]+Z)')
_REC_PRECEDENCE_PATTERN = re.compile(r'FLASH|NIACT IMMEDIATE|IMMEDIATE|PR?IORITY|ROUTINE')
_REC_MCN_PATTERN = re.compile(r'(?:[ ]+)([0-9]{4,})$')

def _route_recipient_from_header(header, reference_id):
    from cablemap.core.models import Recipient
    header = _REC_CLEAN_PATTERN.sub(u'', header)
    res = []
    for route, recipient in _REC_PATTERN.findall(header):
        excluded = []
        mcn = None
        precedence = None
        m = _REC_MCN_PATTERN.search(recipient)
        if m:
            mcn = m.group(1)
            recipient = recipient[:m.start()].strip()
        m = _REC_PRECEDENCE_PATTERN.search(recipient)
        if m:
            precedence = m.group().replace(u'PIOR', u'PRIOR')
            recipient = recipient[:m.start()]
        if recipient.startswith('XMT'):
            #TODO: FHM says: "[...] follow the collective address with a comma, space, "XMT," and
            # the name(s) of the posts in the collective that will not receive the
            # telegram. [...]"
            # But some cables like "07PHNOMPENH1341" use XMT as address
            # Further, some cables like "09STATE63860" use:
            # XMT AMCONSUL JOHANNESBURG
            # AMCONSUL JOHANNESBURG
            continue
        res.append(Recipient(route, recipient.strip(), precedence, mcn, excluded))
    return res


_TO_PATTERN = re.compile(r'(?:\nTO\s+)(.+?)(?=INFO|\Z)', re.DOTALL|re.UNICODE)

def parse_recipients(header, reference_id=None):
    """\
    Returns the recipients of the cable as (maybe empty) list.
    """
    m = _TO_PATTERN.search(header)
    if not m:
        if reference_id and reference_id not in _CABLES_WITHOUT_TO:
            logger.warn('No TO header found in "%s", header: "%s"' % (reference_id, header))
        return []
    to_header = m.group(1)
    return _route_recipient_from_header(to_header, reference_id)


_INFO_PATTERN = re.compile(r'(?:.*?INFO\s+)(.+?)(?=\Z)', re.DOTALL|re.UNICODE)

def parse_info_recipients(header, reference_id=None):
    """\
    Returns the informal recipients of the cable as (maybe empty) list.    
    """
    m = _INFO_PATTERN.search(header)
    if not m:
        return []
    to_header = m.group(1)
    return _route_recipient_from_header(to_header, reference_id)

_CLIST_CONTENT_PATTERN = re.compile(r'''Classified\s+By:?\s*[0-9\.\s]*
        (?:(?:\s*\([A-Z]\))?\s*Classified\s+by:?\s*)?
        (?:\s*\([A-Z]\)\s*)?
        (?:[A-Z]+/[A-Z]+(?:\s*\-\s*)?)?
        (?:
         [A-Z\-/\s\\'\.]+(?:,?\s*A\.?\s*I\.,?|Leader|AT\-LARGE|Pakistan|A/S|M[\-/]?C|\??Aff(?:ai|ia)re?\s*s|Charge?|Secretary(?:\s+of\s+State)?|Mission|General|Couns(?:ell?(?:o|0)u?r)?|Coordinator|Col(?:onel)?|Poloff|Amb\.?(?:assa?dor)?|Advisor|Dir(?:ector)?|Representative|Chief|Head|Consul|Section|Major|Pdas|Ltc|Adviser|Attache|Officer|Ipao|DCM|CDA|Das)\s+
         |Econ(?:omic|couns)?
         |POL(?:ITICAL|couns|OFF)?\s*(?:[/-](?:ECON|MIL))?\s*
         |Section|Charge?|Cons(?:ul)?|Min(?:ister)?
         |Amb\.?(?:assador)?(?:\s+to\s+[A-Z]+)?
         |(?:A/?)?DCM|CDA|INR|ISN
         )?
         \.?\s*
         (.+?)
        (?=(?:F\s*O\s*R\s+|per\s+)?(?:R\s*E\s*A\s*S?\s*ON?|E\.O\.|1\.[45]|1\.\s*\(|CONFIDENTIAL|Summary))''',
    re.IGNORECASE|re.UNICODE|re.DOTALL|re.VERBOSE)
_CLSIST_PATTERN = re.compile(r"[\s\.,]*([A-Z][^,;]+(?:\s*,\s*(?:JR\.?|II+))?)\s*", re.IGNORECASE|re.UNICODE)

def parse_classificationists(content, normalize=True):
    """\
    Returns the classificationist or ``None`` if the classificationist
    cannot be extracted.

    `content`
        The cable's content.
    """
    names = []
    m = _CLIST_CONTENT_PATTERN.search(content)
    if not m:
        return ()
    m = _CLSIST_PATTERN.search(m.group(1))
    if not m:
        return ()
    name = m.group(1).replace(u'\n', ' ')
    name = re.sub('[ ]+', ' ', name).rstrip(' -:').strip().replace(u'Y ee', u'Yee')
    if not name.upper().endswith(u'JR.'):
        name = name.rstrip(u'.')
    if normalize:
        name = name.replace(u'0', u'O').title()
        # Convert something like "Donald Duck, Iii" into "Donald Duck, III"
        names.append(re.sub(r'(Ii+)', lambda m: m.group(1).upper(), name))
    return names


_SIGNER_PATTERN = re.compile(r'(?:[\-\?\"/]|\)(?!\s+END)'
                             r'|\.(?!\s+The\b)'
                             r'|[\sA-Z]*QUOTE)(?:\s+[GP\-3EXEMPT]+'
                             r'|[\sA-Z]+QUOTE)?\s+([A-Z]+[ \-\']?[A-Z]+)\b\.?#*[ ]*\s*(?:LIMITED |NN+|Declassified/Released|NOTE(?:[ ]+BY|:[ ]+)|SECRET|UNCLASSIFIED|CONFIDENTIAL|\Z)', re.IGNORECASE|re.UNICODE)
_SIGNER_PATTERN2 = re.compile(r'[A-Za-z0-9\.][ ]*(?:\n[ ]*)+([A-Z]+\-?[A-Z]+(?:[ ]*[\r\n][A-Z]+\-?[A-Z]+)?)[\s\.]*\Z', re.UNICODE)

def parse_signers(content, canonicalize=True):
    """\
    Returns a maybe empty iterable of signers of the cable.

    `content`
        The cable's content.
    `canonicalize`
        Indicates if the signers should be canonicalized (upper-case the
        string and remove typos) (enabled by default).
    """
    s = content[-300:]
    m = _SIGNER_PATTERN.search(s) or _SIGNER_PATTERN2.search(s)
    if not m:
        return []
    signers = m.group(1)
    tmp_signers = signers.upper()
    if tmp_signers in (u'CONFIDENTIAL', u'UNCLASSIFIED'):
        return []
    if canonicalize:
        tmp_signers = tuple(re.split(ur'\s+', tmp_signers.strip()))
        if tmp_signers == (u'KEEGANPAAL',): # 04TAIPEI3991
            signers = [u'KEEGAN', u'PAAL']
        elif tmp_signers == (u'JOHNSONKEANE',): # 05ASUNCION807
            signers = [u'JOHNSON', u'KEANE']
        elif tmp_signers == (u'STEWARTBALTIMORE',): # 06MUSCAT396
            signers = [u'STEWART', u'BALTIMORE']
        elif tmp_signers == (u'BIGUSBELL',): # 06KIRKUK112
            signers = [u'BIGUS', u'BELL']
        else:
            signers = tmp_signers
    else:
        signers = [signers]
    return [c14n.canonicalize_surname(s) for s in signers] if canonicalize else signers


_SUBJECT_PATTERN = re.compile(ur'(?:^|[ ]+)S?UBJ(?:ECT)?(?:(?::\s*)|(?::?\s+))(?!LINE[/]*)(.+?)(?:\Z|(C O N)|(SENSI?TIVE BUT)|([ ]+REFS?:[ ]+)|(\n[ ]*\n|[\s]*[\n][\s]*[\s]*REFS?:?\s)|(REF:\s)|(REF\(S\):?)|(\s*Classified\s)|([1-9]\.?[ ]+Classified By)|([1-9]\.?[ ]*\([^\)]+\))|((?:1\.?[ ]|\r?\n)Summary)|([A-Z]+\s+[0-9]+\s+[0-9]+\.?[0-9]*\s+OF)|(\-\-\-\-\-*\s+)|(Friday)|(PAGE [0-9]+)|(This is a?n Action Req))', re.DOTALL|re.IGNORECASE|re.UNICODE|re.MULTILINE)
_SUBJECT_MAX_PATTERN = re.compile(r'^1\.?[ ]*(?:\([^\)]+\)|SUMMARY)|SUMMARY|"CANCEL THIS', re.IGNORECASE|re.MULTILINE)
_NL_PATTERN = re.compile(ur'[\r\n]+')
_SLASH_ESCAPE_PATTERN = re.compile(ur'[\\]+')
_WS_PATTERN = re.compile(ur'[ ]{2,}', re.UNICODE)
_BRACES_PATTERN = re.compile(r'^\([^\)]+\)[ ]+| \([A-Z]+\)$')
_HTML_ENTITIES_PATTERN = re.compile(r'&#([0-9]+);')

def parse_subject(content, reference_id=None, clean=True):
    """\
    Parses and returns the subject of a cable. If the cable has no subject, an
    empty string is returned.
    
    `content`
        The cable's content.
    `reference_id`
        The (optional) reference id of the cable. Used for error msgs
    `clean`
        Indicates if classification prefixes like ``(S)`` should be removed from
        the subject (default: ``True``)
        * (TS) for Top Secret
        * (S) for Secret
        * (C) for Confidential
        * (U) for Unclassified
        * (SBU/N) for Sensitive But Unclassified/Noforn, and
        * (SBU) for Sensitive But Unclassified
        Source: 
        U.S. Department of State Foreign Affairs Handbook Volume 5 Handbook 1 — Correspondence Handbook
        5 FAH-1 H-210 -- HOW TO USE TELEGRAMS; page 2
        <http://www.state.gov/documents/organization/89319.pdf>
    """
    def to_unicodechar(match):
        return unichr(int(match.group(1)))
    m = _SUBJECT_MAX_PATTERN.search(content)
    max_idx = m.start() if m else _MAX_HEADER_IDX
    m = _SUBJECT_PATTERN.search(content, 0, max_idx)
    if not m:
        return u''
    res = m.group(1).strip()
    res = _NL_PATTERN.sub(u' ', res)
    res = _WS_PATTERN.sub(u' ', res)
    res = res.replace(u'US- ', u'US-')
    res = _HTML_ENTITIES_PATTERN.sub(to_unicodechar, res)
    if clean:
        res = _WS_PATTERN.sub(u' ', _SLASH_ESCAPE_PATTERN.sub(u'', _BRACES_PATTERN.sub(u'', res))).strip()
    return res


# Commonly month/day/year is used, but sometimes year/month/day
_DEADLINE_PATTERN = re.compile(r'(?:E.?O.?\s*12958:?\s*DECL\s*:?\s*)([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})|([0-9]{4}/[0-9]{2}/[0-9]{2})', re.IGNORECASE|re.UNICODE)

def parse_nondisclosure_deadline(content):
    """\
    Returns the non-disclosure deadline if provided.

    `content`
        The cable's content.
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


# Some cables have an (incomplete) header section within the content, i.e. 07LIMA2129
# This pattern is used to find the "real" REF section
_REF_OFFSET_PATTERN = re.compile('\n\-+ header')
_REF_START_PATTERN = re.compile(r'(?:[\nPROGRAM ]*REF|REF\(S\):?\s*)([^\n]+(\n\s*[0-9]+[,\s]+[^\n]+)?)', re.IGNORECASE|re.UNICODE)
_REF_LAST_REF_PATTERN = re.compile(r'(\n[^\n]*\n)|(\n?[ ]*[A-Z](?:\.(?!O\.|S\.)|\))[^\n]+)', re.IGNORECASE|re.UNICODE)
# "(?:(?:[ ]*REF)?[ ]+[A-Z][ ]+)?" for "10HAVANA9": A. REF A HAVANA 639
_REF_PATTERN = re.compile(r'''([A-Z])?(?:\.|\)|:)?(?:(?:[ ]*REF)?[ ]+[A-Z][ ]+)?\s*\(?([0-9]{2,4})?\)?(?:\s*)([A-Z ]*[A-Z ]*[A-Z\-']{2,})(?:\s+)([0-9]+)(?!\.\.+)(?:\s+\(([0-9]{2,4})\))?''', re.MULTILINE|re.UNICODE|re.IGNORECASE)
_REF_NOT_REF_PATTERN = re.compile(r'\n[0-9]\.[ ]*(?:\([A-Z]+\))?', re.IGNORECASE|re.UNICODE)
_REF_STOP_PATTERN = re.compile('(classified by)|summary|\n1\.?\s*\([SBUC]+\)', re.IGNORECASE|re.UNICODE)
_REF_ORIGIN_PATTERN = re.compile('[0-9]+([A-Z]+)[0-9]+')
#TODO: The following works for all references which contain something like 02ROME1196, check with other cables
_CLEAN_REFS_PATTERN = re.compile(r'(PAGE [0-9]+ [A-Z]+ [0-9]+ [0-9]+ OF [0-9]+ [A-Z0-9]+)|([A-Z]+\s+[0-9]+\s+[0-9]+(?:\.[0-9]+)?\s+OF)', re.UNICODE)

def parse_references(content, year, reference_id=None, canonicalize=True):
    """\
    Returns the references to other cables as (maybe empty) list.
    
    `content`
        The content of the cable.
    `year`
        The year when the cable was created.
    `reference_id`
        The reference identifier of the cable.
    `canonicalize`
        Indicates if the cable reference origin should be canonicalized.
        (enabled by default)
    """
    from cablemap.core.models import Reference
    def format_year(y):
        y = str(y)
        if not y:
            y = str(year)
        if len(y) == 4:
            return y[2:]
        elif len(y) == 3 and y[0] == '0':
            return y[1:]
        return y
    offset = 0
    m_offset = _REF_OFFSET_PATTERN.search(content)
    if m_offset:
        offset = m_offset.end()
    # 1. Try to find "Classified By:"
    m_stop = _REF_STOP_PATTERN.search(content, offset)
    # If found, use it as maximum index to search for references, otherwise use a constant
    max_idx = m_stop and m_stop.start() or _MAX_HEADER_IDX
    # 2. Find references
    m_start = _REF_START_PATTERN.search(content, offset, max_idx)
    # 3. Check if we have a paragraph in the references
    m_stop = _REF_NOT_REF_PATTERN.search(content, m_start and m_start.end() or 0, max_idx)
    last_end = m_start and m_start.end() or 0
    # 4. Find the next max_idx
    max_idx = min(m_stop and m_stop.start() or _MAX_HEADER_IDX, max_idx)
    m_end = _REF_LAST_REF_PATTERN.search(content, last_end, max_idx)
    while m_end:
        last_end = m_end.end()
        m_end = _REF_LAST_REF_PATTERN.search(content, last_end, max_idx)
    res = []
    if m_end and not m_start:
        logger.warn('Found ref end but no start in "%s", content: "%s"' % (reference_id, content))
    if m_start and last_end:
        start = m_start.start(1)
        end = last_end or m_start.end()
        refs = content[start:end].replace('\n', ' ')
        refs = _CLEAN_REFS_PATTERN.sub('', refs)
        for enum, y, origin, sn, alt_year in _REF_PATTERN.findall(refs):
            if alt_year and not y:
                y = alt_year
            y = format_year(y)
            origin = origin.replace(' ', '').replace(u"'", u'').upper()
            if origin == 'AND' and res and res[-1].is_cable():
                last_origin = _REF_ORIGIN_PATTERN.match(res[-1].value).group(1)
                origin = last_origin
                enum = enum or res[-1].name
            elif origin.startswith('AND') and res and res[-1].is_cable(): # for references like 09 FOO 1234 AND BAR 1234
                origin = origin[3:]
                enum = enum or res[-1].name
            reference = u'%s%s%d' % (y, origin, int(sn))
            if canonicalize:
                reference = canonicalize_id(reference)
            length = len(reference)
            if length < 7 or length > 25: # constants.MIN_ORIGIN_LENGTH + constants.MIN_SERIAL_LENGTH + length of year or constants.MAX_ORIGIN_LENGTH + constants.MAX_SERIAL_LENGTH + 2 (for the year) 
                continue
            if not REFERENCE_ID_PATTERN.match(reference):
                if 'CORRUPTION' not in reference and 'ECRET' not in reference and 'PARISPOINT' not in reference and 'TELCON' not in reference and 'FORTHE' not in reference and 'ZOCT' not in reference and 'ZSEP' not in reference and 'ZMAY' not in reference and 'ZNOV' not in reference and 'ZAUG' not in reference and 'PRIORITY' not in reference and 'ZJAN' not in reference and 'ZFEB' not in reference and 'ZJUN' not in reference and'ZJUL' not in reference and 'PREVIO' not in reference and 'SEPTEMBER' not in reference and 'ZAPR' not in reference and 'ZFEB' not in reference and 'PART' not in reference and 'ONFIDENTIAL' not in reference and 'SECRET' not in reference and 'SECTION' not in reference and 'TODAY' not in reference and 'DAILY' not in reference and 'OUTOF' not in reference and 'PROVIDING' not in reference and 'NUMBER' not in reference and 'APRIL' not in reference and 'OCTOBER' not in reference and 'MAIL' not in reference and 'DECEMBER' not in reference and 'FEBRUAY' not in reference and 'AUGUST' not in reference and 'MARCH' not in reference and 'JULY' not in reference and 'JUNE' not in reference and 'MAIL' not in reference and 'JANUARY' not in reference and '--' not in reference and 'PARAGRAPH' not in reference and 'ANDPREVIOUS' not in reference and 'UNCLAS' not in reference and 'ONMARCH' not in reference and 'ONAPRIL' not in reference and 'FEBRUARY' not in reference and 'ONMAY' not in reference and 'ONJULY' not in reference and 'ONJUNE' not in reference and 'NOVEMBER' not in reference and not 'CONFIDENTIAL' in reference:
                    logger.debug('Ignore "%s". Not a valid reference identifier (%s)' % (reference, reference_id))
                continue
            if reference != reference_id:
                reference = Reference(reference, consts.REF_KIND_CABLE, enum)
                if reference not in res:
                    res.append(reference)
    return res


# "Kaz" found in "10ASTANA267" "NOFORN" found in "08MADRID308"
_TAGS_PATTERN = re.compile(r'(?<!Kaz)(?:TAGS|TAG|AGS:)(?!\n\nNOFORN)(?::\s*|\s+)(.+)', re.IGNORECASE|re.UNICODE)
_TAGS_SUBJECT_PATTERN = re.compile(r'(SUBJECT:)', re.IGNORECASE|re.UNICODE)
_TAGS_CONT_PATTERN = re.compile(r'(?:\n)([a-zA-Z_-]+.+)', re.MULTILINE|re.UNICODE)
_TAGS_CONT_NEXT_LINE_PATTERN = re.compile(r'\n[ ]*[A-Za-z_-]+[ ]*,', re.UNICODE)
_TAG_PATTERN = re.compile(r'(GOI[ ]+EXTERNAL)|(GOI[ ]+INTERNAL)|(POLITICAL[ ]+PARTIES)|(MEDIA[ ]+REACTION)|(USEU[ ]+BRUSSELS)|(POLITICS[ ]+FOREIGN[ ]+POLICY)|(MILITARY[ ]+RELATIONS)|(ISRAEL[ ]+RELATIONS)|(COUNTRY[ ]+CLEARANCE)|(CROS[ ]+GERARD)|(ROOD[ ]+JOHN)|(NEW[ ]+ZEALAND)|(MEETINGS[ ]+WITH[ ]+AMBASSADOR)|(DOMESTIC[ ]+POLITICS)|(ITALIAN[ ]+POLITICS)|(ITALY[ ]+NATIONAL[ ]+ELECTIONS)|(IRAQI[ ]+FREEDOM)|(ECONOMY[ ]+AND[ ]+FINANCE)|(GLOBAL[ ]+DEFENSE)|(NOVO[ ]+GUILLERMO)|(REMON[ ]+PEDRO)|(JIMENEZ[ ]+GASPAR)|(CONSULAR[ ]+AFFAIRS)|(ECONOMIC[ ]+AFFAIRS)|(HUMAN[ ]+RIGHTS)|(BUSH[ ]+GEORGE)|(CARSON[ ]+JOHNNIE)|(ZOELLICK[ ]+ROBERT)|(GAZA[ ]+DISENGAGEMENT)|(ISRAELI[ ]+PALESTINIAN[ ]+AFFAIRS)|(COUNTER[ ]+TERRORISM)|(CLINTON[ ]+HILLARY)|(STEINBERG[ ]+JAMES)|(BIDEN[ ]+JOSEPH)|(RICE[ ]+CONDOLEEZZA)|([A-Za-z_-]+)|(\([^\)]+\))|(?:,[ ]+)([A-Za-z_-]+[ ][A-Za-z_-]+)', re.UNICODE|re.MULTILINE)

# Used to normalize the TAG (corrects typos etc.)
_TAG_FIXES = {
    u'CLINTON HILLARY': (u'CLINTON, HILLARY',),
    u'STEINBERG JAMES': (u'STEINBERG, JAMES B.',),
    u'BIDEN JOSEPH': (u'BIDEN, JOSEPH',),
    u'ZOELLICK ROBERT': (u'ZOELLICK, ROBERT',),
    u'RICE CONDOLEEZZA': (u'RICE, CONDOLEEZZA',),
    u'CARSON JOHNNIE': (u'CARSON, JOHNNIE',),
    u'BUSH GEORGE': (u'BUSH, GEORGE',),
    u'ROOD JOHN': (u'ROOD, JOHN',),
    u'CROS GERARD': (u'CROS, GERARD',),
    u'NOVO GUILLERMO': (u'NOVO, GUILLERMO',),
    u'REMON PEDRO': (u'REMON, PEDRO',),
    u'JIMENEZ GASPAR': (u'JIMENEZ, GASPAR',),
    u'COUNTER TERRORISM': (u'COUNTERTERRORISM',),
    u'MOPPS': (u'MOPS',), # 09BEIRUT818
    u'POGOV': (u'PGOV',), # 09LONDON2222
    u'RU': (u'RS',), # 09BERLIN1433, 09RIYADH181 etc.
    u'SYR': (u'SY',),
    u'UNDESCO': (u'UNESCO',), # 05SANJOSE2199
    u'KWWMN': (u'KWMN',), # 09TRIPOLI754
    u'RUPREL': (u'RS', u'PREL'), # 00HELSINKI2613)
    u'ITPHUM': (u'IT', u'PHUM'), # 02ROME1196
    u'ITPGOV': (u'IT', u'PGOV'), # 02ROME3639
    u'NATOPREL': (u'NATO', u'PREL'), # 03VATICAN523
    u'SPCVIS': (u'SP', u'CVIS'), # 04MADRID1764
    u'MASSMNUC': (u'MASS', u'MNUC'), # 08BRASILIA93
    u'KNNPMNUC': (u'KNNP', u'MNUC'), # 08THEHAGUE553
    u'PTER MARR': (u'PTER', u'MARR'), # 07BAKU855
    u'PHUMPGOV': (u'PHUM', u'PGOV'), #09PARAMARIBO103
    u'PHUMPREL': (u'PHUM', u'PREL'), # 07NAIROBI4427
    u'VTPREL': (u'VT', u'PREL'), # 03VATICAN1570 and others
    u'VEPREL': (u'VE', u'PREL'), # 02VATICAN5607
    u'PRELPK': (u'PREL', u'PK'), # 10ISLAMABAD332
    u'PRELBR': (u'PREL', u'BR'), # 06BRASILIA2073
    u'PBTSRU': (u'PBTS', u'RS'), # 09MANAGUA913
    u'PGOVSOCI': (u'PGOV', u'SOCI'), # 07SAOPAULO726
    u'NATOIRAQ': (u'NATO', u'IRAQ'), # 05ATHENS2769
    u'ECONCS': (u'ECON', u'CS'), # 07SANJOSE298
    u'PGOVLO': (u'PGOV', u'LO'), # 08BRATISLAVA377
    u'SNARCS': (u'SNAR', u'CS'), # 08SANJOSE400
    u'ECINECONCS': (u'ECIN', u'ECON', u'CS'), # 06SANJOSE2649
    u'EFINECONCS': (u'EFIN', u'ECON', u'CS'), # 06SANJOSE2803
    u'KWMNCS': (u'KWMN', u'CS'), # 09SANJOSE692
    u'EINDETRD': (u'EIND', u'ETRD'), # 09PARIS1267
    u'ETRDEINVTINTCS': (u'ETRD', u'EINV', 'TINT', u'CS'), # 07SANJOSE426
    u'SNARIZ': (u'SNAR', u'IZ'), # 07HELSINKI127
    u'KPAONZ': (u'KPAO', u'NZ'), # 08WELLINGTON125 and others
    u'ELTNSNAR': (u'ELTN', u'SNAR'), # 07SAOPAULO161
    u'SENVKGHG': (u'SENV', u'KGHG'), # 09OTTAWA246
    u'ECON KISL': (u'ECON', u'KISL'), # 09RIYADH651
    u'UNFCYP': (u'UNFICYP',), # 09ATHENS252
    u'OVIPPRELUNGANU': (u'OVIP', u'PREL', u'UNGA', u'NU'), # 08MANAGUA1184
    u'ECONEFIN': (u'ECON', u'EFIN'), # 09CAIRO1691
    u'ETRDECONWTOCS': (u'ETRD', u'ECON', u'WTO', u'CS'), # 07SANJOSE436
    u'SENVEAGREAIDTBIOECONSOCIXR': (u'SENV', u'EAGR', u'EAID', u'TBIO', u'ECON' u'SOCI' u'XR'), # 08BRASILIA1504 and others
    u'ECONSOCIXR': (u'ECON', u'SOCI', u'XR'), # 08BRASILIA1504 and others
    u'EINVECONSENVCSJA': (u'EINV', u'ECON', u'SENV', u'CS', u'JA'), # 07SANJOSE653
#TODO: SENV GR?!?
#    u'SENVQGR': (u'SENV', u'GR'), # 06BRASILIA2419
    u'EINVKSCA': (u'EINV', u'KSCA'), # 08BRASILIA1335
#TODO: Unsure about this one, maybe POL INTERNAL or POL TINT?
#    u'POLINT': (u'POL', u'INT'), # 05PARIS7195
    u'PHUMBA': (u'PHUM', u'BA'), # 08ECTION01OF02MANAMA492 which is the malformed version of 08MANAMA492
    u'ETRDEINVECINPGOVCS': (u'ETRD', u'EINV', u'ECIN', u'PGOV', u'CS'), # 06SANJOSE2802 and others
    u'AMEDCASCKFLO': (u'AMED', u'CASC', u'KFLO'), # 09BRASILIA542
    u'KFRDKIRFCVISCMGTKOCIASECPHUMSMIGEG': (u'KFRD', u'KIRF', u'CVIS', u'CMGT', u'KOCI', u'ASEC', u'PHUM', u'SMIG', u'EG'), # 09CAIRO2205
    u'ASECKFRDCVISKIRFPHUMSMIGEG': (u'ASEC', u'KFRD', u'CVIS', u'KIRF', u'PHUM', u'SMIG', u'EG'), # 09CAIRO2190
    u'KFRDCVISCMGTCASCKOCIASECPHUMSMIGEG': (u'KFRD', u'CVIS', u'CMGT', u'CASC', u'KOCI', u'ASEC', u'PHUM', u'SMIG', u'EG'), # 09CAIRO1054 and others
    u'PGOVSMIGKCRMKWMNPHUMCVISKFRDCA': (u'PGOV', u'SMIG', u'KCRM', u'KWMN', u'PHUM', u'CVIS', u'KFRD', u'CA'), # 08TORONTO24
    u'KPAOPREL': (u'KPAO', u'PREL'), # 08VIENTIANE632
    u'POLMIL': (u'POL', u'MIL'), # 04PANAMA586 and others
    u'IZPREL': (u'IZ', u'PREL'), # 03ROME2045 and others
}

def parse_tags(content, reference_id=None, canonicalize=True):
    """\
    Returns the TAGS of a cable.
    
    Acc. to the U.S. SD every cable needs at least one tag.

    `content`
        The content of the cable.
    `reference_id`
        The reference identifier of the cable.
    `canonicalize`
        Indicates if duplicates should be removed and malformed
        TAGs like "ECONEFIN" should be corrected (becomes "ECON", "EFIN").
        ``False`` indicates that the TAGs should be returned as found in
        cable.
    """
    m = _TAGS_PATTERN.search(content)
    if not m:
        if reference_id not in _CABLES_WITHOUT_TAGS:
            logger.debug('No TAGS found in cable ID "%r", content: "%s"' % (reference_id, content))
        return []
    tags = m.group(1)
    min_idx = m.end()
    max_idx = _MAX_HEADER_IDX
    msubj = _TAGS_SUBJECT_PATTERN.search(content)
    if msubj:
        max_idx = min(max_idx, msubj.start())
        m = _TAGS_PATTERN.search(content, 0, max_idx)
        if m:
            tags = m.group(1)
    m2 = None
    if tags.endswith(',') or tags.endswith(', ') or _TAGS_CONT_NEXT_LINE_PATTERN.match(content, min_idx, max_idx):
        m2 = _TAGS_CONT_PATTERN.match(content, m.end(), max_idx)
    if m2:
        tags = u' '.join([tags, m2.group(1)])
    res = []
    if not canonicalize:
        return [u''.join(tag).upper() for tag in _TAG_PATTERN.findall(tags) if tag]
    for t in _TAG_PATTERN.findall(tags):
        tag = u''.join(t).upper().replace(u')', u'').replace(u'(', u'')
        if tag == u'SIPDIS': # Found in 05OTTAWA3726 and 05OTTAWA3709. I think it's an error
            continue
        for tag in _TAG_FIXES.get(tag, (tag,)):
            if tag == u'ECONSOCIXR': # 08BRASILIA1504
                for tag in _TAG_FIXES[tag]:
                    if not tag in res:
                        res.append(tag)
                continue
            if not tag in res:
                res.append(tag)
    return res

_END_SUMMARY_PATTERN = re.compile(r'END\s+SUMMARY', re.IGNORECASE)
# 09OSLO146 contains "Summay" instead of "SummaRy"
_START_SUMMARY_PATTERN = re.compile(ur'(SUMMAR?Y( AND COMMENT)?( AND ACTION REQUEST)?( AND INTRODUCTION)?( AND TABLE OF CONTENTS)?[ ‐\-\n:\.]*)', re.IGNORECASE)
# Some cables like 07BAGHDAD3895, 07TRIPOLI1066 contain "End Summary" but no "Summary:" start
# Since End Summary occurs in the first paragraph, we interpret the first paragraph as summary
_ALTERNATIVE_START_SUMMARY_PATTERN = re.compile(r'\n1\.[ ]*(\([^\)]+\))? ')
_PARSE_SUMMARY_PATTERN = re.compile(r'(?:SUMMARY[ \-\n]*)(?::|\.|\s)(.+?)(?=(\n[ ]*\n)|(END[ ]+SUMMARY)|(----+))', re.DOTALL|re.IGNORECASE|re.UNICODE)
_CLEAN_SUMMARY_CLS_PATTERN = re.compile(r'^[ ]*\([SBU/NTSC]+\)[ ]*')
_CLEAN_SUMMARY_WS_PATTERN = re.compile('[ \n]+')
_CLEAN_SUMMARY_PATTERN = re.compile(r'(===+)|(---+)|(((^[1-9])|(\n[1-9]))\.[ ]+\([^\)]+\)[ ]+)|(^[1-2]. Summary:)|(^[1-2]\.[ ]+)|(^and action request. )|(^and comment. )|(2. (C) Summary, continued:)', re.UNICODE|re.IGNORECASE)

def parse_summary(content, reference_id=None):
    """\
    Extracts the summary from the `content` of the cable.
    
    If no summary can be found, ``None`` is returned.
    
    `content`
        The content of the cable.
    `reference_id`
        The reference identifier of the cable.
    """
    summary = None
    m = _END_SUMMARY_PATTERN.search(content)
    if m:
        end_of_summary = m.start()
        m = _START_SUMMARY_PATTERN.search(content, 0, end_of_summary) or _ALTERNATIVE_START_SUMMARY_PATTERN.search(content, 0, end_of_summary)
        if m:
            summary = content[m.end():end_of_summary]
        elif reference_id not in _CABLES_WITH_MALFORMED_SUMMARY:
            logger.debug('Found "end of summary" but no start in "%s", content: "%s"' % (reference_id, content[:end_of_summary]))
    else:
        m = _PARSE_SUMMARY_PATTERN.search(content)
        if m:
            summary = content[m.start(1):m.end(1)]
    if summary:
        summary = _CLEAN_SUMMARY_CLS_PATTERN.sub(u'', summary)
        summary = _CLEAN_SUMMARY_PATTERN.sub(u' ', summary)
        summary = _CLEAN_SUMMARY_WS_PATTERN.sub(u' ', summary)
        summary = summary.strip()
    return summary


if __name__ == '__main__':
    import doctest
    doctest.testmod()

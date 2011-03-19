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
Utility functions for cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
import os
import re
import codecs
from functools import partial
from itertools import imap
from StringIO import StringIO
import gzip
import urllib2
from cablemap.core import cable_from_file, cable_from_html
from cablemap.core.models import Cable
from cablemap.core.constants import REFERENCE_ID_PATTERN, MALFORMED_CABLE_IDS
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            # Google Appengine offers simplejson via django
            from django.utils import simplejson as json
        except ImportError:
            pass #TODO: Exception?

class _Request(urllib2.Request):
    def __init__(self, url):
        urllib2.Request.__init__(self, url, headers={'User-Agent': 'CablemapBot/1.0', 'Accept-Encoding': 'gzip, identity'})

def _fetch_url(url):
    """\
    Returns the content of the provided URL.
    """
    resp = urllib2.urlopen(_Request(url))
    if resp.info().get('Content-Encoding') == 'gzip':
        return gzip.GzipFile(fileobj=StringIO(resp.read())).read().decode('utf-8')
    return resp.read().decode('utf-8')
    

_BASE = 'http://wikileaks.ch/'
_INDEX = _BASE + 'cablegate.html'

_LINKS_PATTERN = re.compile(r"<a href='(.+?)'\s*>")
_PAGINATOR_PATTERN = re.compile('''<div\s+class=(?:"|')paginator(?:"|')\s*>.+?<a href=(?:"|')(/date/[0-9]{4}-[0-9]{2}_).+?(?:"|')>([2-9]+)</a><a href=.+?> &gt;&gt;</a></div>''')
_PAGE_PATTERN = re.compile(r'''<a[ ]+href=(?:"|')([^"']+)(?:"|')>[2-9]+</a>''')
_BY_DATE_PATTERN = re.compile(r'''<div\s+class=(?:"|')sort(?:"|')\s+id=(?:"|')year_1966(?:"|')>(.+?)<h3>Browse\s+by\s+<a\s+href=(?:"|')#by_A''', re.DOTALL)


def cable_page_by_id(reference_id):
    """\
    Returns the HTML page of the cable identified by `reference_id`.

    >>> cable_page_by_id('09BERLIN1167') is not None
    True
    >>> cable_page_by_id('22BERLIN1167') is None
    True
    >>> # Test pagination
    >>> cable_page_by_id('09MOSCOW3010') is not None
    True
    >>> cable_page_by_id('10MADRID87') is not None
    True
    >>> cable_page_by_id('10MUSCAT103') is not None
    True
    """
    def normalize_year(y):
        year = y
        try:
            y = int(y)
        except TypeError:
            raise ValueError('Illegal year "%r"' % y)
        if y < 66:
            year = 2000 + y
        elif y < 100:
            year = 1900 + y
        return year
    def get_html_page(link, link_finder):
        pg = _fetch_url(_BASE + link)
        pg = pg[pg.rindex('pane big'):pg.rindex('</table>')]
        m = link_finder(pg)
        if m:
            return True, _fetch_url(_BASE + m.group(1))
        return False, pg
    m = REFERENCE_ID_PATTERN.match(MALFORMED_CABLE_IDS.get(reference_id, reference_id))
    if not m:
        return None
    if reference_id == '08BISHKEK1021':
        reference_id = '08SECTION01GF02BISHIEK21' # The only cable which has no valid counterpart
    year = normalize_year(m.group(1))
    index = _fetch_url(_INDEX)
    by_date_m = _BY_DATE_PATTERN.search(index)
    if by_date_m:
        index = by_date_m.group(1)
    else:
        return None
    p = re.compile(r"<div.+?id='year_%s'.*?>(.+?)</div>" % year, re.DOTALL)
    m = p.search(index)
    if not m:
        return None
    get_page = partial(get_html_page, link_finder=re.compile(r'''<a\s+href=(?:"|')(.+?)(?:"|')>%s</a>''' % reference_id).search)
    for link in _LINKS_PATTERN.findall(m.group(1)):
        found, page = get_page(link)
        if found:
            return page
        # Walk through the pages
        m = _PAGINATOR_PATTERN.search(page)
        if not m:
            continue
        link_base, max_page = m.groups()
        for pg in xrange(1, int(max_page)):
            found, page = get_page(link_base + str(pg))
            if found:
                return page
    return None

def _json_or_yaml(fn, cable, metaonly=False, include_summary=True):
    dct = {}
    dct.update((k, v) for k, v in cable.to_dict().iteritems() if v or v in (False, True))
    if metaonly:
        dct.pop('header', None)
        dct.pop('body', None)
        if not include_summary:
            dct.pop('summary', None)
    return fn(dct)

def cable_to_json(cable, metaonly=False, include_summary=True):
    """\
    Returns a JSON representation of the provided `cable`.

    It uses the format of <http://www.leakfeed.com/>_ plus some extensions.

    `metaonly`
        Indicates if the header, body and other content-related information
        should be omitted (``False`` by default)
    `include_summary`
        Indicates if the summary belongs to the metadata (``True`` by default)
        This parameter has only an effect if `metaonly` is set to ``True``

    >>> cable = Cable('something')
    >>> js = cable_to_json(cable)
    >>> dct = json.loads(js)
    >>> dct['identifier'] == 'something'
    True
    >>> 'summary' in dct
    False
    >>> cable.summary = 'Summary'
    >>> js = cable_to_json(cable)
    >>> dct = json.loads(js)
    >>> 'summary' in dct
    True
    >>> dct['summary'] == 'Summary'
    True
    >>> cable.content = 'Content'
    >>> dct = json.loads(cable_to_json(cable))
    >>> 'body' in dct
    True
    >>> dct = json.loads(cable_to_json(cable, metaonly=True))
    >>> 'body' in dct
    False
    >>> 'summary' in dct
    True
    >>> dct = json.loads(cable_to_json(cable, metaonly=True, include_summary=False))
    >>> 'body' in dct
    False
    >>> 'summary' in dct
    False
    """
    return _json_or_yaml(json.dumps, cable, metaonly, include_summary)

def cable_from_json(src):
    """\
    Returns a cable from a JSON string.
    
    `src`
        Either a string or a file-like object.

    >>> cable = Cable('something')
    >>> s = cable_to_json(cable)
    >>> cable2 = cable_from_json(s)
    >>> cable2.reference_id == cable.reference_id
    True
    >>> cable.subject = 'Subject'
    >>> s = cable_to_json(cable)
    >>> cable2 = cable_from_json(s)
    >>> cable2.subject == cable.subject
    True
    >>> from StringIO import StringIO
    >>> cable3 = cable_from_json(StringIO(s))
    >>> cable3.subject == cable.subject
    True
    >>> cable3.reference_id == cable.reference_id
    True
    """
    dct = hasattr(src, 'read') and json.load(src) or json.loads(src)
    return Cable.from_dict(dct)

def cable_to_yaml(cable, metaonly=False, include_summary=True):
    """\
    Returns a YAML representation of the provided `cable`.

    `metaonly`
        Indicates if the header, body and other content-related information
        should be omitted (``False`` by default)
    `include_summary`
        Indicates if the summary belongs to the metadata (``True`` by default)
        This parameter has only an effect if `metaonly` is set to ``True``

    >>> from models import Cable
    >>> cable = Cable('something')
    >>> yml = cable_to_yaml(cable)
    >>> import yaml
    >>> dct = yaml.load(yml)
    >>> dct['identifier'] == 'something'
    True
    >>> 'summary' in dct
    False
    >>> cable.summary = 'Summary'
    >>> yml = cable_to_yaml(cable)
    >>> dct = yaml.load(yml)
    >>> 'summary' in dct
    True
    >>> dct['summary'] == 'Summary'
    True
    """
    import yaml
    try:
        from yaml import CDumper as Dumper
    except ImportError:
        from yaml import Dumper
    to_yaml = partial(yaml.dump, Dumper=Dumper)
    return _json_or_yaml(to_yaml, cable, metaonly, include_summary)

def cables_from_directory(directory, predicate=None):
    """\
    Returns a generator with ``models.Cable`` instances.
    
    Walks through the provided directory and returns cables from
    the ``.html`` files.

    `directory`
        The directory to read the cables from.
    `predicate`
        A predicate that is invoked for each cable filename.
        If the predicate evaluates to ``False`` the file is ignored.
        By default, all cable files are used.
        I.e. ``cables_from_directory('./cables/', lambda f: f.startswith('09'))``
        would return cables where the filename starts with ``09``. 
    """
    return imap(cable_from_file, cablefiles_from_directory(directory, predicate))

def cablefiles_from_directory(directory, predicate=None):
    """\
    Returns a generator which yields absoulte filenames to cable HTML files.
    
    `directory`
        The directory.
    `predicate`
        A predicate that is invoked for each cable filename.
        If the predicate evaluates to ``False`` the file is ignored.
        By default, all files with the file extension ".html" are returned.
        I.e. ``cablefiles_from_directory('./cables/', lambda f: f.startswith('09'))``
        would accept only filenames starting with ``09``. 
    """
    pred = predicate or bool
    for root, dirs, files in os.walk(directory):
        for name in (n for n in files if '.html' in n and pred(n)):
            yield os.path.join(os.path.abspath(root), name)

def cables_from_7z(fileobj, predicate=None):
    """\
    Returns a generator with ``models.Cable`` instances.
    
    Walks through the provided archive and returns cables from
    the ``.html`` files. This function assumes that the archive uses the 
    standard cablegate archive layout (it contains a directory "/cables/").

    `fileobj`
        The file to read the cables from.
    `predicate`
        A predicate that is invoked for each cable filename.
        If the predicate evaluates to ``False`` the file is ignored.
        By default, all cable files are used.
        I.e. ``cables_from_7z(fileobj, lambda f: f.startswith('09'))``
        would return cables where the filename starts with ``09``. 
    """
    import py7zlib
    def refid(name):
        return name[:name.rindex('.')]
    a = py7zlib.Archive7z(fileobj)
    pred = predicate or bool
    basename = os.path.basename
    return (cable_from_html(unicode(member.read(), 'utf-8'), refid(basename(member.filename))) for member in a.getmembers() if member.filename.startswith('cable/') and pred(basename(member.filename)))

def cable_by_id(reference_id):
    """\
    Returns a cable by its reference identifier or ``None`` if
    the cable does not exist.

    The cable is fetched from the ``wikileaks.ch`` website.

    `reference_id`
        The reference identifier of the cable.
    """
    page = cable_page_by_id(reference_id)
    if page:
        return cable_from_html(page)
    return None


_CLEAN_PATTERNS = (
        # pattern, substitution
        (re.compile(r'''([0-9]+\s*\.?\s*\(?[SBU/NTSC]+\)[ ]*)  # Something like 1. (C)
                    |(\-{3,}|={3,}|_{3,}|/{3,}|\#{3,}|\*{3,}|\.{4,})      # Section delimiters
                    |(\s*[A-Z]+\s+[0-9 \.]+OF\s+[0-9]+)    # Section numbers like ROME 0001 003.2 OF 004
                    |(^[0-9]+\s*\.\s*)                     # Paragraph numbering without classification
                    |((END )?\s*SUMMAR?Y(\s+AND\s+COMMENT)?(\s+AND\s+ACTION\s+REQUEST)?\s*\.?:?[ ]*) # Introduction/end of summary
                    |((END )?\s*COMMENT\s*\.?:?[ ]*)       # Introduction/end of comment
                    |(^\s*SIPDIS\s*)                       # Trends to occur randomly ;)
                    |((?<=[a-z])?xx+)                      # xxx
                    ''', re.VERBOSE|re.MULTILINE|re.IGNORECASE),
            ''),
    )

def clean_content(content):
    """\
    Removes paragraph numbers, section delimiters, xxxx etc. from the content.
    
    This function can be used to clean-up the cable's content before it
    is processed by NLP tools or to create a search engine index.
    
    `content`
        The content of the cable.
    """
    for pattern, subst in _CLEAN_PATTERNS:
        content = pattern.sub(subst, content)
    return content


_ACRONYMS = [l.rstrip() for l in codecs.open(os.path.join(os.path.dirname(__file__), 'acronyms.txt'), 'rb', 'utf-8')]

#TODO: This should be automated as well.
_SPECIAL_WORDS = {
    'UK-BASED': u'UK-Based',
    'DROC--VATICAN': u'DROC--Vatican',
    'BRAZIL-UNSC:': u'Brazil-UNSC:',
    'NETHERLANDS/EU/TURKEY:': u'Netherlands/EU/Turkey:',
    'US-BRAZIL': u'US-Brazil',
    'NETHERLANDS/EU:': u'Netherlands/EU:',
    'EU/TURKEY:': u'EU/Turkey:',
    'ACCESSION/EU:': u'Accession/EU:',
    'EX-GTMO': u'Ex-GTMO',
    'SUDAN/ICC:': u'Sudan/ICC:',
    'IDP/REFUGEE': u'IDP/Refugee',
    'EU/PAKISTAN:': u'EU/Pakistan:',
    'US-IRAN': u'US-Iran',
    'DUTCH/EU:': u'Dutch/EU:',
    'DoD': 'DoD',
    'SPAIN/CT:': u'Spain/CT:',
    'SPAIN/CIA': u'Spain/CIA',
    'SPAIN/ETA:': u'Spain/ETA:',
    'PRC/IRAN:': u'PRC/Iran:',
    'NETHERLANDS/JSF:': u'Netherlands/JSF:',
    'NETHERLANDS/JSF': u'Netherlands/JSF',
    'TURKEY/EU': u'Turkey/EU',
    'TURKEY-EU': u'Turkey-EU',
    'EU-AFRICA': u'EU/Africa',
    'U.S.-FRANCE-EU': u'U.S.-France-EU',
    'CHAD/SUDAN/EUFOR:': u'Chad/Sudan/EUFOR:',
    '(ART)': u'(art)',
    'MBZ': u'MbZ',
    'MbZ': u'MbZ',
    'SECGEN': u'SecGen',
    'Ex-IM': u'Ex-IM',
}

_TITLEFY_SMALL_PATTERN = re.compile(r'^(([0-9]+(th|st|rd|nd))|(a)|(an)|(and)|(as)|(at)|(but)|(by)|(en)|(for)|(if)|(in)|(of)|(on)|(or)|(the)|(to)|(v\.?)|(via)|(vs\.?))$', re.IGNORECASE)
_TITLEFY_BIG_PATTERN = re.compile(ur"^((%s)|(xx+)|(XX+)|(\([A-Z]{2,4}\):?))(([,:;\.\-])|(?:'|’)([a-z]{1,3}))?$" % r'|'.join(_ACRONYMS), re.UNICODE|re.IGNORECASE)
_APOS_PATTERN = re.compile(ur"^(\w+)('|’|,)([A-Z]{1,3}|,s)$", re.UNICODE|re.IGNORECASE)
_is_number = re.compile('^[0-9]+(th|st|rd|nd)$', re.IGNORECASE).match

def titlefy(subject):
    """\
    Titlecases the provided subject but respects common abbreviations.
   
    This function returns ``None`` if the provided `subject` is ``None``. It
    returns an empty string if the provided subject is empty.
   
    `subject
        A cable's subject.
    """
    def clean_word(word):
        return _APOS_PATTERN.sub(lambda m: u'%s%s%s' % (m.group(1), m.group(2) if not m.group(2) == ',' else u"'", m.group(3).lower()), word)
    def titlefy_word(word):
        if _is_number(word):
            return word.lower()
        if _TITLEFY_BIG_PATTERN.match(word):
            return clean_word(word.upper())
        return clean_word(_SPECIAL_WORDS.get(word, word.title()))
    if not subject:
        return None if subject is None else u''
    res = []
    append = res.append
    wl = subject.strip().split()
    append(titlefy_word(wl[0]))
    for word in wl[1:]:
        if _TITLEFY_SMALL_PATTERN.match(word):
            if res[-1][-1] not in ':-':
                if word == u'A' and res[-1] == u'and' and res[-2] == 'Q':
                    # Q and A
                    append(word.upper())
                else:
                    append(word.lower())
            else:
                append(titlefy_word(word))
        else:
            append(titlefy_word(word))
    return u' '.join(res)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

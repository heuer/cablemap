# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Utility functions for cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import absolute_import, with_statement
import os
import re
import csv
import codecs
import string
from itertools import imap
from StringIO import StringIO
import gzip
import urllib2
from cablemap.core import cable_from_file, cable_from_html, cable_from_row, constants as consts
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
            raise ImportError('Cannot detect a JSON decoder')
import sys
csv.field_size_limit(sys.maxint)
del sys


class _Request(urllib2.Request):
    def __init__(self, url):
        urllib2.Request.__init__(self, url,
                                 headers={'User-Agent': 'Cablemap/1.2',
                                          'Accept-Encoding': 'gzip, identity'})


def _fetch_url(url):
    """\
    Returns the content of the provided URL.
    """
    try:
        resp = urllib2.urlopen(_Request(url))
    except urllib2.URLError:
        if 'wikileaks.org' in url:
            resp = urllib2.urlopen(_Request(url.replace('wikileaks.org', 'wikileaks.ch')))
        else:
            raise
    if resp.info().get('Content-Encoding') == 'gzip':
        return gzip.GzipFile(fileobj=StringIO(resp.read())).read().decode('utf-8')
    return resp.read().decode('utf-8')
    

_CGSN_BASE = u'https://cablegatesearch.wikileaks.org/cable.php?id='
_CGSN_WL_SOURCE_SEARCH = re.compile(ur'''<td.*?>Source.+?<a.*?href=["']([^"']+)''').search

def cable_page_by_id(reference_id):
    """\
    Experimental: Returns the HTML page of the cable identified by `reference_id`.

    >>> cable_page_by_id('09BERLIN1167') is not None
    True
    >>> cable_page_by_id('22BERLIN1167') is None
    True
    >>> cable_page_by_id('09MOSCOW3010') is not None
    True
    >>> cable_page_by_id('10MADRID87') is not None
    True
    >>> cable_page_by_id('10MUSCAT103') is not None
    True
    """
    def wikileaks_id(reference_id):
        if reference_id in consts.INVALID_CABLE_IDS.values():
            for k, v in consts.INVALID_CABLE_IDS.iteritems():
                if v == reference_id:
                    return k
        return reference_id
    html = _fetch_url(_CGSN_BASE + wikileaks_id(reference_id))
    m = _CGSN_WL_SOURCE_SEARCH(html)
    return _fetch_url(m.group(1)) if m else None


def cable_by_id(reference_id):
    """\
    Returns a cable by its reference identifier or ``None`` if
    the cable does not exist.

    `reference_id`
        The reference identifier of the cable.
    """
    page = cable_page_by_id(reference_id)
    return cable_from_html(page) if page else None


def cable_by_url(url):
    """\
    Returns a cable read from the provided IRI.

    `url`
        The IRI to fetch the cable from.
    """
    page = _fetch_url(url)
    return cable_from_html(page) if page else None


def cables_from_source(path, predicate=None):
    """\
    Returns a generator with ``ICable`` instances.

    `path`
        Either a directory or a CSV file.
    `predicate`
        A predicate that is invoked for each cable reference identifier.
        If the predicate evaluates to ``False`` the cable is ignored.
        By default, all cables are used.
        I.e. ``cables_from_source('cables.csv', lambda r: r.startswith('09'))``
        would return cables where the reference identifier starts with ``09``.
    """
    return cables_from_directory(path, predicate) if os.path.isdir(path) else cables_from_csv(path, predicate)


def cables_from_csv(filename, predicate=None, encoding='utf-8'):
    """\
    Returns a generator with ``ICable`` instances.

    Reads the provided CSV file and returns a cable for each row.

    `filename`
        Absolute path to a file to read the cables from.
        The file must be a CSV file with the following columns:
        <identifier>, <creation-date>, <reference-id>, <origin>, <classification-level>, <references-to-other-cables>, <header>, <body>
        The delimiter must be a comma (``,``) and the content must be enclosed in double quotes (``"``).
    `predicate`
        A predicate that is invoked for each cable reference identifier.
        If the predicate evaluates to ``False`` the cable is ignored.
        By default, all cables are used.
        I.e. ``cables_from_csv('cables.csv', lambda r: r.startswith('09'))``
        would return cables where the reference identifier starts with ``09``.
    `encoding`
        The file encoding (``UTF-8`` by default).
    """
    pred = predicate or bool
    with open(filename, 'rb') as f:
        for row in _UnicodeReader(f, encoding=encoding, delimiter=',', quotechar='"', escapechar='\\'):
            if row and pred(row[2]):
                yield cable_from_row(row)


class _UTF8Recoder:
    """\
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class _UnicodeReader:
    """\
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = _UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

def cables_from_directory(directory, predicate=None):
    """\
    Returns a generator with ``ICable`` instances.
    
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
        for name in (n for n in files if '.html' in n and pred(n[:-5])):
            yield os.path.join(os.path.abspath(root), name)

def reference_id_parts(reference_id):
    """\
    Returns a tuple from the provided `reference_id`::

        (YEAR, ORIGIN, S/N)

    `reference_id`
        Cable reference identifier or canonical identifier.
    """
    m = consts.REFERENCE_ID_PATTERN.match(reference_id)
    if m:
        return m.groups()
    raise ValueError('Illegal reference identifier: "%s"' % reference_id)


_SIGNERS = json.load(codecs.open(os.path.join(os.path.dirname(__file__), 'signers.json'), 'rb', 'utf-8'))

def signer_name(sign, canonical_id, default=None):
    """\
    Returns the real name for the provided `sign`.

    Returns `default` if the name cannot be found.

    `sign`
        The sign, i.e. ``CLINTON``.
    `canonical_id`
        Canonical cable identifier.
    `default` 
        The value which shoule be returned iff the sign cannot be found.
    """
    year, origin, _ = reference_id_parts(canonical_id)
    origins = _SIGNERS.get(sign)
    res = default
    if origins:
        tmp = origins.get(origin)
        if isinstance(tmp, dict):
            tmp = tmp.get(year, default)
        res = tmp
    return res

_TAGS_SUBJECT = [l.upper().rstrip() for l in codecs.open(os.path.join(os.path.dirname(__file__), 'subject-tags.txt'), 'rb', 'utf-8')]
_TAGS_ORG = [l.upper().rstrip() for l in codecs.open(os.path.join(os.path.dirname(__file__), 'organization-tags.txt'), 'rb', 'utf-8')]

def tag_kind(tag, default=consts.TAG_KIND_UNKNOWN):
    """\
    Returns the TAG kind.

    `tag`
        A string.
    `default`
        A value to return if the TAG kind is unknown
        (set to ``constants.TAG_KIND_UNKNOWN`` by default)
    """
    if len(tag) == 2:
        return consts.TAG_KIND_GEO
    if u',' in tag:
        return consts.TAG_KIND_PERSON
    if tag[0] in u'Kk' and len(tag) == 4:
        return consts.TAG_KIND_PROGRAM
    t = tag.upper()
    if t in _TAGS_SUBJECT:
        return consts.TAG_KIND_SUBJECT
    if t in _TAGS_ORG:
        return consts.TAG_KIND_ORG
    return default


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
    'NSC-DIRECTED': u'NSC-Directed',
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
    'DOD': 'DoD',
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
    'GOH': u'GoH',
    'US-LIBYAN': u'US-Libyan',
    u'FAO/WHO': u'FAO/WHO',
}

_TITLEFY_SMALL_PATTERN = re.compile(r'^(([0-9]+(th|st|rd|nd))|(a)|(an)|(and)|(as)|(at)|(but)|(by)|(en)|(for)|(if)|(in)|(of)|(on)|(or)|(the)|(to)|(v\.?)|(via)|(vs\.?))$', re.IGNORECASE)
_TITLEFY_BIG_PATTERN = re.compile(ur"^([%s]?(%s)|(xx+)|(XX+)|(\([A-Z]{2,4}\):?))(?:[%s]?)(([,:;\.\-])|(?:'|’)([a-z]{1,3}))?$" % (string.punctuation, r'|'.join(_ACRONYMS), string.punctuation), re.UNICODE|re.IGNORECASE)
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

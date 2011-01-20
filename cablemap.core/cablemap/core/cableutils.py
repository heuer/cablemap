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
import re
from functools import partial
from StringIO import StringIO
import gzip
import urllib2
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

_CABLE_ID_PATTERN = re.compile('([0-9]{2})([A-Z]+)([0-9]+)')

_LINKS_PATTERN = re.compile(r"<a href='(.+?)'\s*>")
_PAGINATOR_PATTERN = re.compile('''<div\s+class=(?:"|')paginator(?:"|')\s*>(.+?)</div>''')
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
    >>> cable_page_by_id('10PRISTINA84') is not None
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
    m = _CABLE_ID_PATTERN.match(reference_id)
    if not m:
        return None
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
        for l in _PAGE_PATTERN.findall(m.group(1)):
            found, page = get_page(l)
            if found:
                return page
    return None

def cable_to_json(cable):
    """\
    Returns a JSON representation of the provided `cable`.

    It uses the format of <http://www.leakfeed.com/>_ plus some extensions.
    """
    return json.dumps(cable.to_dict())

def cable_to_yaml(cable):
    """\
    Returns a YAML representation of the provided `cable`.
    """
    import yaml
    try:
        from yaml import CDumper as Dumper
    except ImportError:
        from yaml import Dumper
    return yaml.dump(cable.to_dict(), Dumper=Dumper)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

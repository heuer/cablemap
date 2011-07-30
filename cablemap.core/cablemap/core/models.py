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
This module provides models to keep data about cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
import codecs
from operator import itemgetter
from cablemap.core import reader, constants as consts

__all__ = ['cable_from_file', 'cable_from_html']

_EMPTY = tuple()

def cable_from_file(filename):
    """\
    Returns a cable from the provided file.
    
    `filename`
        An absolute path to the cable file.
    """
    html = codecs.open(filename, 'rb', 'utf-8').read()
    return cable_from_html(html, reader.reference_id_from_filename(filename))

def cable_from_html(html, reference_id=None):
    """\
    Returns a cable from the provided HTML page.
    
    `html`
        The HTML page of the cable
    `reference_id`
        The reference identifier of the cable. If the reference_id is ``None``
        this function tries to detect it.
    """
    if not html:
        raise ValueError('The HTML page of the cable must be provided, got: "%r"' % html)
    if not reference_id:
        reference_id = reader.reference_id_from_html(html)
    cable = Cable(reference_id)
    reader.parse_meta(html, cable)
    cable.header = reader.get_header_as_text(html, reference_id)
    cable.content = reader.get_content_as_text(html, reference_id)
    return cable

# Commonly used base URIs for Wikileaks Cablegate
# Formats: 
# * BASE/<year>/<month>/<reference-id>
# * BASE/<year>/<month>/<reference-id>.html
_WL_CABLE_BASE_URIS = (
                u'http://wikileaks.org/cable/',
                u'http://wikileaks.ch/cable/',
                u'http://cablegate.wikileaks.org/cable/', # Does not work anymore
                u'http://213.251.145.96/cable/' # Seems to work neither
                )

# Source: <https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/utils.py#L30>
class cached_property(object):
    """\
    A decorator that converts a function into a lazy property.
    """
    _missing = object()

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, cached_property._missing)
        if value is cached_property._missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value

class Reference(tuple):
    """\
    Represents a reference to another cable, or e-mail message
    or any other referencable item.
    """
    __slots__ = ()
    
    def __new__(cls, value, kind, name=None):
        return tuple.__new__(cls, (value, kind, name or None))

    def is_cable(self):
        return self.kind == consts.REF_KIND_CABLE

    def is_email(self):
        return self.kind == consts.REF_KIND_EMAIL

    value = property(itemgetter(0))
    kind = property(itemgetter(1))
    name = property(itemgetter(2))


class Recipient(tuple):
    """\
    Represents a recipient of a cable.
    """
    __slots__ = ()
    
    def __new__(cls, route, name, precedence=None, mcn=None, excluded=None):
        return tuple.__new__(cls, (route or None, name, precedence or None, mcn or None, excluded or _EMPTY))

    route = property(itemgetter(0))
    name = property(itemgetter(1))
    excluded = property(itemgetter(2))
    # 5 FAH-1 H-221: FLASH, NIACT IMMEDIATE, IMMEDIATE, PRIORITY, ROUTINE
    precedence = property(itemgetter(3))
    # 5 FAH-2 H-321.7, 5 FAH-2 H-321.8
    # Message continuity number (MCN). An MCN is a
    # consecutive number from a series dedicated to each Department of State
    # activity. You assign an MCN to the Department activity on each telegram
    # sent to them, action or info
    mcn = property(itemgetter(4))

class Cable(object):
    """\
    Holds data about a cable.
    """
    def __init__(self, reference_id):
        """\

        `reference_id`
            The reference identifier of the cable
        """
        if not reference_id:
            raise ValueError('The reference id must be provided')
        self.reference_id = unicode(reference_id) # Ensure Unicode
        self.origin = None
        self.header = None
        self.content = None
        self.created = None
        self.released = None
        self.media_uris = []

    @cached_property
    def canonical_id(self):
        return reader.canonicalize_id(self.reference_id)

    @cached_property
    def wl_uris(self):
        """\
        Returns cable IRIs to WikiLeaks (mirrors).
        """
        def year_month(d):
            date, time = d.split()
            return date.split('-')[:2]
        if not self.created:
            raise ValueError('The "created" property must be provided')
        year, month = year_month(self.created)
        l = u'%s/%s/%s' % (year, month, self.reference_id)
        html = l + u'.html'
        wl_uris = []
        append = wl_uris.append
        for wl in _WL_CABLE_BASE_URIS:
            append(wl + l)
            append(wl + html)
        return wl_uris

    def __unicode__(self):
        return self.reference_id

    #
    # Header properties
    #
    @cached_property
    def transmission_id(self):
        if self.partial:
            return None
        return reader.parse_transmission_id(self.header, self.reference_id)

    @cached_property
    def recipients(self):
        if self.partial:
            return ()
        return reader.parse_recipients(self.header, self.reference_id)

    @cached_property
    def info_recipients(self):
        return reader.parse_info_recipients(self.header, self.reference_id)

    @cached_property
    def partial(self):
        return 'This record is a partial extract of the original cable' in self.header

    #
    # Content properties
    #
    @cached_property
    def subject(self):
        return reader.parse_subject(self.content, self.reference_id)

    @cached_property
    def nondisclosure_deadline(self):
        return reader.parse_nondisclosure_deadline(self.content)

    @cached_property
    def references(self):
        return reader.parse_references(self.content, self.created[:4], self.reference_id)

    @cached_property
    def tags(self):
        return reader.parse_tags(self.content, self.reference_id)

    @cached_property
    def summary(self):
        return reader.parse_summary(self.content, self.reference_id)

    @cached_property
    def content_header(self):
        return reader.header_body_from_content(self.content)[0]

    @cached_property
    def content_body(self):
        return reader.header_body_from_content(self.content)[1]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

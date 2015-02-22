# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
This module provides models to keep data about cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import absolute_import
import codecs
from itertools import chain
from operator import itemgetter
from cablemap.core import reader, c14n, consts
from cablemap.core.interfaces import ICable, IReference, IRecipient, implements

__all__ = ['cable_from_file', 'cable_from_html', 'cable_from_row']

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


def cable_from_row(row):
    """\
    Returns a cable from the provided row (a tuple/list).

    Format of the row:

        <identifier>, <creation-date>, <reference-id>, <origin>, <classification-level>, <references-to-other-cables>, <header>, <body>

    Note:
        The `<identifier>` and `<references-to-other-cables>` columns are ignored.

    `row`
        A tuple or list with 8 items.
    """
    def format_creation_date(created):
        date, time = created.split()
        month, day, year, hour, minute = [x.zfill(2) for x in chain(date.split(u'/'), time.split(u':'))]
        return u'%s-%s-%s %s:%s' % (year, month, day, hour, minute)
    _, created, reference_id, origin, classification, _, header, body = row
    cable = Cable(reference_id)
    cable.created = format_creation_date(created)
    cable.origin = origin
    cable.classification = classification.upper()
    cable.header = header
    cable.content = body
    return cable


# Commonly used base URIs for Wikileaks Cablegate
# Formats: 
# * BASE/<year>/<month>/<reference-id>
# * BASE/<year>/<month>/<reference-id>.html
_WL_CABLE_BASE_URIS = (
                u'https://wikileaks.org/cable/',
                u'http://wikileaks.org/cable/',
                u'http://wikileaks.ch/cable/',
                u'http://cablegate.wikileaks.org/cable/', # Does not work anymore
                u'http://213.251.145.96/cable/' # Seems to work neither
                )


class Reference(tuple):
    """\
    Represents a reference to another cable, or e-mail message
    or any other referencable item.
    """
    __slots__ = ()
    implements(IReference)
    
    def __new__(cls, value, kind, bullet=None, title=None):
        return tuple.__new__(cls, (value, kind, bullet.upper() if bullet else None, title.strip('"') if title else None))

    def is_cable(self):
        return self.kind == consts.REF_KIND_CABLE

    value = property(itemgetter(0))
    kind = property(itemgetter(1))
    bullet = property(itemgetter(2))
    title = property(itemgetter(3))


class Recipient(tuple):
    """\
    Represents a recipient of a cable.
    """
    __slots__ = ()
    implements(IRecipient)
    
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
    implements(ICable)

    def __init__(self, reference_id):
        """\

        `reference_id`
            The reference identifier of the cable
        """
        if not reference_id:
            raise ValueError('The reference id must be provided')
        self.reference_id = unicode(reference_id)
        self.origin = None
        self.header = None
        self.content = None
        self.created = None
        self.released = None
        self.classification = None
        self.media_uris = []


    @property
    def canonical_id(self):
        return c14n.canonicalize_id(self.reference_id)

    @property
    def plusd_canonical_id(self):
        return self.reference_id + u'_a'

    @property
    def plusd_uri(self):
        return u'http://www.wikileaks.org/plusd/cables/%s.html' % self.plusd_canonical_id

    @property
    def cabledrum_uri(self):
        return u'http://www.cabledrum.net/cables/' + self.reference_id

    @property
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
    @property
    def transmission_id(self):
        return reader.parse_transmission_id(self.header) if not self.is_partial else None

    @property
    def recipients(self):
        return reader.parse_recipients(self.header, self.reference_id) if not self.is_partial else _EMPTY

    @property
    def info_recipients(self):
        return reader.parse_info_recipients(self.header, self.reference_id)

    @property
    def is_partial(self):
        return 'This record is a partial extract of the original cable' in self.header

    #
    # Content properties
    #
    @property
    def subject(self):
        return reader.parse_subject(self.content, self.reference_id)

    @property
    def classification_categories(self):
        return reader.parse_classification_categories(self.content)

    @property
    def nondisclosure_deadline(self):
        return reader.parse_nondisclosure_deadline(self.content)

    @property
    def references(self):
        return reader.parse_references(self.content, self.created[:4], self.reference_id)

    @property
    def tags(self):
        return reader.parse_tags(self.content, self.reference_id)

    @property
    def summary(self):
        return reader.parse_summary(self.content, self.reference_id)

    @property
    def comment(self):
        return reader.parse_comment(self.content)

    @property
    def signed_by(self):
        return reader.parse_signed_by(self.content)

    @property
    def classified_by(self):
        return reader.parse_classified_by(self.content)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

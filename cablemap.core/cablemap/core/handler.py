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
This module defines a event handlers to process cables.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from __future__ import absolute_import
import logging
import urllib2
from .utils import cables_from_source, titlefy
from .interfaces import ICableHandler, implements
from .constants import REFERENCE_ID_PATTERN

class NoopCableHandler(object):
    """\
    `ICableHandler` implementation which does nothing.
    """
    implements(ICableHandler)
    
    def __getattr__(self, name):
        def noop(*args): pass
        return noop

class DelegatingCableHandler(object):
    """\
    A `ICableHandler` which delegates all events to an underlying
    `ICableHandler` instance.
    """
    implements(ICableHandler)

    def __init__(self, handler):
        """\
        `handler`
            The ICableHandler instance which should receive the events.
        """
        self._handler = handler

    def __getattr__(self, name):
        return getattr(self._handler, name)

class LoggingCableHandler(object):
    """\
    A `ICableHandler` which logs all events and delegates the events to
    an underlying `ICableHandler` instance.
    """
    implements(ICableHandler)
    
    def __init__(self, handler, level='info'):
        """\

        `handler`
            The ICableHandler instance which should receive the events.
        `level`
            The logging level (default: 'info')
        """
        self._handler = handler
        self.level = level

    def __getattr__(self, name):
        def logme(*args):
            getattr(logging, self.level)('%s%r' % (name, args))
            getattr(self._handler, name)(*args)
        return logme

class TeeCableHandler(object):
    """\
    A `ICableHandler` which delegates the events to two underlying `ICableHandler`
    instances.
    """
    implements(ICableHandler)

    def __init__(self, first, second):
        """\

        `first`
            The ICableHandler instance which should receive the events first.
        `second`
            The ICableHandler which receives the events after the first handler.
        """
        self._first = first
        self._second = second

    def __getattr__(self, name):
        def delegate(*args):
            getattr(self._first, name)(*args)
            getattr(self._second, name)(*args)
        return delegate

class MultipleCableHandler(object):
    """\
    A `ICableHandler` which delegates the events to multiple underlying `ICableHandler`
    instances.
    """
    implements(ICableHandler)

    def __init__(self, handlers):
        """\

        `handlers`
            An iterable of ICableMapHandler instances.
        """
        self._handlers = tuple(handlers)

    def __getattr__(self, name):
        def delegate(*args):
            for handler in self._handlers:
                getattr(handler, name)(*args)
        return delegate

class CableYearOriginFilter(DelegatingCableHandler):
    """\

    """
    def __init__(self, handler, year_filter=None, origin_filter=None):
        super(CableYearOriginFilter, self).__init__(handler)
        if year_filter and origin_filter:
            self._filter = lambda y, o: year_filter(y) and origin_filter(o)
        elif year_filter:
            self._filter = lambda y, o: year_filter(y)
        elif origin_filter:
            self._filter = lambda y, o: origin_filter(o)
        else:
            self._filter = bool
        self._process = False

    def start(self):
        self._handler.start()

    def end(self):
        self._handler.end()

    def start_cable(self, reference_id, canonical_id):
        year, origin, _ = REFERENCE_ID_PATTERN.match(canonical_id).groups()
        self._process = self._filter(year, origin)
        if self._process:
            self._handler.start_cable(reference_id, canonical_id)

    def __getattr__(self, name):
        def noop(*args): pass
        if self._process:
            return super(CableYearOriginFilter, self).__getattr__(name)
        return noop

class DefaultMetadataOnlyFilter(DelegatingCableHandler):
    """\
    ICableHandler implementation that acts as filter to omit the
    header and content of a cable. Further, it generates optionally titlefied
    subjects, and filters WikiLeaks IRIs != http://wikileaks.org/cable/<year>/<month>/<reference-id>.html
    """
    def __init__(self, handler, titlefy_subject=True):
        """\

        `handler`
            The ICableHandler which should receive the (filtered) events.
        `titlefy_subject`
            Indicates if the subjects should be titlefied (default: ``True``).
        """
        super(DefaultMetadataOnlyFilter, self).__init__(handler)
        if titlefy_subject:
            self.handle_subject = self._handle_subject_titlefy

    def handle_wikileaks_iri(self, iri):
        if iri.startswith(u'http://wikileaks.org') and iri.endswith(u'html'):
            self._handler.handle_wikileaks_iri(iri)

    def _handle_subject_titlefy(self, subject):
        self._handler.handle_subject(titlefy(subject))

    def handle_release_date(self, date):
        # This info isn't that interesting anymore since the lastest
        # release uses "2011-08-30" for all cables.
        pass

    def handle_body(self, body):
        pass

    def handle_header(self, header):
        pass


class DebitlyFilter(DelegatingCableHandler):
    """\
    `DelegatingCableHandler` implementation that expands bit.ly media IRIs
    """
    def __init__(self, handler):
        """\

        `handler`
            The ICableHandler which should receive the (filtered) events.
        """
        super(DebitlyFilter, self).__init__(handler)
        self._bitly2url = {}
        # For some reason this returns 404, acc. to <http://knowurl.com/>
        # the IRI is:
        self._bitly2url[u'http://bit.ly/mDfYBE'] = u'http://www.haiti-liberte.com/archives/volume4-46/Les%20c%C3%A2bles%20de%20WikiLeaks%20sur%20Ha%C3%AFti%20publi%C3%A9s%20par%20Ha%C3%AFti%20Libert%C3%A9.asp'

    def handle_media_iri(self, iri):
        class HeadRequest(urllib2.Request):
            def get_method(self):
                return 'HEAD'
        if iri.startswith(u'http://bit.ly'):
            if not iri in self._bitly2url:
                request = HeadRequest(iri)
                try:
                    response = urllib2.urlopen(request)
                    self._bitly2url[iri] = response.geturl()
                except urllib2.HTTPError:
                    pass
            iri = self._bitly2url.get(iri, iri)
        self._handler.handle_media_iri(iri)


def handle_cable(cable, handler, standalone=True):
    """\
    Emits event from the provided `cable` to the handler.

    `cable`
        A cable object.
    `handler`
        A ICableHandler instance.
    `standalone`
        Indicates if a `start` and `end` event should be
        issued (default: ``True``).
        If `standalone` is set to ``False``, no ``handler.start()``
        and ``handler.end()`` event will be issued.
    """
    def datetime(dt):
        date, time = dt.split(u' ')
        if len(time) == 5:
            time = time + u':00'
        time = time + u'Z'
        return u'T'.join([date, time])
    if standalone:
        handler.start()
    handler.start_cable(cable.reference_id, cable.canonical_id)
    for iri in cable.wl_uris:
        handler.handle_wikileaks_iri(iri)
    handler.handle_creation_datetime(datetime(cable.created))
    if cable.released:
        handler.handle_release_date(cable.released[:10])
    if cable.nondisclosure_deadline:
        handler.handle_nondisclosure_deadline(cable.nondisclosure_deadline)
    if cable.transmission_id:
        handler.handle_transmission_id(cable.transmission_id)
    if cable.subject:
        handler.handle_subject(cable.subject)
    if cable.summary:
        handler.handle_summary(cable.summary)
    if cable.comment:
        handler.handle_comment(cable.comment)
    handler.handle_header(cable.header)
    handler.handle_body(cable.content)
    handler.handle_origin(cable.origin)
    handler.handle_classification(cable.classification)
    handler.handle_partial(cable.partial)
    for signer in cable.signers:
        handler.handle_signer(signer)
    for tag in cable.tags:
        handler.handle_tag(tag)
    for iri in cable.media_uris:
        handler.handle_media_iri(iri)
    for rec in cable.recipients:
        handler.handle_recipient(rec)
    for rec in cable.info_recipients:
        handler.handle_info_recipient(rec)
    for ref in cable.references:
        handler.handle_reference(ref)
    handler.end_cable()
    if standalone:
        handler.end()

def handle_cables(cables, handler):
    """\
    Issues one ``handler.start()`` event, processes all `cables` and
    issues a ``handler.end()`` event.

    `cables`
        An iterable of Cable objects.
    """
    handler.start()
    for cable in cables:
        handle_cable(cable, handler, False)
    handler.end()

def handle_source(path, handler, predicate=None):
    """\
    Reads all cables from the provided source and issues events to
    the `handler`.

    `path`
        Either a directory with cable files or a CSV file.
    `handler`
        The handler which should receive the events.
    `predicate`
        A predicate that is invoked for each cable reference identifier.
        If the predicate evaluates to ``False`` the cable is ignored.
        By default, all cables are used.
        I.e. ``handle_source('cables.csv', handler, lambda r: r.startswith('09'))``
        would return cables where the reference identifier starts with ``09``.
    """
    handle_cables(cables_from_source(path, predicate), handler)


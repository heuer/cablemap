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
import logging
from cablemap.core.utils import cables_from_directory
from cablemap.core.interfaces import ICableHandler, implements

class NoopCableHandler(object):
    """\
    `ICableHandler` implementation which does nothing.
    """
    implements(ICableHandler)
    
    def __getattr__(self, name):
        def noop(*args): pass
        return noop

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
        self._first = first
        self._second = second

    def __getattr__(self, name):
        def delegate(*args):
            getattr(self._first, name)(*args)
            getattr(self._second, name)(*args)
        return delegate


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
    def date_time(dt):
        return dt.replace(u' ', u'T') + u'Z'
    if standalone:
        handler.start()
    handler.start_cable(cable.reference_id, cable.canonical_id)
    for rec in cable.recipients:
        handler.handle_recipient(rec)
    for rec in cable.info_recipients:
        handler.handle_info_recipient(rec)
    for ref in cable.references:
        handler.handle_reference(ref)
    handler.handle_creation_datetime(date_time(cable.created))
    handler.handle_release_datetime(date_time(cable.released))
    if cable.nondisclosure_deadline:
        handler.handle_nondisclosure_deadline(cable.nondisclosure_deadline)
    if cable.transmission_id:
        handler.handle_transmission_id(cable.transmission_id)
    handler.handle_classification(cable.classification)
    handler.handle_partial(cable.partial)
    for tag in cable.tags:
        handler.handle_tag(tag)
    for iri in cable.wl_uris:
        handler.handle_wikileaks_iri(iri)
    for iri in cable.media_uris:
        handler.handle_media_iri(iri)
    if cable.subject:
        handler.handle_subject(cable.subject)
    if cable.summary:
        handler.handle_summary(cable.summary)
    handler.handle_header(cable.header)
    handler.handle_body(cable.content)
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

def handle_directory(directory, handler):
    """\
    Reads all cables from the provided directory and issues events to
    the `handler`.

    `directory`
        The directory to process.
    `handler`
        The handler which should receive the events.
    """
    handle_cables(cables_from_directory(directory), handler)

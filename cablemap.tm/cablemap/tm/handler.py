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
This module defines an event handler to process cables.
"""
from __future__ import absolute_import
import re
from mio.ctm.miohandler import CTMHandler
from mio.xtm.miohandler import XTM21Handler
from tm.mio.handler import simplify
from tm import XSD, mio
from cablemap.core import constants as consts
from cablemap.core.interfaces import ICableHandler, implements
from . import psis

__all__ = ('create_ctm_handler', 'create_xtm_handler', 'MIOCableHandler')

_PREFIXES = {
    u'onto': psis.NS_ONTO,
    u'cb': psis.NS_CABLE,
    u'sj': psis.NS_TAG_SUBJECT,
    u'geo': psis.NS_TAG_GEO,
    u'prg': psis.NS_TAG_PROGRAM,
    u'ps': psis.NS_TAG_PERSON,
    u'org': psis.NS_TAG_ORG,
    u'st': psis.NS_STATION,
    u'cls': psis.NS_CLASSIFICATION,
}

def create_ctm_handler(fileobj):
    """\
    Returns a `ICableHandler` instance which writes Compact Topic Maps syntax (CTM).

    `fileobj`
        A file-like object.
    """
    handler = CTMHandler(fileobj)
    for prefix, ns in _PREFIXES.iteritems():
       handler.add_prefix(prefix, str(ns))
    return _cablehandler(handler)

def create_xtm_handler(fileobj):
    """\
    Returns a `ICableHandler` instance which writes XML Topic Maps syntax (XTM) 2.1.

    `fileobj`
        A file-like object.
    """
    return _cablehandler(XTM21Handler(fileobj=fileobj))
    
def _cablehandler(handler):
    """\
    Converts a MIO handler into a `ICableHandler`.
    """
    handler.comment = u'Generated by Cablemap - https://github.com/heuer/cablemap'
    return MIOCableHandler(handler)


_is_dedicated_media_page = re.compile(r'https?://.+?/.+').match

class MIOCableHandler(object):
    """\
    Implementation of a `ICableHandler` which translates the events into
    MIO events (c.f. <https://mappa.googlecode.com/hg/tm/tm/mio/handler.py>_)
    """
    implements(ICableHandler)

    def __init__(self, handler):
        """\

        `handler`
            MIO event handler.
        """
        self._handler = simplify(handler)
        self._cable = None
        self._cable_id = None
        self._ref_counter = 0

    #
    # ICableHandler methods.
    #
    def start(self):
        self._handler.startTopicMap()
        
    def end(self):
        self._handler.endTopicMap()

    def start_cable(self, reference_id, canonical_id):
        h = self._handler
        self._cable = psis.cable_psi(canonical_id)
        self._cable_id = canonical_id
        h.startTopic(self._cable)
        self._name(canonical_id)
        self._name(reference_id, psis.REFERENCE_TYPE)
        h.isa(psis.CABLE_TYPE)

    def end_cable(self):
        self._cable, self._cable_id = None, None
        self._handler.endTopic()

    def handle_tag(self, tag):
        self._assoc(psis.TAGGED_TYPE,
                    psis.CABLE_TYPE, self._cable,
                    psis.TAG_TYPE, psis.tag_psi(tag))
   
    def handle_origin(self, origin):
        # Cheating here. The `origin` isn't used but the cable identifier.
        self._sent_by(psis.origin_psi_by_cable_id(self._cable_id), self._cable)
    
    def handle_recipient(self, recipient):
        pass

    def handle_info_recipient(self, recipient):
        pass

    def _handle_recipient(self, recipient, typ):
        """\

        """

    def handle_reference(self, reference):
        enum = reference.name
        reifier = None
        if enum:
            self._ref_counter+=1
            reifier = mio.ITEM_IDENTIFIER, u'#%s-ref-%s' % (self._cable_id, self._ref_counter)
        processed = True
        kind = reference.kind
        handler = self._handler
        if kind == consts.REF_KIND_CABLE:
            self._handle_reference_cable(reference, handler, reifier)
        elif kind == consts.REF_KIND_BOOK:
            processed = self._handle_reference_book(reference, handler, reifier)
        else:
            processed = False
        if processed and reifier:
            handler.startTopic(reifier)
            self._name(enum)
            handler.endTopic()

    def _handle_reference_cable(self, reference, handler, reifier):
        """\

        """
        cable_ref = psis.cable_psi(reference.value)
        self._assoc(psis.REFERENCES_TYPE,
                    psis.SOURCE_TYPE, self._cable,
                    psis.TARGET_TYPE, cable_ref,
                    reifier)
        handler.startTopic(cable_ref)
        self._name(reference.value)
        handler.isa(psis.CABLE_TYPE)
        handler.endTopic()
        self._sent_by(psis.origin_psi_by_cable_id(reference.value), cable_ref)

    def _handle_reference_book(self, reference, handler, reifier):
        """\

        """
        return False
        
    
    def handle_subject(self, subject):
        self._name(subject, psis.SUBJECT_TYPE)

    def handle_transmission_id(self, tid):
        self._occ(tid, psis.TID_TYPE)

    def handle_header(self, header):
        self._occ(header, psis.HEADER_TYPE)

    def handle_body(self, body):
        self._occ(body, psis.BODY_TYPE)

    def handle_summary(self, summary):
        self._occ(summary, psis.SUMMARY_TYPE)

    def handle_classification(self, classification):
        self._assoc(psis.CLASSIFIED_AS_TYPE,
                    psis.CABLE_TYPE, self._cable,
                    psis.CLASSIFICATION_TYPE, psis.classification_psi(classification))

    def handle_nondisclosure_deadline(self, date):
        self._occ(date, psis.NONDISCLOSURE_DEADLINE_TYPE, XSD.date)

    def handle_creation_datetime(self, datetime):
        self._occ(datetime, psis.CREATED_TYPE, XSD.dateTime)

    def handle_release_date(self, date):
        self._occ(date, psis.RELEASED_TYPE, XSD.date)

    def handle_partial(self, partial):
        if partial:
            self._assoc(psis.IS_PARTIAL_TYPE,
                        psis.PARTIAL_TYPE, self._cable)

    def handle_wikileaks_iri(self, iri):
        self._handler.subjectLocator(iri)

    def handle_media_iri(self, iri):
        if _is_dedicated_media_page(iri):
            self._assoc(psis.COVERED_BY_TYPE,
                        psis.CABLE_TYPE, self._cable,
                        psis.COVERED_BY_RESOURCE_TYPE, (mio.SUBJECT_LOCATOR, iri))
        else:
            self._assoc(psis.COVERED_BY_TYPE,
                        psis.CABLE_TYPE, self._cable,
                        psis.MEDIA_TYPE, psis.media_psi(iri))

    #
    # Private methods
    #
    def _name(self, value, typ=None):
        """\
        Issues events to create a name.

        `value`
            The name.
        `typ`
            Optional identity of the name type. If type is ``None`` (default)
            the default name type will be used.
        """
        self._handler.name(value, typ)

    def _occ(self, value, typ, datatype=None):
        """\
        Issues events to create an occurrence.

        `value`
            The string value
        `typ`
            The occurrence type
        `datatype`
            The datatype (default: xsd:string)
        """
        self._handler.occurrence(typ, value, datatype)

    def _sent_by(self, origin, cable):
        """\

        `origin`
            Topic identity (commonly a subject identifier) of the originator of the cable
        `cable`
            Topic identity (commonly a subject identifier) of the cable.
        """
        self._assoc(psis.SENT_BY_TYPE,
                    psis.SENDER_TYPE, origin,
                    psis.CABLE_TYPE, cable)

    def _assoc(self, typ, role1, player1, role2=None, player2=None, reifier=None):
        """\

        """
        h = self._handler
        h.startAssociation(typ)
        h.role(role1, player1)
        if role2:
            h.role(role2, player2)
        if reifier:
            h.reifier(reifier)
        h.endAssociation()

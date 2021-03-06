# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2012 -- Lars Heuer <heuer[at]semagia.com>
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
import logging
import htmlentitydefs
import urllib2
import gzip
from StringIO import StringIO

from mio.ctm.miohandler import CTMHandler
from mio.xtm.miohandler import XTM21Handler
from tm.mio.handler import simplify
from tm import XSD, mio
from cablemap.core import consts as consts
from cablemap.core.handler import NoopCableHandler
from . import psis

logger = logging.getLogger('cablemap.tm.handler')

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
    u'wp': psis.NS_WP,
    u'r': psis.NS_ROUTE,
    u'pr': psis.NS_PRECEDENCE,
    u'p': psis.NS_PERSON,
    u'ap': u'http://www.aftenposten.no/spesial/wikileaksdokumenter/',
    u'ala': u'http://www.al-akhbar.com/node/',
    u'th': u'http://www.thehindu.com/news/the-india-cables/',
}

def create_ctm_miohandler(fileobj, title=None, comment=None, register_prefixes=True, register_templates=True, detect_prefixes=False):
    """\

    """
    handler = CTMHandler(fileobj)
    handler.title = title
    handler.comment = comment
    handler.detect_prefixes = detect_prefixes
    if register_prefixes:
        register_default_prefixes(handler)
    if register_templates:
        handler.add_association_template(u'classified', psis.CLASSIFIED_AS_TYPE, psis.CABLE_TYPE, psis.CLASSIFICATION_TYPE)
        handler.add_association_template(u'origin', psis.SENT_BY_TYPE, psis.CABLE_TYPE, psis.SENDER_TYPE)
        handler.add_association_template(u'references', psis.REFERENCES_TYPE, psis.SOURCE_TYPE, psis.TARGET_TYPE)
        handler.add_association_template(u'to', psis.RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE)
        handler.add_association_template(u'to', psis.RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE, psis.ROUTE_TYPE)
        handler.add_association_template(u'to', psis.RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE, psis.ROUTE_TYPE, psis.PRECEDENCE_TYPE)
        handler.add_association_template(u'to', psis.RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE, psis.ROUTE_TYPE, psis.PRECEDENCE_TYPE, psis.MCN_TYPE)
        handler.add_association_template(u'info', psis.INFO_RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE)
        handler.add_association_template(u'info', psis.INFO_RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE, psis.ROUTE_TYPE)
        handler.add_association_template(u'info', psis.INFO_RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE, psis.ROUTE_TYPE, psis.PRECEDENCE_TYPE)
        handler.add_association_template(u'info', psis.INFO_RECIPIENT_TYPE, psis.CABLE_TYPE, psis.RECIPIENT_TYPE, psis.ROUTE_TYPE, psis.PRECEDENCE_TYPE, psis.MCN_TYPE)
        handler.add_association_template(u'tagged', psis.TAGGED_TYPE, psis.CABLE_TYPE, psis.TAG_TYPE)
        handler.add_association_template(u'is-partial', psis.IS_PARTIAL_TYPE, psis.PARTIAL_TYPE)
        handler.add_association_template(u'signed-by', psis.SIGNED_TYPE, psis.CABLE_TYPE, psis.SIGNER_TYPE)
    return handler

def register_default_prefixes(handler):
    """\

    """
    for prefix, ns in _PREFIXES.iteritems():
       handler.add_prefix(prefix, str(ns))

def create_xtm_miohandler(fileobj, title=None, comment=None):
    """\

    """
    handler = XTM21Handler(fileobj=fileobj)
    handler.title = title
    handler.comment = comment
    return handler

def create_ctm_handler(fileobj, title=u'Cablegate Topic Map', comment=u'Generated by Cablemap - https://github.com/heuer/cablemap', detect_prefixes=False):
    """\
    Returns a `ICableHandler` instance which writes Compact Topic Maps syntax (CTM).

    `fileobj`
        A file-like object.
    """
    return MIOCableHandler(create_ctm_miohandler(fileobj, title, comment, detect_prefixes=detect_prefixes))

def create_xtm_handler(fileobj, title=u'Cablegate Topic Map', comment=u'Generated by Cablemap - https://github.com/heuer/cablemap'):
    """\
    Returns a `ICableHandler` instance which writes XML Topic Maps syntax (XTM) 2.1.

    `fileobj`
        A file-like object.
    """
    return MIOCableHandler(create_xtm_miohandler(fileobj, title, comment))
    

class BaseMIOCableHandler(NoopCableHandler):
    """\
    Common base class for `ICableHandler` implementations which issue MIO events.

    This class keeps track of the currently processed cable and provides some utility
    methods to issue MIO events.
    """
    def __init__(self, handler):
        """\

        `handler`
            MIO event handler.
        """
        self._handler = simplify(handler)
        self._cable_psi = None
        self._cable_canonical_id = None
        self._cable_reference_id = None

    #
    # ICableHandler methods.
    #
    def start(self):
        self._handler.startTopicMap()
        
    def end(self):
        self._handler.endTopicMap()

    def start_cable(self, reference_id, canonical_id):
        self._cable_psi = psis.cable_psi(canonical_id)
        self._cable_reference_id = reference_id
        self._cable_canonical_id = canonical_id

    def end_cable(self):
        self._cable_psi, self._cable_reference_id, self._cable_canonical_id = None, None, None

    #
    # Protected methods
    #
    def _start_cable(self):
        h = self._handler
        h.startTopic(self._cable_psi)
        return h

    def _end_cable(self):
        self._handler.endTopic()
    
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


_is_dedicated_media_page = re.compile(r'https?://.+?/.+').match

class MIOCableHandler(BaseMIOCableHandler):
    """\
    Implementation of a `ICableHandler` which translates the events into
    MIO events (c.f. <https://mappa.googlecode.com/hg/tm/tm/mio/handler.py>_)
    """
    def __init__(self, handler):
        """\

        `handler`
            MIO event handler.
        """
        super(MIOCableHandler, self).__init__(handler)
        self._ref_counter = 0

    #
    # ICableHandler methods.
    #
    def start_cable(self, reference_id, canonical_id):
        super(MIOCableHandler, self).start_cable(reference_id, canonical_id)
        self._start_cable().isa(psis.CABLE_TYPE)
        self._name(canonical_id)
        self._name(reference_id, psis.REFERENCE_TYPE)

    def end_cable(self):
        super(MIOCableHandler, self).end_cable()
        self._end_cable()

    def handle_tag(self, tag):
        self._assoc(psis.TAGGED_TYPE,
                    psis.CABLE_TYPE, self._cable_psi,
                    psis.TAG_TYPE, psis.tag_psi(tag))
   
    def handle_origin(self, origin):
        self._sent_by(psis.origin_psi(origin), self._cable_psi)
    
    def handle_recipient(self, recipient):
        self._handle_recipient(psis.RECIPIENT_TYPE, recipient)

    def handle_info_recipient(self, recipient):
        self._handle_recipient(psis.INFO_RECIPIENT_TYPE, recipient)

    def _handle_recipient(self, typ, recipient):
        """\

        """
        route, name, precedence, mcn = recipient.route, recipient.name, recipient.precedence, recipient.mcn
        if not name:
            return
        h = self._handler
        h.startAssociation(typ)
        h.role(psis.CABLE_TYPE, self._cable_psi)
        h.role(psis.RECIPIENT_TYPE, psis.station_psi(name, route))
        if route:
            h.role(psis.ROUTE_TYPE, psis.route_psi(route))
        if precedence:
            h.role(psis.PRECEDENCE_TYPE, psis.precedence_psi(precedence))
        if mcn:
            h.role(psis.MCN_TYPE, psis.mcn_psi(mcn))
        h.endAssociation()

    def handle_reference(self, reference):
        enum = reference.bullet
        reifier = None
        if enum:
            self._ref_counter+=1
            reifier = mio.ITEM_IDENTIFIER, u'#%s-ref-%s' % (self._cable_canonical_id, self._ref_counter)
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
                    psis.SOURCE_TYPE, self._cable_psi,
                    psis.TARGET_TYPE, cable_ref,
                    reifier)
        handler.startTopic(cable_ref)
        handler.isa(psis.CABLE_TYPE)
        self._name(reference.value)
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

    def handle_content(self, content):
        self._occ(content, psis.CONTENT_TYPE)

    def handle_summary(self, summary):
        self._occ(summary, psis.SUMMARY_TYPE)

    def handle_comment(self, comment):
        self._occ(comment, psis.COMMENT_TYPE)

    def handle_classification(self, classification):
        for cls in psis.classification_psis(classification):
            self._assoc(psis.CLASSIFIED_AS_TYPE,
                        psis.CABLE_TYPE, self._cable_psi,
                        psis.CLASSIFICATION_TYPE, cls)

    def handle_classificationist(self, classificationist):
        pass #TODO

    def handle_classification_category(self, category):
        pass #TODO

    def handle_nondisclosure_deadline(self, date):
        self._occ(date, psis.NONDISCLOSURE_DEADLINE_TYPE, XSD.date)

    def handle_creation_datetime(self, datetime):
        self._occ(datetime, psis.CREATED_TYPE, XSD.dateTime)

    def handle_release_date(self, date):
        self._occ(date, psis.RELEASED_TYPE, XSD.date)

    def handle_partial(self, partial):
        if partial:
            self._assoc(psis.IS_PARTIAL_TYPE,
                        psis.PARTIAL_TYPE, self._cable_psi)

    def handle_wikileaks_iri(self, iri):
        self._handler.subjectLocator(iri)

    def handle_signer(self, signer):
        self._assoc(psis.SIGNED_TYPE,
                    psis.CABLE_TYPE, self._cable_psi,
                    psis.SIGNER_TYPE, psis.signer_psi(signer, self._cable_canonical_id))
            

    def handle_media_iri(self, iri):
        if _is_dedicated_media_page(iri):
            resource = mio.SUBJECT_LOCATOR, iri
            self._assoc(psis.COVERED_BY_TYPE,
                        psis.CABLE_TYPE, self._cable_psi,
                        psis.COVERED_BY_RESOURCE_TYPE, resource)
            self._assoc(psis.PUBLISHED_TYPE,
                        psis.PUBLISHED_RESOURCE_TYPE, resource,
                        psis.PUBLISHER_TYPE, psis.publisher_psi(iri))
        else:
            self._assoc(psis.COVERED_BY_TYPE,
                        psis.CABLE_TYPE, self._cable_psi,
                        psis.MEDIA_TYPE, psis.publisher_psi(iri))

    #
    # Private methods
    #
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


_find_title = re.compile(r'<title>(.+?)</title>', re.DOTALL).search
_find_meta_encoding = re.compile(r'''<meta[^>]+charset=['"]?(.*?)['"]?\s*/?\s*>''', re.IGNORECASE).search

class _Request(urllib2.Request):
    def __init__(self, url):
        urllib2.Request.__init__(self, url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
                                                     'Accept-Encoding': 'gzip, identity'})

# Source: <http://effbot.org/zone/re-sub.htm#unescape-html>
def _unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def _normalize_ws(text):
    return re.sub(r'[ ]{2,}', ' ', re.sub(r'[\r\n]+', ' ', text))


class MediaTitleResolver(BaseMIOCableHandler):
    """\
    Creates topics with subject locators from media IRIs and assigns a name to them.

    Requires an Internet connection.
    """
    def __init__(self, handler):
        """\

        `handler`
            MIO event handler.
        """
        super(MediaTitleResolver, self).__init__(handler)
        self._seen_iris = set()

    def end(self):
        super(MediaTitleResolver, self).end()
        self._seen_iris = None

    def handle_media_iri(self, iri):
        def fetch_url(url):
            resp = urllib2.urlopen(_Request(url))
            encoding = resp.headers.getparam('charset')
            if resp.info().get('Content-Encoding') == 'gzip':
                res = gzip.GzipFile(fileobj=StringIO(resp.read())).read()
            else:
                res = resp.read()
            if not encoding:
                m = _find_meta_encoding(res)
                if m:
                    encoding = m.group(1)
            if encoding:
                return res.decode(encoding)
            return res

        def find_name(page):
            m = _find_title(page)
            return _normalize_ws(_unescape(m.group(1).strip())) if m else None
            
        if iri in self._seen_iris or not _is_dedicated_media_page(iri):
            return
        try:
            page = fetch_url(iri)
        except urllib2.HTTPError, ex:
            logger.debug(ex)
            return
        except ValueError, ex: # Encoding error
            logger.debug(ex)
            return
        finally:
            self._seen_iris.add(iri)
        name = find_name(page)
        if name:
            h = self._handler
            h.startTopic((mio.SUBJECT_LOCATOR, iri))
            h.name(name)
            h.endTopic()

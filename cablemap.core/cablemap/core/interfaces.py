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
Documentation interfaces.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
try:
    from zope.interface import Interface, Attribute, implements
except ImportError:
    class Interface(object): 
        def __init__(self, descr): pass
    class Attribute(object):
        def __init__(self, descr): pass
    def implements(i): pass

class ICable(Interface):
    """\

    """
    reference_id = Attribute("""\
    Returns the WikiLeaks reference identifier (a string).

    This attribute is read-only.
    """)
    canonical_id = Attribute("""\
    Returns the unique canonical identifier of the cable (a string).

    This attribute is read-only.
    """)
    origin = Attribute("""\
    Sets/returns the origin of the cable (a string).

    This attribute is writable.
    """)
    header = Attribute("""\
    Sets/returns the header of the cable (a string).

    This attribute is writable.
    """)
    content  = Attribute("""\
    Sets/returns the content of the cable (a string).

    This attribute is writable.
    """)
    created = Attribute("""\
    Sets/returns the creation date of the cable (a string).

    This attribute is writable.
    """)
    released = Attribute("""\
    Sets/returns the WikiLeaks' date of the cable (a string).

    This attribute is writable.
    """)
    media_uris = Attribute("""\
    Sets/returns an iterable of media IRIs which cover this cable.

    This attribute is writable.
    """)
    wl_uris = Attribute("""\
    Returns cable IRIs to WikiLeaks (mirrors) (a list).

    This attribute is read-only.
    """)
    transmission_id = Attribute("""\
    The transmission identifier (a string) of the cable or ``None``.

    This attribute is read-only.
    """)
    recipients = Attribute("""\
    The recipients of the cable.

    Returns a maybe empty iterable of action `cablemap.core.interfaces.IRecipient` instances.

    C.f. `5 FAH-2 H-233 <http://www.state.gov/documents/organization/89293.pdf>`_

    This attribute is read-only.
    """)
    info_recipients = Attribute("""\
    Returns a maybe empty iterable of info `cablemap.core.interfaces.IRecipient` instances.

    C.f. `5 FAH-2 H-233 <http://www.state.gov/documents/organization/89293.pdf>`_

    This attribute is read-only.
    """)
    partial = Attribute("""\
    Indicates if this cable is only partially available (a boolean).

    This attribute is read-only.
    """)
    subject = Attribute("""\
    The (maybe empty string) subject.

    This attribute is read-only.
    """)
    classification = Attribute("""\
    The classification level.

    This attribute is writable.
    """)
    classification_categories = Attribute("""\
    Returns a maybe empty iterable of classification categories.

    A classification level is represented as an uppercased char (A-H)

    C.f. `5 FAH-3 H-700 <http://www.state.gov/documents/organization/89254.pdf>`_:

        * 1.4(a) military plans, weapons systems, or operations;
        * 1.4(b) foreign government information*;
        * 1.4(c) intelligence activities, sources, or methods, or cryptology;
        * 1.4(d) foreign relations or foreign activities of the United States,
          including confidential sources;
        * 1.4(e) scientific, technological or economic matters relating to national security;
          which includes defense against transnational terrorism;
        * 1.4(f) USG programs for safeguarding nuclear materials or facilities;
        * 1.4(g) vulnerabilities or capabilities of systems, installations, infrastructures,
          projects or plans, or protection services relating to the national security,
          which includes defense against transnational terrorism; and
        * 1.4(h) weapons of mass destruction.

    This attribute is read only.
    """)
    nondisclosure_deadline = Attribute("""\
    The non-disclosure deadline or ``None`` if it is unknown.

    This attribute is read-only.
    """)
    references = Attribute("""\
    A maybe empty iterable of `IReference` instances.
    """)
    tags = Attribute("""\
    A maybe empty iterable of TAGs (strings).

    This attribute is read-only.
    """)
    summary = Attribute("""\
    The summary of the cable or ``None``.

    This attribute is read-only.
    """)
    comment = Attribute("""\
    The comment of the author of the cable or ``None``.

    This attribute is read-only.
    """)
    signers = Attribute("""\
    A maybe empty iterable of signers of the cable.

    The signers are represented as string, i.e. ``'CLINTON'``

    This attribute is read-only.
    """)
    content_header = Attribute("""\
    The "header" part of the cable's content (everything before the
    first paragraph).

    This attribute is read-only.
    """)
    content_body = Attribute("""\
    The "body" part of the cable's content (everything from the
    first paragraph on).

    This attribute is read-only.
    """)

class IReference(Interface):
    """\
    Represents a reference to another cable, or e-mail message
    or any other referencable item.
    """
    def is_cable():
        """\
        Returns if this reference instance represents a reference to
        a cable.
        """
    value = Attribute("""\
    The reference, i.e. a cable identifier.

    This attribute is read-only.
    """)
    kind = Attribute("""\
    An integer.

    The type of the reference, i.e. ``CABLE``.

    This attribute is read-only.
    """)
    bullet = Attribute("""\
    A string or ``None``.

    If the reference is part of an enumeration, it should return something
    like ``A`` or ``1``.

    This attribute is read-only.
    """)
    title = Attribute("""\
    A string or ``None``.

    Title of the reference or ``None``.

    This attribute is read-only.
    """)

class IRecipient(Interface):
    """\
    Represents a recipient of a cable.
    """
    route = Attribute("""\
    A string or ``None``.

    The route.

    This attribute is read-only.
    """)
    name = Attribute("""\
    A string or ``None``.

    The name of the recipient (PLAD - Plain Language Address Designator).

    C.f. `5 FAH-2 H-321.6 <http://www.state.gov/documents/organization/89289.pdf>`_

    This attribute is read-only.
    """)
    excluded = Attribute("""\
    A list of recipient names which are excluded.

    This attribute is read-only.
    """)
    precedence = Attribute("""\
    A string or ``None``.

    Should be (acc. to `5 FAH-1 H-221 <http://www.state.gov/documents/organization/89318.pdf>`_):

        * FLASH
        * NIACT IMMEDIATE
        * IMMEDIATE
        * PRIORITY
        * ROUTINE

    This attribute is read-only.
    """)
    mcn = Attribute("""\
    A string or ``None``.

    C.f. `5 FAH-2 H-321.7, 5 FAH-2 H-321.8 <http://www.state.gov/documents/organization/89289.pdf>`_:

        Message continuity number (MCN). An MCN is a
        consecutive number from a series dedicated to each Department of State
        activity. You assign an MCN to the Department activity on each telegram
        sent to them, action or info.

    This attribute is read-only.
    """)


class ICableHandler(Interface):
    """\
    Defines an interface for classes which are capable to process one or more 
    cables.

    The first event is `start` and the last event must be `end`.
    Between these events one or more `start_cable`/`end_cable` events
    must occur. All subsequent events like `handle_subject` assign properties
    to the cable which was started by `start_cable`.

    ``None`` values are not accepted by handler. If something is ``None`` (like
    the subject), the event must not be issued.
    """

    def start():
        """\
        First event.
        """

    def end():
        """\
        Last event.
        """

    def start_cable(reference_id, canonical_id):
        """\
        Indicates the start of a cable.

        `reference_id`
            The WikiLeaks' identifier of the cable
        `canonical_id`
            The canonical identifier of the cable.
        """
        
    def end_cable():
        """\
        Indicates that the cable which was started by `start_cable`
        has been processed.
        """

    def handle_tag(tag):
        """\
        Adds a TAG to the cable.

        `tag`
            A string.
        """

    def handle_origin(origin):
        """\
        Assigns the cable's origin.

        `origin`
            A string.
        """
    
    def handle_recipient(recipient):
        """\
        Assigns a recipient to the cable.

        `recipient`
            A `IRecipient` instance.
        """

    def handle_info_recipient(recipient):
        """\
        Assigns an info recipient to the cable.

        `recipient`
            A `IRecipient` instance.
        """

    def handle_reference(reference):
        """\
        Assigns a cable reference. 

        Indicates that the `reference` is referenced by the current cable.

        `reference`
            A `IReference` instance.
        """
    
    def handle_subject(subject):
        """\
        Assigns the subject to the cable.

        `subject`
            A string.
        """

    def handle_signer(signer):
        """\
        Assigns a signer to the cable.

        `signer`
            A string, like ``'CLINTON'``
        """

    def handle_transmission_id(tid):
        """\
        Assigns the transmission id to the cable.

        `tid`
            A string.
        """

    def handle_header(header):
        """\
        Assigns the header to the cable.

        `header`
            A string.
        """

    def handle_body(body):
        """\
        Assigns the body to the cable.

        `body`
            A string.
        """

    def handle_summary(summary):
        """\
        Assigns the summary to the cable.

        `summary`
            A string.
        """

    def handle_comment(comment):
        """\
        Assigns the comment to the cable.

        `comment`
            A string.
        """

    def handle_classification(classification):
        """\
        Assigns the classification to the cable.

        `classification`
            An uppercased string.
        """

    def handle_classification_category(category):
        """\
        Assigns the classification category.

        `category`
            An uppercased char (A-H)
        """

    def handle_nondisclosure_deadline(date):
        """\
        Assigns the non-disclosure deadline to the cable.

        `date`
            `ISO 8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ formatted date
        """

    def handle_creation_datetime(datetime):
        """\
        Assigns the creation datetime to the cable.
        
        `datetime`
            `ISO 8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ formatted datetime
        """

    def handle_release_date(date):
        """\
        Assigns the WikiLeaks release date to the cable.

        `date`
            `ISO 8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ formatted date
        """

    def handle_partial(partial):
        """\
        Indicates that the whole cable text is (not) available.
        
        `partial`
            A boolean value, ``True`` indicates that the current cable is
            only partially available.
        """

    def handle_wikileaks_iri(iri):
        """\
        Assigns the provided WikiLeaks IRI to the cable.

        `iri`
            The IRI to add.
        """

    def handle_media_iri(iri):
        """\
        Assigns the provided IRI to the media coverage IRIs.

        `iri`
            The IRI to add.
        """

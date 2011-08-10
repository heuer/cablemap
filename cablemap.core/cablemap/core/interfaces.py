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
    from zope.interface import Interface, Attribute
except ImportError:
    class Interface(object): 
        def __init__(self, descr): pass
    class Attribute(object):
        def __init__(self, descr): pass

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

    Returns a maybe empty iterable of `IRecipient` instances.

    This attribute is read-only.
    """)
    info_recipients = Attribute("""\
    Returns a maybe empty iterable of `IRecipient` instances.

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
    name = Attribute("""\
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

    The name of the recipient.

    This attribute is read-only.
    """)
    excluded = Attribute("""\
    A list of recipient names which are excluded.

    This attribute is read-only.
    """)
    precedence = Attribute("""\
    A string or ``None``.

    Should be (acc. to 5 FAH-1 H-221):
    * FLASH
    * NIACT IMMEDIATE
    * IMMEDIATE
    * PRIORITY
    * ROUTINE

    This attribute is read-only.
    """)
    mcn = Attribute("""\
    A string or ``None``.

    5 FAH-2 H-321.7, 5 FAH-2 H-321.8:

    Message continuity number (MCN). An MCN is a
    consecutive number from a series dedicated to each Department of State
    activity. You assign an MCN to the Department activity on each telegram
    sent to them, action or info.

    This attribute is read-only.
    """)
    

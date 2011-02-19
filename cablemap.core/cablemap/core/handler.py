# -*- coding: utf-8 -*-
"""\
DEPRECATED

This module defines an event handler to process cables.
"""
import warnings

warnings.warn('Deprecated, use "cablemap.tm.handler"', DeprecationWarning)

#
# The following constants are taken from `tm.mio` and repeated here to
# avoid a dependency to the package `tm.mio`.
#
ITEM_IDENTIFIER = 1
"""\
Constant for an item identifier reference.
"""

SUBJECT_IDENTIFIER = 2
"""\
Constant for a subject identifier reference.
"""

SUBJECT_LOCATOR = 3
"""\
Constant for a subject locator reference.
"""

class CableHandler(object):
    """\
    Defines an interface for classes which are capable to process one or more 
    cables.

    The first event is `start` and the last event must be `end`.
    Between these events one or more `start_cable`/`end_cable` events
    must occur. All subsequent events like `handle_subject` assign properties
    to the cable which was started by `start_cable`.

    ``None`` values are not accepted by handler. If something is ``None`` (like
    the subject), the event must not be issued.
    
    ``identity`` is a tuple which consists of the "kind" of identity (subject
    identifier, subject locator, item identifier) and an absolute IRI, i.e. 
    ``(SUBJECT_IDENTIFIER, u'http://psi.example.org/cable/123')``
    """

    def start(self):
        """\
        First event.
        """
        pass
        
    def end(self):
        """\
        Last event.
        """
        pass

    def start_cable(self, identity):
        """\
        Indicates the start of a cable.

        `identity`
            The identitiy of the cable
            (subject identifier, subject locator, item identifier)
            Should be a subject identifier.
        """
        pass
        
    def end_cable(self):
        """\
        Indicates that the cable which was started by `start_cable`
        has been processed.
        """
        pass

    def handle_subject_locator(self, iri):
        """\
        Adds a subject identifier to the cable.

        `iri`
            An IRI which acts as subject identifier.
        """
        pass

    def handle_reference_id(self, reference_id):
        """\
        Assigns the reference ID to the current cable.

        `reference_id`
            A string.
        """
        pass
    
    def handle_tag(self, identity):
        """\
        Adds a TAG to the cable.

        `identity`
            A subject identifier, subject locator, or item identifier.
            Commonly a subject identifier.
        """
        pass
   
    def handle_origin(self, identity):
        """\
        Assigns the cable's origin.

        `identity`
            A subject identifier, subject locator, or item identifier.
            Commmonly a subject identifier.
        """
        pass
    
    def handle_recipient(self, identity):
        """\
        Assigns a recipient to the cable.

        `identity`
            A subject identifier, subject locator, or item identifier.
            Commonly a subject identifier.
        """
        pass

    def handle_info_recipient(self, identity):
        """\
        Assigns an info recipient to the cable.

        `identity`
            A subject identifier, subject locator, or item identifier.
            Commonly a subject identifier.
        """
        pass

    def handle_reference(self, identity):
        """\
        Assigns a cable reference to the cable. 

        Indicates that the cable identified by `identity` is referenced by
        the current cable.

        `identity`
            A subject identifier, subject locator, or item identifier.
            Commonly a subject identifier.
        """
        pass
    
    def handle_subject(self, subject):
        """\
        Assigns the subject to the cable.

        `subject`
            A string.
        """
        pass

    def handle_transmission_id(self, tid):
        """\
        Assigns the transmission id to the cable.

        `tid`
            A string.
        """
        pass

    def handle_header(self, header):
        """\
        Assigns the header to the cable.

        `header`
            A string.
        """
        pass

    def handle_body(self, body):
        """\
        Assigns the body to the cable.

        `body`
            A string.
        """
        pass

    def handle_summary(self, summary):
        """\
        Assigns the summary to the cable.

        `summary`
            A string.
        """
        pass

    def handle_classification(self, identity):
        """\
        Assigns the classification to the cable.

        `identity`
            A subject identifier, subject locator, or item identifier.
            Commonly a subject identifier.
        """
        pass

    def handle_nondisclosure_deadline(self, date):
        """\
        Assigns the non-disclosure deadline to the cable.

        `date`
            ISO 8601 formatted date
        """
        pass

    def handle_creation(self, datetime):
        """\
        Assigns the creation datetime to the cable.
        
        `datetime`
            ISO 8601 formatted datetime
        """
        pass

    def handle_release(self, datetime):
        """\
        Assigns the Wikileaks release datetime to the cable.

        `datetime`
            ISO 8601 formatted datetime
        """
        pass

    def handle_partial(self, partial):
        """\
        Indicates that the whole cable text is (not) available.
        
        Implementations of this interface should assume that this method 
        is not called if the cable is *not* partial and therfore assume that
        the current cable is complete.
        
        `partial`
            A boolean value, ``True`` indicates that the current cable is
            only partially available.
        """
        pass

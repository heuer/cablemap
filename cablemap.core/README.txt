==============================================
Cablemap - A Cablegate to Topic Maps converter
==============================================


Cablemap - The core package
---------------------------
The core package provides utilities which can be used to extract information
from diplomatic cables::

    >>> from cablemap.core import cable_from_html
    >>> from cablemap.core.cableutils import cable_page_by_id, cable_to_json
    >>> 
    >>> rid = '09BERLIN1167'
    >>> # Fetches the cable with the reference id '09BERLIN1167' from the Internet
    >>> page = cable_page_by_id(rid)
    >>> # Converts the HTML page into a cable object
    >>> cable = cable_from_html(page, rid)
    >>> cable.reference_id
    '09BERLIN1167'
    >>> cable.subject
    u'DATA PRIVACY TRUMPS SECURITY: IMPLICATIONS OF A FDP VICTORY ON COUNTERTERRORISM COOPERATION'
    >>> json = cable_to_json(cable)
    >>> 

The core package has no Topic Maps related code and can be used independently 
of the other packages.

For other examples see: https://github.com/heuer/cablemap/tree/master/examples

==============================================
Cablemap - A Cablegate to Topic Maps converter
==============================================


Cablemap - The core package
---------------------------
The core package provides utilities which can be used to extract information
from diplomatic cables::

    >>> from cablemap.core import cable_by_id
    >>> from cablemap.core.utils import cable_to_json
    >>> 
    >>> # Fetches the cable with the reference id '09BERLIN1167' from the Internet
    >>> # and converts it into a Cable object
    >>> cable = cable_by_id('09BERLIN1167')
    >>> cable.reference_id
    u'09BERLIN1167'
    >>> cable.subject
    u'DATA PRIVACY TRUMPS SECURITY: IMPLICATIONS OF A FDP VICTORY ON COUNTERTERRORISM COOPERATION'
    >>> json = cable_to_json(cable)
    >>> 

The core package has no Topic Maps related code and can be used independently 
of the other packages.

For other examples see: https://github.com/heuer/cablemap/tree/master/examples

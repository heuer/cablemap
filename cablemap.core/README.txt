==============================================
Cablemap - A Cablegate to Topic Maps converter
==============================================


Cablemap - The core package
---------------------------
The core package provides utilities which can be used to extract information
from diplomatic cables::

    >>> from cablemap.core import cable_by_id
    >>> from cablemap.core.utils import cable_to_json, titlefy
    >>> 
    >>> # Fetches the cable with the reference id '09BERLIN1167' from the Internet
    >>> # and converts it into a Cable object
    >>> cable = cable_by_id('09BERLIN1167')
    >>> cable.reference_id
    u'09BERLIN1167'
    >>> cable.subject
    u'DATA PRIVACY TRUMPS SECURITY: IMPLICATIONS OF A FDP VICTORY ON COUNTERTERRORISM COOPERATION'
    >>> # Generate a more readable subject
    >>> titlefy(cable.subject)
    u'Data Privacy Trumps Security: Implications of a FDP Victory on Counterterrorism Cooperation'
    >>> json = cable_to_json(cable)
    >>> 

The core package has no Topic Maps related code and can be used independently 
of the other packages.

For other examples see: https://github.com/heuer/cablemap/tree/master/examples


Installation
------------
cablemap.core 0.2.0 is the current stable release. To install it, use::

    easy_install -U cablemap.core==0.2.0

cablemap.core 0.3.0 is the unstable, next release; install it via::

    easy_install -U cablemap.core

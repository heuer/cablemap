==============================================
Cablemap - A Cablegate to Topic Maps converter
==============================================


What is Cablemap?
-----------------
Cablemap converts the Wikileaks Cablegate dataset into Topic Maps. Further, 
it provides utilities to extract information from the Cablegate dataset 
independently of Topic Maps.


Getting started
---------------
Even if you don't know Topic Maps or don't care about Topic Maps, Cablemap 
can help to extract useful information from the diplomatic cables. Several 
modules like the ``reader.py`` module are independent of Topic Maps and 
provide a convenient interface to the cable information.

To get started with Cablemap, look into the ``cablemap.core`` package which 
provides utilities to convert cable HTML sources into cable objects and a 
translation of cables into JSON.


Disclaimer
----------
Cablemap is not a mirror and has no ties to Wikileaks. 
It provides just a parser to read published cables which are already widely 
available on the web.

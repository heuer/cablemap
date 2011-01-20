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
translation of cables into JSON and YAML.


License
-------
Copyright (c) 2011 -- Lars Heuer - <heuer[at]semagia.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * Neither the project name nor the names of the contributors may be 
      used to endorse or promote products derived from this software 
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
Several REF parsing tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

_TEST_DATA = (
        (u'01VATICAN5095', [u'99ROME2196']),
        ('04THEHAGUE1919', [u'04USEUBRUSSELS3226']),
        ('05BRASILIA1851', [u'05STATE127529', u'05STATE110840', u'05USUNNEWYORK1442']),
        ('05PORTAUPRINCE1609', [u'05PORTAUPRINCE1537', u'05TOKYO3020', u'05OSLO868', u'05OTTAWA1734']),
        ('06PORTAUPRINCE2187', [u'06PORTAUPRINCE1734', u'06PORTAUPRINCE1561']),
        ('06SANJOSE2734', [u'06STATE19152', u'06SANJOSE2223', u'06SANJOSE1955']),
        ('07LIMA2129', [u'07LIMA1841', u'07LIMA2000', u'07LIMA2009', u'07LIMA2026']),
        ('07LIMA2323', [u'07LIMA2000', u'07LIMA2009', u'07LIMA2126', u'07LIMA2236']),
        ('04HALIFAX40', [u'03OTTAWA1924', u'03OTTAWA566', u'03OTTAWA503', u'03HALIFAX58', u'02OTTAWA3205']),

    )


def test_references():
    def check(cable_id, references):
        cable = cable_by_id(cable_id)
        assert cable
        eq_(references, cable.references)
    for cable_id, refs in _TEST_DATA:
        yield check, cable_id, refs
    

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

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
Tests non-disclosure deadline parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from cablemap.core.reader import parse_nondisclosure_deadline

def test_nondisclosure_deadline():
    """

    >>> parse_nondisclosure_deadline('DEPT FOR WHA/BSC E.O. 12958: DECL: 11/22/2012 ')
    u'2012-11-22'
    >>> parse_nondisclosure_deadline('EO 12958 DECL: 2020/02/23')
    u'2020-02-23'
    >>> parse_nondisclosure_deadline('E.O. 12958: DECL: 11/03/2015')
    u'2015-11-03'
    >>> parse_nondisclosure_deadline('EO 12958 DECL: 12/31/2034')
    u'2034-12-31'
    >>> parse_nondisclosure_deadline('E.O. 12958 DECL: 12/31/2034')
    u'2034-12-31'
    >>> parse_nondisclosure_deadline('E.o. 12958: decl: 07/01/2034')
    u'2034-07-01'
    >>> parse_nondisclosure_deadline(u'E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu Subject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?\\n\\n(U) Classifi')
    u'2014-01-07'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 12/31/2034')
    u'2034-12-31'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 6/30/08')
    u'2008-06-30'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 6/3/08')
    u'2008-06-03'
    >>> parse_nondisclosure_deadline(u'EO 12958: decl: 06/30/08')
    u'2008-06-30'
    >>> parse_nondisclosure_deadline(u'E.O. 12958: N/A') is None
    True
    """

if __name__ == '__main__':
    import doctest
    doctest.testmod()

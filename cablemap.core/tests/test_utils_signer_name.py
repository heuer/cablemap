# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2012 -- Lars Heuer <heuer[at]semagia.com>
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
Tests cablemap.core.utils.signer_name.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.utils import signer_name

_TEST_DATA = (
    (u'98STATE1234', u'ALBRIGHT', u'Madeleine Korbel Albright'),
    (u'98ABUDHABI1234', u'ALBRIGHT', u'Richard A. Albright'),
    (u'98BERLIN1234', u'ALBRIGHT', None),
    (u'01KUWAIT1234', u'JONES', u'Richard Henry Jones'),
    (u'08KUWAIT1234', u'JONES', u'Deborah K. Jones'),

)

def test_name():
    def check(sign, canonical_id, expected):
        eq_(expected, signer_name(sign, canonical_id))
    for canonical_id, sign, expected in _TEST_DATA:
        yield check, sign, canonical_id, expected

def test_default():
    eq_('bar', signer_name(u'FOO', u'98BERLIN1234', 'bar'))
    eq_(None, signer_name(u'FOO', u'98BERLIN1234'))
    eq_(u'FOO', signer_name(u'FOO', u'98BERLIN1234', u'FOO'))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

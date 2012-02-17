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
Tests the handling of invalid WikiLeaks cable ids.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import ok_, eq_
from cablemap.core import cable_by_id, c14n
from cablemap.core.constants import INVALID_CABLE_IDS

def _get_test_cases():
    return INVALID_CABLE_IDS.iteritems()

def test_from_invalid_cable_id():
    def check(incorrect_id, correct_id):
        cable = cable_by_id(incorrect_id)
        ok_(cable is not None)
        eq_(incorrect_id, cable.reference_id)
        eq_(c14n.canonicalize_id(incorrect_id), cable.canonical_id, 'Unexpected canonical identifier for the incorrect id')
        eq_(c14n.canonicalize_id(correct_id), cable.canonical_id, 'Unexpected canonical identifier for the correct id')
    for incorrect_id, correct_id in _get_test_cases():
        yield check, incorrect_id, correct_id

def test_to_invalid_cable_id():
    def check(incorrect_id, correct_id):
        cable = cable_by_id(correct_id)
        ok_(cable is not None)
        eq_(incorrect_id, cable.reference_id)
        eq_(c14n.canonicalize_id(incorrect_id), cable.canonical_id, 'Unexpected canonical identifier for the incorrect id')
        eq_(c14n.canonicalize_id(correct_id), cable.canonical_id, 'Unexpected canonical identifier for the correct id')
    for incorrect_id, correct_id in _get_test_cases():
        yield check, incorrect_id, correct_id



if __name__ == '__main__':
    import nose
    nose.core.runmodule()

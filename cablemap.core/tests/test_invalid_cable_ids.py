# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
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

# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
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

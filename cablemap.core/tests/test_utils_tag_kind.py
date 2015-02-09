# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests cablemap.core.utils.tag_kind

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.utils import tag_kind
from cablemap.core import constants as consts

_TEST_DATA = (
    (u'KIPR', consts.TAG_KIND_PROGRAM),
    (u'kwww', consts.TAG_KIND_PROGRAM),
    (u'OBAMA, BARACK', consts.TAG_KIND_PERSON),
    (u'GE', consts.TAG_KIND_GEO),
    (u'NASA', consts.TAG_KIND_ORG),
    (u'ECON', consts.TAG_KIND_SUBJECT),
    (u'PHUM', consts.TAG_KIND_SUBJECT),
    (u'UNKNOWN', consts.TAG_KIND_UNKNOWN),
    (u'phum', consts.TAG_KIND_SUBJECT),
    (u"BA'ATH", consts.TAG_KIND_ORG),
)

def test_tag_kind():
    def check(tag, expected):
        eq_(expected, tag_kind(tag))
    for tag, expected in _TEST_DATA:
        yield check, tag, expected

def test_tag_kind_default():
    eq_(consts.TAG_KIND_UNKNOWN, tag_kind('THIS IS UNKNOWN'))
    eq_(consts.TAG_KIND_SUBJECT, tag_kind('THIS IS UNKNOWN', consts.TAG_KIND_SUBJECT))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

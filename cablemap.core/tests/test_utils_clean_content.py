# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests cablemap.core.utils.clean_content

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
import os
import codecs
from nose.tools import eq_
from cablemap.core.utils import clean_content

_DATA_DIR = 'data-clean'

_TEST_DATA = (
    ('gentlexxx', u'gentle'),
    ('xx', ''),
)

def test_clean():
    def check(content, expected):
        eq_(expected, clean_content(content))
    for content, expected in _TEST_DATA:
        yield check, content, expected

def test_cleaning():
    def check(expected, input):
        eq_(expected, clean_content(input))
    base = os.path.join(os.path.dirname(__file__), _DATA_DIR)
    for name in [name for name in os.listdir(os.path.join(base, 'in')) if name.endswith('.txt')]:
        input = codecs.open(os.path.join(base, 'in', name), 'rb', 'utf-8').read()
        expected = codecs.open(os.path.join(base, 'out', name), 'rb', 'utf-8').read()
        yield check, expected, input


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

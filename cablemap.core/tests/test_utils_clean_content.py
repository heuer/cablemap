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

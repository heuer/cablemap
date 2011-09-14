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
    (u'OBAMA, BARACK', consts.TAG_KIND_PERSON),
    (u'GE', consts.TAG_KIND_GEO),
    (u'NASA', consts.TAG_KIND_ORG),
    (u'ECON', consts.TAG_KIND_SUBJECT),
    (u'PHUM', consts.TAG_KIND_SUBJECT),
    (u'UNKNOWN', consts.TAG_KIND_UNKNOWN),
    (u'phum', consts.TAG_KIND_UNKNOWN),
    (u"BA'ATH", consts.TAG_KIND_ORG),
)

def test_tag_kind():
    def check(tag, expected):
        eq_(expected, tag_kind(tag))
    for tag, expected in _TEST_DATA:
        yield check, tag, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

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
Tests against ``cablemap.nlp.texttools``.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
import cablemap.nlp.texttools as tt

_DATA = (
        '''I've been waiting. I've been waiting night and day.''',
        '''I'VE BEEN WAITING. I'VE BEEN WAITING NIGHT AND DAY.''',
        '''you are will I be''',
        )

_WORDS_RESULTS = (
    ['waiting', 'waiting', 'night', 'day'],
    ['WAITING', 'WAITING', 'NIGHT', 'DAY'],
    [],
    )

_LOWERCASED_WORDS_RESULTS = (
    ['waiting', 'waiting', 'night', 'day'],
    ['waiting', 'waiting', 'night', 'day'],
    [],
    )

_SENT_RESULTS = (
    ['''I've been waiting.''', '''I've been waiting night and day.'''],
    ['''I'VE BEEN WAITING.''', '''I'VE BEEN WAITING NIGHT AND DAY.'''],
    ['you are will I be'],
    )

_FREQ_DIST_RESULTS = (
    {'waiting': 2, 'night': 1, 'day': 1},
    {'WAITING': 2, 'NIGHT': 1, 'DAY': 1},
    {},
    )

def test_words():
    def check(content, words):
        eq_(words, list(tt.words(content)))
    for i, c in enumerate(_DATA):
        yield check, c, _WORDS_RESULTS[i]

def test_lowercased_words():
    def check(content, words):
        eq_(words, list(tt.lowercased_words(content)))
    for i, c in enumerate(_DATA):
        yield check, c, [w.lower() for w in _WORDS_RESULTS[i]]

def test_sent_list():
    def check(content, sentences):
        eq_(sentences, tt.sentence_list(content))
    for i, c in enumerate(_DATA):
        yield check, c, _SENT_RESULTS[i]

def test_freqdist():
    def check(words, fq):
        eq_(sorted(fq.iteritems()), sorted(tt.freq_dist(words).iteritems()))
    for i, c in enumerate(_DATA):
        yield check, tt.words(c), _FREQ_DIST_RESULTS[i]

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

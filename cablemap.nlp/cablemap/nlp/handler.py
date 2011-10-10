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
Event handler to create a cable corpus.
"""
from __future__ import absolute_import
from cablemap.core.handler import NoopCableHandler
from .corpus import CableCorpus

class CorpusWriter(NoopCableHandler):
    """\
    Creates a cable corpus.
    """
    def __init__(self, path, prefix=None, dct=None, tokenizer=None, allow_dict_updates=True):
        """\

        `path`
            Directory where the generated files are stored.
        `prefix`
            A prefix for the generated file names.
        `dct`
            An existing `gensim.corpora.dictionary.Dictionary`
            If it's ``None`` (default) a dictionary will be created.
        `tokenizer`
            A function to tokenize/normalize/clean-up strings.
            If it's ``None`` (default), a default function will be used to tokenize
            texts.
        `allow_dict_updates`
            Indicats if unknown words should be added to the dictionary (default ``True``).
        """
        self._corpus = CableCorpus(path, prefix, dct, tokenizer, allow_dict_updates)
        self._reference_id = None
        self._buff = []

    def end(self):
        self._corpus.close()

    def start_cable(self, reference_id, canonical_id):
        self._reference_id = reference_id

    def end_cable(self):
        self._corpus.add_texts(self._reference_id, self._buff)
        self._buff = []

    def handle_subject(self, s):
        self._buff.append(s)

    def handle_summary(self, s):
        self._buff.append(s)

    def handle_comment(self, s):
        self._buff.append(s)

    def handle_header(self, s):
        self._buff.append(s)

    def handle_content(self, s):
        self._buff.append(s)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

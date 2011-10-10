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
Cable corpus.
"""
import os
from itertools import chain, count
from gensim.corpora.dictionary import Dictionary
from gensim import utils
try:
    import json
except ImportError:
    import simplejson as json
from .utils import IncrementalMmWriter


class CableCorpus(object):
    """\

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
            A function to tokenize/normalize/clean-up/remove stop words from strings.
            If it's ``None`` (default), a default function will be used to tokenize texts.
        `allow_dict_updates`
            Indicats if unknown words should be added to the dictionary (default ``True``).
        """
        def tokenize(text):
            return utils.tokenize(text, lowercase=True)
        if not os.path.isdir(path):
            raise IOError('Expected a directory path')
        self.dct = dct or Dictionary()
        self._path = path
        self._prefix = prefix or 'cables_'
        self._tokenize = tokenizer or tokenize
        self._mw = IncrementalMmWriter(os.path.join(path, self._prefix + 'bow.mm'))
        self.allow_dict_updates = allow_dict_updates
        self._cables = []

    def add_texts(self, reference_id, texts):
        """\

        `reference_id`
            The reference identifier of the cable.
        `texts`
            An iterable of strings.
        """
        self.add_words(reference_id, chain(*(self._tokenize(t) for t in texts)))

    def add_text(self, reference_id, text):
        """\

        `reference_id`
            The reference identifier of the cable.
        `text`
            An string.
        """
        self.add_words(reference_id, self._tokenize(text))

    def add_words(self, reference_id, words):
        """\

        `reference_id`
            The reference identifier of the cable.
        `words`
            An iterable of words.
        """
        self._cables.append(reference_id)
        self._mw.add_vector(self.dct.doc2bow(words, self.allow_dict_updates))

    def close(self):
        self._mw.close()
        self.dct.save_as_text(os.path.join(self._path, self._prefix + 'wordids.txt'))
        json_filename = os.path.join(self._path, self._prefix + 'id2docid.json')
        json.dump(dict(zip(self._cables, count())), open(json_filename, 'wb'))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

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
    The cable corpus consists of several files which are written into a directory.

    * a dictionary with a ``<word id> <word> <frequency>`` mapping saved under "wordids.txt"
    * a JSON file with a ``<cable reference id> <document number>`` mapping under "id2docid.json"
    * a `Market Matrix format <http://math.nist.gov/MatrixMarket/formats.html>` vector space model file "bow.mm"

    CAUTION: The corpus overrides any existing files with the same file name in the specified directory.

    By default, the corpus creates the word dictionary and the vector space model which
    may lead into an unuseful vector space model. To filter certain words, the corpus may be
    initialized with a pre-generated word dictionary. To make the dictionary immutable, the property
    ``allow_dict_updates`` should be set to ``False`` (updates are allowed by default).
    The resulting vector space model contains only words which are in the word dictionary then.

    Example to reduce the clutter::

        corpus = CableCorpus('/my/directory/')
        # Add some texts here
        corpus.add_text('ref-1', u'bla bla bla')
        corpus.add_text('ref-2', u'bla bla blub')
        ...
        corpus.dct.filter_extremes()
        corpus.close()

        from gensim.corpora.dictionary import Dictionary

        # Load previously created dict
        dct = Dictionary.load_from_text('/my/directory/cables_wordids.txt')
        # Create another corpus with the previously word dict
        corpus = CableCorpus('/my/directory/', dct, allow_dict_updates=False)
        # Add some texts
        ....
        corpus.close()
    """
    def __init__(self, path, prefix=None, dct=None, tokenizer=None, allow_dict_updates=True):
        """\
        Initializes the cable corpus.
        
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
            #TODO: clean-up, remove stop words, remove SIPDIS, PAGE info, add a stemmer etc... 
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
        Adds the words from the provided iterable `texts` to the corpus.

        The strings will be tokenized.

        `reference_id`
            The reference identifier of the cable.
        `texts`
            An iterable of strings.
        """
        self.add_words(reference_id, chain(*(self._tokenize(t) for t in texts)))

    def add_text(self, reference_id, text):
        """\
        Adds the words from the provided text to the corpus.

        The string will be tokenized.

        `reference_id`
            The reference identifier of the cable.
        `text`
            An string.
        """
        self.add_words(reference_id, self._tokenize(text))

    def add_words(self, reference_id, words):
        """\
        Adds the words to the corpus. The words won't be tokenized/fitered.

        `reference_id`
            The reference identifier of the cable.
        `words`
            An iterable of words.
        """
        self._cables.append(reference_id)
        self._mw.add_vector(self.dct.doc2bow(words, self.allow_dict_updates))

    def close(self):
        """\
        This method MUST be called after all texts/words have been added
        to the corpus.
        """
        self._mw.close()
        self.dct.save_as_text(os.path.join(self._path, self._prefix + 'wordids.txt'))
        json_filename = os.path.join(self._path, self._prefix + 'id2docid.json')
        json.dump(dict(zip(self._cables, count())), open(json_filename, 'wb'))


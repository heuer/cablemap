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
Experimental script to create a corpus, similar to gensim.corpora.wikicorpus

TODO: Support user input
"""
from __future__ import absolute_import
import os
from gensim.models import TfidfModel
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.mmcorpus import MmCorpus
from cablemap.core import handle_source, predicates as pred
from cablemap.nlp.handler import NLPFilter, DictionaryHandler, CorpusHandler

_DEFAULT_KEEP_WORDS=10000

def create_filter(handler):
    return NLPFilter(handler, want_content=True, want_summary=False, want_comment=False, want_tags=False)

def create_corpus(src, out_dir, no_below=20, keep_words=_DEFAULT_KEEP_WORDS):
    """\

    """
    wordid_filename = os.path.join(out_dir, 'cables_wordids.pickle')
    bow_filename = os.path.join(out_dir, 'cables_bow.mm')
    tfidf_filename = os.path.join(out_dir, 'cables_tfidf.mm')
    predicate = None # Could be set to something like pred.origin_filter(pred.origin_germany)
    # 1. Create word dict
    dct = Dictionary()
    dct_handler = DictionaryHandler(dct)
    handler = create_filter(dct_handler)
    handle_source(src, handler, predicate)
    dct.filter_extremes(no_below=no_below, no_above=0.1, keep_n=keep_words)
    dct.save(wordid_filename)
    # 2. Reiterate through the cables and create the vector space
    corpus_handler = CorpusHandler(out_dir, dct=dct, allow_dict_updates=False)
    handler = create_filter(corpus_handler)
    handle_source(src, handler, predicate)
    # 3. Load corpus
    mm = MmCorpus(bow_filename)
    # 4. Create TF-IDF model
    tfidf = TfidfModel(mm, id2word=dct, normalize=True)
    # 5. Save the TF-IDF model
    MmCorpus.serialize(tfidf_filename, tfidf[mm], progress_cnt=10000)

if __name__ == '__main__':
    create_corpus('cables.csv', './corpus/')


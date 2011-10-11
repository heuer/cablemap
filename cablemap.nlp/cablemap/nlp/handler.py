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
from cablemap.core.handler import NoopCableHandler, DelegatingCableHandler
from .corpus import WordCorpus, CableCorpus

class NLPFilter(DelegatingCableHandler):
    """\
    A configurable filter to swallow unwanted events/texts.

    By default, the texts of

        * header
        * TAGs
        * cable content

    are ignored.
    """
    def __init__(self, handler, want_tags=False, want_content=False, want_summary=True, want_comment=True, want_header=False):
        """\

        """
        super(NLPFilter, self).__init__(handler)
        self.want_tags = want_tags
        self.want_content = want_content
        self.want_summary = want_summary
        self.want_commet = want_comment
        self.want_header = want_header

    def handle_header(self, s):
        if self.want_header:
            self._handler.handle_header(s)

    def handle_tag(self, s):
        if self.want_tags:
            self._handler.handle_tag(s)

    def handle_content(self, s):
        if self.want_content:
            self._handler.handle_content(s)

    def handle_summary(self, s):
        if self.want_summary:
            self._handler.handle_summary(s)

    def handle_comment(self, s):
        if self.want_comment:
            self._handler.handle_comment(s)

class NLPCableHandler(NoopCableHandler):
    """\
    `cablemap.core.interfaces.ICableHandler` implementation which collects
    texts and adds 

    The handler uses by default the information from
    * summary
    * comment
    * header
    * content
    * TAGs

    The information can be reduced if the events are filtered in advance, i.e.::

        from cablemap.core.handler import DelegatingCableHandler, handle_source
        from cablemap.core import constants as consts
        from cablemap.core.utils import tag_kind
        from cablemap.nlp.handler import CorpusHandler, NLPFilter

        class MyFilter(NLPFilter):
            '''\
            Filters all TAGs which are not person TAGs
            '''
            def handle_tag(self, tag):
                # Let only person TAGs pass
                if self.want_tags and tag_kind(tag) == consts.TAG_KIND_PERSON:
                    self._handler.handle_tag(tag)


        writer = CorpusHandler('/my/path')
        handler = MyFilter(writer)

        handle_source('cables.csv', handler)

    As result, the corpus will not contain information from the cable headers and all TAGs
    which are not person TAGs won't be part of the corpus, too.

    Without filtering, the writer will add duplicate information to the corpus since it adds
    the comment and the summary section (which are part of the cable's content) to the corpus
    in addition to the cable's content.
    """
    def __init__(self, corpus, before_close=None):
        """\

        `corpus`
            An object which has a `add_texts(reference_id, iterable_of_strings)`` and
            a ``close`` method.
        `before_close`
            An optional function which is called with the underlying corpus before it is
            closed.
        """
        self._corpus = corpus
        self._reference_id = None
        self._buff = []
        self.before_close = before_close

    def end(self):
        if self.before_close:
            self.before_close(self._corpus)
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

    def handle_tag(self, s):
        self._buff.append(s)

class DictionaryHandler(NLPCableHandler):
    """\
    `NLPCableHandler` implementation which works on a `WordCorpus`.

    Note: This handler won't attempt to persist the Dictionary. The caller
    should handle over an existing Dictionary or should save it in the `before_close`
    callback::

        from gensim.corpora.dictionary import Dictionary
        from cablemap.core import handle_source

        dct = Dictionary()
        handler = DictionaryHandler(dct)

        handle_source('cables.csv', handler)

        # Now save the dict:
        dct.save_as_text('/path/wordids.txt')
        
    """
    def __init__(self, dct=None, tokenizer=None, before_close=None):
        """\

        `dct`
            An existing `gensim.corpora.dictionary.Dictionary`
            If it's ``None`` (default) a dictionary will be created.
        `tokenizer`
            A function to tokenize/normalize/clean-up strings.
            If it's ``None`` (default), a default function will be used to tokenize
            texts.
        `before_close`
            An optional function which is called with the underlying corpus before it is
            closed.
        """
        super(DictionaryHandler, self).__init__(WordCorpus(dct, tokenizer), before_close)

class CorpusHandler(NLPCableHandler):
    """\
    Creates a `cablemap.nlp.corpus.CableCorpus` instance.
    """
    def __init__(self, path, dct=None, tokenizer=None, allow_dict_updates=True, prefix=None, before_close=None):
        """\
        Initializes the corpus writer which creates a new `CableCorpus`.

        `path`
            Directory where the generated files are stored.
        `dct`
            An existing `gensim.corpora.dictionary.Dictionary`
            If it's ``None`` (default) a dictionary will be created.
        `tokenizer`
            A function to tokenize/normalize/clean-up strings.
            If it's ``None`` (default), a default function will be used to tokenize
            texts.
        `allow_dict_updates`
            Indicats if unknown words should be added to the dictionary (default ``True``).
        `prefix`
            A prefix for the generated file names.
        `before_close`
            An optional function which is called with the underlying corpus before it is
            closed. May be useful to modify the corpus or the Dictionary before changes are
            written to disk.
        """
        super(CorpusHandler, self).__init__(CableCorpus(path, dct, tokenizer, allow_dict_updates, prefix),
                                           before_close)

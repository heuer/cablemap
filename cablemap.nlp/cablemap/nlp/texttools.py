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

"""
import re
import nltk
from nltk.tokenize import TreebankWordTokenizer, WordPunctTokenizer
from nltk.corpus import stopwords
from nltk import sent_tokenize

stop_words = set(stopwords.words('english'))
tokenizer = WordPunctTokenizer()
tokenize = tokenizer.tokenize


_CLEAN_PATTERN = re.compile(r'''([0-9]+\s*\.?\s*\(?[SBU/NTSC]+\)[ ]*)   # Something like 1. (C)
                                 |(\-{3,})                              # Section delimiter ---
                                 |(\s*[A-Z]+\s+[0-9 \.]+OF\s+[0-9]+)    # Section numbers like ROME 0001 003.2 OF 004
                                 |(^[0-9]+\s*\.\s*)                     # Paragraph numbering without classification
                                 |((END )?\s*SUMMAR?Y(\s+AND\s+COMMENT)?\s*\.?:?[ ]*) # Introduction/end of summary
                                 |((END )?\s*COMMENT\s*\.?:?[ ]*)        # Introduction/end of comment
                            ''', re.VERBOSE|re.MULTILINE|re.IGNORECASE)

def clean_cable_content(content):
    """\
    Removes content like "1. (C)" from the content.
    
    `content`
        The content of the cable.
    """
    res = _CLEAN_PATTERN.sub('', content)
    return res

_UNWANTED_WORDS_PATTERN = re.compile(r'(--+)|(xx+)', re.IGNORECASE|re.UNICODE)

def _accept_word(word):
    """\
    Returns if the `word` is acceptable/useful
    
    `word`
        The word to check.
    """
    return len(word) > 2 \
            and word not in stop_words \
            and not _UNWANTED_WORDS_PATTERN.match(word)

def word_list(content, filter=True, predicate=None):
    """\
    Returns the list of words from the provided text.
    
    `content`
        A text.
    `filter`
        Indicates if stop words and garbage like "xxxxxx" should be removed from
        the word list.
    `predicate`
        An alternative word filter. If it is ``None`` "xxxx", "---",
        default stop words, and words which have no min. length of 3 are filtered
        (iff ``filter`` is set to ``True``).
    
    >>> word_list('Hello and goodbye ------ ')
    ['Hello', 'goodbye']
    >>> word_list('Hello, and goodbye ------ Subject xxxxxxxxx XXXXXXXXXXXX here')
    ['Hello', 'goodbye', 'Subject']
    >>> word_list('Hello, and goodbye.How are you?')
    ['Hello', 'goodbye', 'How']
    """
    words = tokenize(content)
    if filter or predicate:
        if predicate is None:
            predicate = _accept_word
        return [w for w in words if predicate(w)]
    return words

def sentence_list(content):
    """\
    Returns a list of sentences from the provided content.
    
    `content`
        A text.
    
    >>> sentence_list("I've been waiting. I've been waiting night and day.")
    ["I've been waiting.", "I've been waiting night and day."]
    """
    return sent_tokenize(content)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

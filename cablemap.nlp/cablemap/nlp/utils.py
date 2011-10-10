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
Utilities
"""
from gensim.matutils import MmWriter

class IncrementalMmWriter(object):
    """\
    Wraps a `gensim.matutils.MmWriter` to write a corpus incrementally.

    It's purpose is somewhat similar to
    `gensim.matutils.MmWriter.write_corpus(fname, corpus, progress_cnt=1000, index=False)` but
    it doesn't expect that all vectors are available. The vectors are added incrementally via
    `add_vector`.
    """
    def __init__(self, filename):
        mmw = MmWriter(filename)
        # write empty headers to the file (with enough space to be overwritten later)
        mmw.write_headers(-1, -1, -1) # will print 50 spaces followed by newline on the stats line
        self._mmw = mmw
        self._num_docs = -1
        self._num_terms = 0
        self._num_nnz = 0 # number of non-zeroes in the sparse corpus matrix

    def add_vector(self, vector):
        """\
        Writes the provided vector to the matrix.

        `vector`
            An iterable of ``(word-id, word-frequency)`` tuples
        """
        self._num_docs+=1
        max_id, veclen = self._mmw.write_vector(self._num_docs, vector)
        self._num_terms = max(self._num_terms, 1 + max_id)
        self._num_nnz += veclen

    def close(self):
        """\
        Closes the writer.

        This method MUST be called once all vectors are added.
        """
        self._mmw.fake_headers(self._num_docs+1, self._num_terms, self._num_nnz)
        self._mmw.close()

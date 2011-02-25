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
Experimental module which stores cables into Whoosh.
"""
from __future__ import absolute_import
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import SchemaClass, ID, TEXT
from whoosh.qparser import QueryParser


class CableSchema(SchemaClass):
    """\
    Default schema to store cable information.
    
    Note: This class provides only a subset of the cable information, namely
    ``reference_id``, ``subject`` and the cable content.
    """
    reference_id = ID(unique=True, stored=True)
    subject = TEXT
    body = TEXT


def index_cables(directory, cables, clean=False, schema=CableSchema, add_cable=None):
    """\
    Writes the provides `cables` to the Whoosh index.
    
    `directory`
        The directory for the Whoosh index.
    `cables`
        An iterable of cables.
    `clean`
        Indicates if the index should be created from scratch (default: ``False``)
        If set to ``True`` any existing index within the `directory` will be 
        removed.
    `schema`
        The Whoosh schema (default: `CableSchema`)
    `add_cable`
        Function which will be invoked for each cable in `cables`
        The function must accept a Whoosh writer instance and a cable object.
        If `add_cable` is ``None`` (default), a default function will be used
        which assumes a schema similar to `CableSchema`.
    """
    def _add_cable(writer, cable):
        writer.add_document(reference_id=unicode(cable.reference_id),
                            subject=unicode(cable.subject),
                            body=unicode(getattr(cable, 'content_body', cable.content))
                            )
    if clean or not os.path.exists(directory):
        ix = create_in(directory, schema=schema)
    else:
        ix = open_dir(directory)
    writer = ix.writer()
    add_cable = add_cable or _add_cable
    for cable in cables:
        add_cable(writer, cable)
    writer.commit()

def index_cable(directory, cable, schema=CableSchema, add_cable=None):
    """\
    Adds a single cable to the index.

    `directory`
        The directory for the Whoosh index.
    `cable`
        A cable.
    `schema`
        The Whoosh schema (default: `CableSchema`)
    `add_cable`
        The function must accept a Whoosh writer instance and a cable object.
        If `add_cable` is ``None`` (default), a default function will be used
        which assumes a schema similar to `CableSchema`.
    """
    index_cables(directory, (cable,), clean=False, schema=schema, add_cable=add_cable)
  

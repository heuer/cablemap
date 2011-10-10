# -*- coding: utf-8 -*-
"""\
Playground to generarte the cable corpus
"""
import os
from cablemap.core import handle_source, predicates as pred
from cablemap.core.handler import DefaultMetadataOnlyFilter, TeeCableHandler
from cablemap.nlp.handler import CorpusWriter

def generate_corpus(src):
    handler = TeeCableHandler(DefaultMetadataOnlyFilter(CorpusWriter('./', prefix='german_cables_metadata_')),
                              CorpusWriter('./', prefix='german_cables_'))
    handle_source(src, handler, pred.origin_filter(pred.origin_germany))

if __name__ == '__main__':
    generate_corpus('cables.csv')

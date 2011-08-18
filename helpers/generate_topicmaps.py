# -*- coding: utf-8 -*-
"""\
Experimental script to generarte topic maps.
"""
import os
import re
import codecs
from cablemap.core.utils import titlefy
from cablemap.core.handler import MultipleCableHandler, DelegatingCableHandler, handle_directory
from cablemap.tm.handler import create_ctm_handler, create_xtm_handler

import logging 
import sys
logger = logging.getLogger('cablemap.core.reader')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


class DefaultCableHandler(DelegatingCableHandler):
    """\
    
    """
    def handle_wikileaks_iri(self, iri):
        if iri.startswith('http://wikileaks.org') and iri.endswith('html'):
            self._handler.handle_wikileaks_iri(iri)

    def handle_subject(self, subject):
        self._handler.handle_subject(titlefy(subject))

    def handle_body(self, body):
        pass

    def handle_header(self, header):
        pass


class SubjectLocatorsCableHandler(DelegatingCableHandler):
    """\
    
    """
    def __getattr__(self, name):
        def noop(*args):
            pass
        if 'start' not in name and 'end' not in name and 'wikileaks' not in name:
            return noop
        return getattr(self._handler, name)

class ContentCableHandler(DelegatingCableHandler):
    """\
    
    """
    def __getattr__(self, name):
        def noop(*args):
            pass
        if 'start' not in name and 'end' not in name and 'body' not in name and 'header' not in name:
            return noop
        return getattr(self._handler, name)


def openfile(name):
    return open(os.path.join(os.path.dirname(__file__), name), 'wb')

def generate_topicmaps(cable_directory):
    ctm_tm = openfile('cables.ctm')
    xtm_tm = openfile('cables.xtm')
    slos_ctm = openfile('cable-subject-locators.ctm')
    slos_xtm = openfile('cable-subject-locators.xtm')
    content_ctm = openfile('cable-content.ctm')
    content_xtm = openfile('cable-content.xtm')
    files = [ctm_tm, xtm_tm, slos_ctm, slos_xtm, content_ctm, content_xtm]
    handlers = []
    handlers.append(DefaultCableHandler(create_ctm_handler(ctm_tm)))
    handlers.append(DefaultCableHandler(create_xtm_handler(xtm_tm)))
    handlers.append(SubjectLocatorsCableHandler(create_ctm_handler(slos_ctm)))
    handlers.append(SubjectLocatorsCableHandler(create_xtm_handler(slos_xtm)))
    handlers.append(ContentCableHandler(create_ctm_handler(content_ctm)))
    handlers.append(ContentCableHandler(create_xtm_handler(content_xtm)))
    handle_directory(cable_directory, MultipleCableHandler(handlers))
    for f in files:
        f.close()
    
    
if __name__ == '__main__':
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    generate_topicmaps('./cable/')

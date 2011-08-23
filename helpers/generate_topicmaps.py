# -*- coding: utf-8 -*-
"""\
Experimental script to generarte topic maps.
"""
import os
import codecs
from tm.mio import handler
from mio.ctm.miohandler import CTMHandler
from mio.xtm.miohandler import XTM21Handler
from cablemap.core.handler import DefaultMetadataOnlyFilter, DebitlyFilter, TeeCableHandler, MultipleCableHandler, DelegatingCableHandler, handle_directory
from cablemap.tm.handler import create_ctm_handler, create_xtm_handler, create_ctm_miohandler, create_xtm_miohandler, MediaTitleResolver

import logging 
import sys
logger = logging.getLogger('cablemap.core.reader')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

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


def mediatitle_resolver_ctm(fileobj):
    return MediaTitleResolver(CTMHandler(fileobj))

def mediatitle_resolver_xtm(fileobj):
    return MediaTitleResolver(XTM21Handler(fileobj=fileobj))

def openfile(name):
    return open(os.path.join(os.path.dirname(__file__), name), 'wb')

def generate_topicmaps(cable_directory, handle_media=False):
    def tee(files, filename):
        ctm = openfile(filename + '.ctm')
        xtm = openfile(filename + '.xtm')
        files.append(ctm)
        files.append(xtm)
        return TeeCableHandler(create_ctm_handler(ctm), create_xtm_handler(xtm))
    files = []
    handlers = []
    handlers.append(DefaultMetadataOnlyFilter(DebitlyFilter(tee(files, 'cables'))))
    handlers.append(SubjectLocatorsCableHandler(tee(files, 'cable-subject-locators')))
    handlers.append(ContentCableHandler(tee(files, 'cable-content')))
    if handle_media:
        ctm, xtm = openfile('media-iris.ctm'), openfile('media-iris.xtm')
        files.append(ctm)
        files.append(xtm)
        h = DebitlyFilter(MediaTitleResolver(handler.TeeMapHandler(create_ctm_miohandler(ctm), create_xtm_miohandler(xtm))))
        handlers.append(h)
    handle_directory(cable_directory, MultipleCableHandler(handlers))
    for f in files:
        f.close()


   
if __name__ == '__main__':
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    generate_topicmaps('./cable/')

# -*- coding: utf-8 -*-
"""\
Experimental script to generarte topic maps.
"""
import os
import codecs
from tm.mio import handler
from mio.ctm.miohandler import CTMHandler
from mio.xtm.miohandler import XTM21Handler
from cablemap.core import handle_source, predicates as pred
from cablemap.core.handler import DefaultMetadataOnlyFilter, DebitlyFilter, TeeCableHandler, \
     MultipleCableHandler, DelegatingCableHandler, CableIdFilter
from cablemap.tm import psis
from cablemap.tm.handler import create_ctm_handler, create_xtm_handler, \
     create_ctm_miohandler, create_xtm_miohandler, MediaTitleResolver, BaseMIOCableHandler

import logging 
import sys
logger = logging.getLogger('cablemap.core.reader')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

_CGS_BASE = u'http://www.cablegatesearch.net/cable.php?id='

class SubjectLocatorsCableHandler(BaseMIOCableHandler):
    """\
    
    """
    def start_cable(self, rid, c14n_id):
        super(SubjectLocatorsCableHandler, self).start_cable(rid, c14n_id)
        self._start_cable()

    def end_cable(self):
        self.handle_wikileaks_iri(_CGS_BASE + self._cable_reference_id)
        super(SubjectLocatorsCableHandler, self).end_cable()
        self._end_cable()

    def handle_wikileaks_iri(self, iri):
        self._handler.subjectLocator(iri)

class ContentCableHandler(DelegatingCableHandler):
    """\
    
    """
    def __getattr__(self, name):
        def noop(*args):
            pass
        if 'start' not in name and 'end' not in name and 'content' not in name and 'header' not in name:
            return noop
        return getattr(self._handler, name)

def slo_handler(files, filename='cable-subject-locators'):
    ctm, xtm = openfile(filename + '.ctm'), openfile(filename + '.xtm')
    files.append(ctm)
    files.append(xtm)
    ctm_miohandler = create_ctm_miohandler(ctm, register_prefixes=False, register_templates=False)
    ctm_miohandler.add_prefix(u'cb', str(psis.NS_CABLE))
    ctm_miohandler.add_prefix(u'cgs', _CGS_BASE)
    mio_handler = handler.TeeMapHandler(ctm_miohandler, create_xtm_miohandler(xtm))
    return SubjectLocatorsCableHandler(mio_handler)

def openfile(name):
    return open(os.path.join(os.path.dirname(__file__), name), 'wb')

def generate_topicmaps(src, handle_media=False):
    def tee(files, filename):
        ctm = openfile(filename + '.ctm')
        xtm = openfile(filename + '.xtm')
        files.append(ctm)
        files.append(xtm)
        return TeeCableHandler(create_ctm_handler(ctm), create_xtm_handler(xtm))
    files = []
    handlers = []
    european_handler = CableIdFilter(tee(files, 'european-cables'), pred.origin_filter(pred.origin_europe))
    all_cables_handler = tee(files, 'cables')
    handlers.append(DefaultMetadataOnlyFilter(DebitlyFilter(TeeCableHandler(european_handler, all_cables_handler))))
    handlers.append(slo_handler(files))
    handlers.append(ContentCableHandler(tee(files, 'cable-content')))
    if handle_media:
        ctm, xtm = openfile('media-iris.ctm'), openfile('media-iris.xtm')
        files.append(ctm)
        files.append(xtm)
        h = DebitlyFilter(MediaTitleResolver(handler.TeeMapHandler(create_ctm_miohandler(ctm), create_xtm_miohandler(xtm))))
        handlers.append(h)
    handle_source(src, MultipleCableHandler(handlers))
    for f in files:
        f.close()

   
if __name__ == '__main__':
    generate_topicmaps('cables.csv')

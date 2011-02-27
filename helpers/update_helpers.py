# -*- coding: utf-8 -*-
"""\
This module tries to detect acronyms, finds cables w/o subject.
"""
import os
import re
import codecs
from functools import partial
from cablemap.core import cables_from_directory

import logging 
import sys
logger = logging.getLogger('cablemap-reader')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

_AC_PATTERN = re.compile(r'\(([A-Z\-/\.]{2,}[0-9]*)\)')

_ACRONYMS = (u'AA/S', u'ADC', u'AFM', u'AG', u'ASD/ISA', u'AU', u'AK', u'APHSCT',
             u'AF-PAK', u'AKP', u'ASD', u'AQAP', u'AQIM', u'ARENA',
             u'BBC', u'BP', u'BR-3',
             u'CMC', u'CNP', u'CODEL', u'CJCS', u'CT', u'CWS/BWC', u'CW', u'CENTCOM',
             u'CDR', u'CFE', u'CISMOA', u'CN', u'CIA', u'CTJWG', u'CG', u'CL',
             u'DAS', u'DCA', u'DDR', u'DEA', u'DG', u'DCM', u'DFID',
             u'DRC', u'DASD', u'DIO', u'DHS', u'DOL', u'DPRK',
             u'EFCC', u'ETA', u'EU', u'EU/US', u'EXBS', u'EUR', u'EFTA',
             u'FATF', u'FBI', u'FCO', u'FDA', u'FDP', u'FM', u'FTAA', u'FARC', u'FX2', u'FMLN',
             u'GAERC', u'GDRC', u'GM', u'GOAJ', u'GOB', u'GOC', u'GOE', u'GOI', u'GOK', u'GOL',
             u'GPC', u'GSL', u'GSP', u'GTMO', u'GOF', u'GOS', u'GBRV', u'GOP', u'GOU', u'GFA',
             u'G/TIP',
             u'HMG', u'HLDG', u'HLG', u'HEU',
             u'ICTY', u'II', u'III', u'IMF', u'ITGA', u'IPR', u'IRGC', u'ICAO', u'IRA', u'ISAF',
             u'(INCSR)', u'ICRC', u'ISA', u'INR/B', u'ICC', u'ICG-G', u'ICJ', u'ILSA',
             u'JSF', u'JHA', u'JCET', u'JPMG',
             u'MDC', u'MEP', u'MFA', u'MOD', u'MI-17', u'MI-6',
             u'MRE', u'MP', u'MONUC', u'MOP-3', u'MEA',
             u'NATO', u'NDP', u'NSA', u'NGO', u'NEA', u'NEA/MAG', u'NTM-I',
             u'OIC', u'OECD', u'OAS',
             u'PA', u'PD', u'PM', u'PMDB', u'PS', u'PDAS', u'PRT', u'POC', u'PRC/DPRK',
             u'PNG', u'PRC',
             u'ROK', u'RWE', u'RFG', u'RMB', u'RSO', u'RPO', u'RTG',
             u'SLA', u'SLA/U', u'SPD', u'SWIFT', u'S/WCI', u'S/CT', u'S/CRS',
             u'S/GC', u'SCSL', u'S/SRAP', u'SG',
             u'TFTP', u'TFTP/SWIFT', u'U.S.-EU', u'U.S.-UK', u'UAE', u'UK', u'UN',
             u'UNHCR', u'UNSC', u'US', u'US-CU', u'US-EU', u'USG', u'USTR', u'UNCHR',
             u'USEB', u'UNGA', u'U.S./UK', u'UNESCO', u'U/SYG', u'US-ROYG', u'UNSCR',
             u'USG-GOB', u'USD/P', u'USS', u'UNDP',
             u'VFM', u'VP', u'VI', u'VARIG', u'VOA',
             u'WEF', u'WTO',
             u'XVI',
             u'ZANU-PF')

_UNWANTED = (u'SAVE',)

def run_update(in_dir, predicate=None):
    seen_cables = set()
    acronyms = set(_ACRONYMS)
    subjects = set()
    tids = set()
    for cable in cables_from_directory(in_dir, predicate):
        update_acronyms(cable, acronyms)
        update_missing_subjects(cable, subjects)
        # Ignore missing transmission ids, the parser seems to detect them correctly
        # update_missing_transmission_ids(cable, tids)
        seen_cables.add(cable.reference_id)
    return {'acronyms': acronyms, 'subjects': subjects, 'tids': tids, 'seen_cables': seen_cables}

def update_acronyms(cable, acronyms):
    if not cable.subject or not cable.content_body:
        return
    subject_words = [w for w in cable.subject.upper().split() if not w.startswith('XXXXX')]
    acronyms.update((ac for ac in _AC_PATTERN.findall(cable.content_body) if ac in subject_words and ac not in _UNWANTED))

def update_missing_subjects(cable, cable_refs):
    if not cable.subject:
        cable_refs.add(cable.reference_id)

def update_missing_transmission_ids(cable, cable_refs):
    if not cable.partial and not cable.transmission_id:
        cable_refs.add(cable.reference_id)
 
def _filename(name):
    return os.path.join(os.path.dirname(__file__), name)

def _file_in_core(name):
    return os.path.join(os.path.dirname(__file__), '..', 'cablemap.core', 'cablemap/core/', name)

def _file_as_set(filename):
    if not os.path.exists(filename):
        return set()
    f = codecs.open(filename, 'rb', 'utf-8')
    s = set((l.rstrip() for l in f))
    f.close()
    return s

def _write_set(filename, s):
    f = codecs.open(filename, 'wb', 'utf-8')
    for item in sorted(s):
        f.write(item)
        f.write('\n')
    f.close()

def update_file(filename, found):
    if not found:
        return
    current = _file_as_set(filename)
    diff = current ^ (found | current)
    if diff:
        _write_set(filename, (found | current))
        print('New in "%s": %r' % (filename, diff))


_FILE_SEEN_CABLES = _filename('seen_cables.txt')
_FILE_ACRONYMS = _file_in_core('acronyms.txt')
_FILE_SUBJECTS = _filename('no_subject.txt')
_FILE_TIDS = _filename('no_transmissionid.txt')
    
if __name__ == '__main__':
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    def filter_known_cables(f, knowncables):
        name = f[:f.rfind('.')]
        return name not in knowncables
    if not os.path.exists(_FILE_SEEN_CABLES):
        f = open(_FILE_SEEN_CABLES, 'wb')
        f.close()
    seen_cables = _file_as_set(_FILE_SEEN_CABLES)
    want_file = partial(filter_known_cables, knowncables=seen_cables)
    res = run_update('./cable/', want_file)
    update_file(_FILE_ACRONYMS, res['acronyms'])
    update_file(_FILE_SUBJECTS, res['subjects'])
    update_file(_FILE_TIDS, res['tids'])
    # Should be the last step in case of errors in one of the above steps
    if seen_cables ^ (seen_cables | res['seen_cables']):
        seen_cables.update(res['seen_cables'])
        _write_set(_FILE_SEEN_CABLES, seen_cables)    

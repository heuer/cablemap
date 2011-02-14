# -*- coding: utf-8 -*-
"""\
This module tries to detect acronyms in the cable texts.
"""
import re
from cablemap.core import cables_from_directory

_AC_PATTERN = re.compile(r'\(([A-Z\-/\.]{2,}[0-9]*)\)')

_ACRONYMS = (u'AA/S', u'ADC', u'AFM', u'AG', u'ASD/ISA', u'AU', u'AK', u'APHSCT',
             u'AF-PAK', u'AKP', u'ASD', u'AQAP', u'AQIM', u'ARENA',
             u'BBC', u'BP', u'BR-3',
             u'CMC', u'CNP', u'CODEL', u'CJCS', u'CT', u'CWS/BWC', u'CW', u'CENTCOM',
             u'CDR', u'CFE', u'CISMOA', u'CN', u'CIA', u'CTJWG', u'CG',
             u'DAS', u'DCA', u'DDR', u'DEA', u'DG', u'DCM', u'DFID',
             u'DRC', u'DASD', u'DIO', u'DHS', u'DOL', u'DPRK',
             u'EFCC', u'ETA', u'EU', u'EU/US', u'EXBS', u'EUR', u'EFTA',
             u'FATF', u'FBI', u'FCO', u'FDP', u'FM', u'FTAA', u'FARC', u'FX2', u'FMLN',
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
             u'PD', u'PM', u'PMDB', u'PS', u'PDAS', u'PRT', u'POC', u'PRC/DPRK', u'PNG',
             u'PRC',
             u'ROK', u'RWE', u'RFG', u'RMB', u'RSO', u'RPO',
             u'SLA', u'SLA/U', u'SPD', u'SWIFT', u'S/WCI', u'S/CT', u'S/CRS',
             u'S/GC', u'SCSL', u'S/SRAP', u'SG',
             u'TFTP', u'TFTP/SWIFT', u'U.S.-EU', u'U.S.-UK', u'UAE', u'UK', u'UN',
             u'UNHCR', u'UNSC', u'US', u'US-CU', u'US-EU', u'USG', u'USTR', u'UNCHR',
             u'USEB', u'UNGA', u'U.S./UK', u'UNESCO', u'U/SYG', u'US-ROYG', u'UNSCR',
             u'VFM', u'VP', u'VI', u'VARIG', u'VOA',
             u'WEF', u'WTO',
             u'XVI',
             u'ZANU-PF')

_UNWANTED = (u'SAVE',)

def find_acronyms(in_dir):
    s = set(_ACRONYMS)
    for cable in cables_from_directory(in_dir):
        if not cable.subject or not cable.content_body:
            continue
        subject_words = cable.subject.upper().split()
        s.update((ac for ac in _AC_PATTERN.findall(cable.content_body) if ac in subject_words and ac not in _UNWANTED))
    return s
    
if __name__ == '__main__':
    import os, codecs
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    filename = os.path.join(os.path.dirname(__file__), 'acronyms.txt')
    f = codecs.open(filename, 'rb', 'utf-8')
    current_acronyms = set((l.rstrip() for l in f))
    f.close()
    acronyms = find_acronyms('./cable/')
    diff = acronyms ^ current_acronyms
    if diff:
        print 'difference: ', diff
        f = codecs.open(filename, 'wb', 'utf-8')
        for acronym in sorted(acronyms):
            f.write(acronym)
            f.write('\n')


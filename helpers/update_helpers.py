# -*- coding: utf-8 -*-
"""\
This module tries to detect acronyms and cables w/o subject.
"""
import os
import re
import codecs
from functools import partial
from collections import defaultdict
from cablemap.core import cables_from_source

import logging 
import sys
logger = logging.getLogger('cablemap.core.reader')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

_AC_PATTERN = re.compile(r'\(([A-Z\-/\.]{2,}[0-9]*)\)')

_KNOWN_TAGS = ('BIDEN, JOSEPH', "RICE, CONDOLEEZZA", "CLINTON, HILLARY", "CARSON, JOHNNIE", u'BUSH, GEORGE W.',
               "NEW ZEALAND", "ROOD, JOHN", "ECONOMY AND FINANCE", "ECONOMIC AFFAIRS", "HUMAN RIGHTS",
               "ITALY NATIONAL ELECTIONS", "ZOELLICK, ROBERT", "ZANU-PF", "GAZA DISENGAGEMENT",
               "COUNTERTERRORISM", "IRAQI FREEDOM", "MEETINGS WITH AMBASSADOR", "EXTERNAL", "CONSULAR AFFAIRS",
               "JIMENEZ, GASPAR", "ITALIAN POLITICS", "ISRAELI PALESTINIAN AFFAIRS", "DOMESTIC POLITICS",
               "CROS, GERARD", "GLOBAL DEFENSE", "ISRAEL RELATIONS", "MILITARY RELATIONS", "POLITICS FOREIGN POLICY",
               "USEU BRUSSELS", "INDIA-BURMA", "STEINBERG, JAMES B.", "NOVO, GUILLERMO", "REMON, PEDRO",
               "COUNTRY CLEARANCE", "CARICOM", "INMARSAT", "UNESCO", "INTERPOL", "INTELSAT", u'CYPRUS',
               u'MEDIA REACTION', u'UNICEF', u'SPECIALIST', u'POLITICAL PARTIES', u'OFFICIALS', u'UNFICYP',
               u'ECOSOC', u'MERCOSUR', u'AFGHANISTAN', u'MACEDONIA', u'MQADHAFI', u'GOI EXTERNAL', u'GOI INTERNAL',
               u'INTERNAL', u'EXTERNAL', u'ISLAMISTS', u'UNCTAD', u'MINUSTAH', u'UNIDROIT', u'CAMBODIA',
               u'COPUOS', u'UNPUOS', u'ATPDEA', u'AMCHAMS', u'POLITICAL', u'POLINT', u'REGION',
               u'FOREIGN POL', u'MEDIA REACTION REPORT', u'TIP IN TURKEY', u'TURKEY', u'HEBRON', u'KUWAIT-IRAQ RELATIONS',
               u'TERRORISM', u'AGRICULTURE', u'ELECTIONS', u'PHALANAGE PARTY', u'ANACHISTS', u'ECONOMIC', u'ECONOMICS',
               u'ANARCHISTS', u'JOSEPH, ROBERT G.', u'MURRAY, PATTY', 'LOTT, TRENT', u'NELSON, BEN', u'HADLEY, STEPHEN',
               u'THOMMA, THOMAS', u'QADRI, MOHAMMAD AFZAL', u'SECRETARY OF COMMERCE', u'BURNS, WILLIAM',
               u'ISRAELI SOCIETY', u'ENVIRONMENT SCIENCE AND TECHNOLOGY', u'SETTLEMENTS', u'KUWAIT IRAN RELATIONS',
               u'DEMOCRATIC REFORM', u'RELFREE', u'HUMAN RIGHTS VETTING',  u'SIMS, NICOLE MARIE', u'MAHURIN, PATRICK WARREN',
               u'HIV AND AIDS', u'U.S.-ISRAEL RELATIONS', u'U.S.-ZIMBABWE BILATERAL RELATIONS', u'CHENEY, RICHARD',
               u'WELCH, DAVID', u'BOEHNER, JOHN', u'OBAMA, BARACK', u'PELOSI, NANCY', u'RICE, SUSAN', u'SALOPEK, PAUL',
               u'SIPRNET', u'WEBSITE', u'BORDER PATROL', u'MCLELLAN, ANNE', u'ZACCARDELLI, GIULIANO', u'BUSH, LAURA',
               u'UNHCR', u'UNHRC-1', u'UNHCR-2', u'FRANCO-GERMAN RELATIONS', u'FRAZER, JENDAYI', u'FRIED, DANIEL',
               u'MILLENNIUM CHALLENGE ACCOUNT', u'ACCELERATED DEPORTATION', u'WARD, WILLIAM E.', u'WELFARE AND WHEREABOUTS',
               u'REINEMEYER/WILCOX EMAIL--09/17/07', u'HIGH LEVEL MEETINGS', u'HOMELAND SECURITY', u'HOSTAGE',
               u'MILITARY COOPERATION', u'ZIMBABWE SOUTH AFRICAN RELATIONS', u'MARCH 05 ELECTIONS', u'ACTION',
               u'REPATRIATION', u'ADOPTION', u'BILATERAL', u'MARTIN, PAUL', u'PETTIGREW, PIERRE',
               u'CLARKSON, ADRIENNE', u'AGUIRRE LETE, JUAN LUIS', u'ALVAREZ, ROBERT WILLIAM',
               u"BA'ATH", u'MISSILE DEFENSE', u'CANADIAN MILITARY', u'MARTIN, BARBARA', u'FREEDOM OF PRESS',
               u'BORDER SECURITY', u'BORDER CONTROL', u'CHABAROU, MOURAD', u'CHAMAN, JONATHAN',
               u'CHAO, ELAINE', u'CLINTON, BILL', u'CONAWAY, MICHAEL', u'COUNTRY VISITS', u'TRAFFICKING', u'SMUGGLING',
               u'HARPER, STEPHEN', u'BIOTECHNOLOGY', u'BLUNT, ROY', u'BOUCHAR, ABDELMAJID', u'BOUHABILA, NOUREDDINE',
               u'BOULOUDO, KHALID', u'BOUSBAA, NASREDDINE', u'CHERTOFF, MICHAEL', u'CHELIDZE, ALEXANDER',
               u'LEVINE, JEFFREY D.', u'LTTE - PEACE PROCESS', u'2004 ELECTIONS', u'2005 ELECTION', u'2006 ELECTIONS',
               u'2006 PARALYMPIC GAMES', u'HUMANITARIAN AID', u'AFRICA', u'AIRSPACE FEES', u'HIMELFARB, ALEX',
               u'ALGERIA-EUROPE RELATIONS', 'ALGERIA-MOROCCO RELATIONS', u'ALGERIAN VIEWS ON IRAN',
               u'ABKHAZIA', u'ALLAG, LARBI BEN AHMED', u'CANAHUATI YACAMAN, MIGUEL FELIPE', u'CAMEL JOCKEYS',
               u'CANADA-US EXCHANGE', u'CANADIAN UKRAINIAN COMMUNITY', u'AGRICULTURE/FOOD SECURITY',
               u'AIR INDIA', u'AIR QUALITY', u'CHURCH', u"AMBASSADOR'S CALLS", u'ANTI CORRUPTION BUREAU',
               u'ANTI-CORRUPTION', u'ARAB LEAGUE', u'AFRICAN UNION', u'ANTITERRORISM/FORCE PROTECTION',
               u'ANTISEMITIC', u'MUSEUM', u'MUSLIM COMMUNITY', u'MUSLIM EXTREMISM', u'MUSLIM ISSUES',
               u'MUSLIMS', u'NATIONAL ASSEMBLY', u'ALIREZA, ABDULLAH ZAINAL', u'AMBOSELI',
               )

_ACRONYMS = (u'AA/S', u'ADC', u'AFM', u'AG', u'ASD/ISA', u'AU', u'AK', u'APHSCT',
             u'AF-PAK', u'AKP', u'ASD', u'AQAP', u'AQIM', u'ARENA',
             u'BBC', u'BP', u'BR-3',
             u'CMC', u'CNP', u'CODEL', u'CJCS', u'CT', u'CWS/BWC', u'CW', u'CENTCOM',
             u'CDR', u'CFE', u'CISMOA', u'CN', u'CIA', u'CTJWG', u'CG', u'CL', u'CBD',
             u'DAS', u'DCA', u'DDR', u'DEA', u'DG', u'DCM', u'DFID',
             u'DRC', u'DASD', u'DIO', u'DHS', u'DOL', u'DPRK',
             u'EFCC', u'ETA', u'EU', u'EU/US', u'EXBS', u'EUR', u'EFTA',
             u'FATF', u'FBI', u'FCO', u'FDA', u'FDP', u'FM', u'FTAA', u'FARC', u'FX2', u'FMLN',
             u'GAERC', u'GCC', u'GDRC', u'GM', u'GOAJ', u'GOB', u'GOC', u'GOE', u'GOI', u'GOK',
             u'GOL', u'GPC', u'GSL', u'GSP', u'GTMO', u'GOF', u'GOS', u'GBRV', u'GOP', u'GOU',
             u'GFA', u'G/TIP', u'GI',
             u'HMG', u'HLDG', u'HLG', u'HEU',
             u'ICTY', u'II', u'III', u'IMF', u'ITGA', u'IPR', u'IRGC', u'ICAO', u'IRA', u'ISAF',
             u'(INCSR)', u'ICRC', u'ISA', u'INR/B', u'ICC', u'ICG-G', u'ICJ', u'ILSA',
             u'JSF', u'JHA', u'JCET', u'JPMG',
             u'MDC', u'MEP', u'MFA', u'MOD', u'MI-17', u'MI-6',
             u'MRE', u'MP', u'MONUC', u'MOP-3', u'MEA',
             u'NATO', u'NDP', u'NSA', u'NGO', u'NEA', u'NEA/MAG', u'NTM-I',
             u'OIC', u'OECD', u'OAS', u'OSCE', u'OPEC',
             u'PA', u'PD', u'PM', u'PMDB', u'PS', u'PDAS', u'PRT', u'POC', u'PRC/DPRK',
             u'PNG', u'PRC',
             u'ROK', u'RWE', u'RFG', u'RMB', u'RSO', u'RPO', u'RTG',
             u'SLA', u'SLA/U', u'SPD', u'SWIFT', u'S/WCI', u'S/CT', u'S/CRS',
             u'S/GC', u'SCSL', u'S/SRAP', u'SG', u'SAS',
             u'TFTP', u'TFTP/SWIFT', u'U.S.-EU', u'U.S.-UK', u'UAE', u'UK', u'UN',
             u'UNHCR', u'UNSC', u'US', u'US-CU', u'US-EU', u'USG', u'USTR', u'UNCHR',
             u'USEB', u'UNGA', u'U.S./UK', u'UNESCO', u'U/SYG', u'US-ROYG', u'UNSCR',
             u'USG-GOB', u'USD/P', u'USS', u'UNDP',
             u'VFM', u'VP', u'VI', u'VARIG', u'VOA',
             u'WEF', u'WTO',
             u'XVI',
             u'ZANU-PF')

_UNWANTED = (u'AND', u'ITS', u'SAVE', u'CITES', u'SHARIA', u'IRAN', u'WHO',
             u'CAN', u'SAO', u'IT', u'POSITION', u'AMBASSADOR', u'ENLARGEMENT',
             u'CHINA', u'ACT', u'GOT', u'LIBERTAD', u'POLITICAL', u'POPULATION',
             u'ECONOMIC', u'MEXICO', u'AN', u'IS', u'OFFICE', u'WEST', u'YES',
             u'NELSON-LOTT', u'NEGROPONTE', u'PRESIDENT', u'SECRETARY',)

def run_update(in_dir, predicate=None):
    acronyms = set(_ACRONYMS)
    subjects = set()
    tags = defaultdict(list)
    for cable in cables_from_source(in_dir, predicate):
        update_acronyms(cable, acronyms)
        update_missing_subjects(cable, subjects)
        update_tags(cable, tags)
    return {'acronyms': acronyms, 'subjects': subjects, 'tags': tags}

def update_acronyms(cable, acronyms):
    if not cable.subject:
        return
    subject_words = [w for w in cable.subject.upper().split() if not w.startswith('XXXXX') and len(w) >= 2 and w not in acronyms and w not in _UNWANTED]
    if subject_words:
        acronyms.update((ac for ac in _AC_PATTERN.findall(cable.content) if ac in subject_words))

def update_missing_subjects(cable, cable_refs):
    if cable.content and not cable.subject:
        cable_refs.add(cable.reference_id)

def update_tags(cable, tags):
    for tag in cable.tags:
        if len(tag) > 5 and tag not in _KNOWN_TAGS:
            tags[tag].append(cable.reference_id)
 
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
    diff = current ^ found
    if diff:
        _write_set(filename, found)
        removed = current - found
        fn = os.path.basename(filename)
        header = 'Changes in %s' % fn
        print('\n' + header)
        print('=' * len(header))
        if removed:
            print('Removed:\n%r\n' % (removed))
        added = found - current
        if added:
            print('Added:\n%r\n' % (added))


_FILE_ACRONYMS = _file_in_core('acronyms.txt')
_FILE_SUBJECTS = _filename('no_subject.txt')
_FILE_TAGS = _filename('tags.txt')
    
if __name__ == '__main__':
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    res = run_update('./cable/')
    update_file(_FILE_ACRONYMS, res['acronyms'])
    update_file(_FILE_SUBJECTS, res['subjects'])
    update_file(_FILE_TAGS, set(res['tags'].keys()))
    print('Valid TAGs?')
    tags = res['tags']
    for k in sorted(tags.keys()):
       print(u'%s:\n    %s' % (k, u', '.join(tags[k])))

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
    import os
    if not os.path.isdir('./cable/'):
        raise Exception('Expected a directory "cable"')
    current_acronyms = set([u'(INCSR)', u'AA/S', u'ABD', u'ADC', u'AEC', u'AESA', u'AF-PAK', u'AFM', u'AG', u'AK', u'AKP', u'AL', u'ALBA', u'AMA', u'AML/CFT', u'ANA', u'APHSCT', u'AQAP', u'AQIM', u'ARENA', u'ARS', u'ASD', u'ASD/ISA', u'AT', u'AU', u'BBC', u'BP', u'BR-163', u'BR-3', u'CAR', u'CCID', u'CDA', u'CDR', u'CEN-SAD', u'CENTCOM', u'CFE', u'CG', u'CIA', u'CISMOA', u'CITES', u'CIWG', u'CJCS', u'CMC', u'CN', u'CNP', u'COAS', u'CODEL', u'COGAT', u'COP-15', u'CPC', u'CSI', u'CSIS', u'CSU', u'CT', u'CTJWG', u'CW', u'CWS/BWC', u'DAS', u'DASD', u'DCA', u'DCM', u'DCOS', u'DDR', u'DEA', u'DFID', u'DG', u'DHS', u'DIO', u'DOL', u'DPRK', u'DRC', u'E-PINE', u'EAC', u'EC', u'EDF', u'EFCC', u'EFTA', u'EGIS', u'EITI', u'ELN', u'ENR', u'ETA', u'ETIA', u'EU', u'EU/US', u'EUR', u'EXBS', u'F-X', u'FARC', u'FATF', u'FBI', u'FCO', u'FCPA', u'FDLR', u'FDP', u'FM', u'FMLN', u'FTAA', u'FX2', u'G/TIP', u'GAERC', u'GBRV', u'GC', u'GDRC', u'GFA', u'GHQ', u'GICNT', u'GM', u'GOAJ', u'GOB', u'GOC', u'GOE', u'GOF', u'GOI', u'GOK', u'GOL', u'GOP', u'GOS', u'GOU', u'GPC', u'GSI', u'GSL', u'GSP', u'GTMO', u'HEU', u'HEU-LEU', u'HLDG', u'HLG', u'HMG', u'IAEA', u'IAF', u'ICAO', u'ICC', u'ICG-G', u'ICJ', u'ICRC', u'ICTY', u'IDF', u'II', u'III', u'ILSA', u'IMF', u'IMO', u'INR/B', u'IPCC', u'IPR', u'IRA', u'IRENA', u'IRGC', u'IRGC-QF', u'IRI', u'IRISL', u'ISA', u'ISAF', u'ISN/CTR', u'ITGA', u'JCET', u'JEM', u'JHA', u'JPMG', u'JSF', u'JUD', u'LAAD', u'LIFG', u'M/V', u'MANPADS', u'MB', u'MDC', u'MEA', u'MEK', u'MEP', u'MFA', u'MI-17', u'MI-6', u'MINUSTAH', u'MOA', u'MOD', u'MOIS', u'MONUC', u'MOP-3', u'MP', u'MRE', u'MST', u'MTCR', u'NAM', u'NATO', u'NCP', u'NDP', u'NEA', u'NEA/MAG', u'NEC', u'NFIU', u'NGO', u'NIE', u'NNSA', u'NPT', u'NSA', u'NSC', u'NSG', u'NTM-I', u'OAS', u'OECD', u'OEF', u'OIC', u'ONA', u'ONDCP', u'OPCON', u'OSCE', u'PAD', u'PAG', u'PASF', u'PCC', u'PD', u'PDAS', u'PGA', u'PJD', u'PM', u'PMDB', u'PNG', u'POC', u'PPP', u'PRC', u'PRC/DPRK', u'PRT', u'PS', u'PSDB', u'QATAR', u'QDR', u'QIZ', u'QME', u'RAK', u'RFG', u'RMB', u'ROK', u'RPO', u'RSO', u'RWE', u'S/CRS', u'S/CT', u'S/GC', u'S/SRAP', u'S/WCI', u'SAFE', u'SBIG', u'SCOFCAH', u'SCSL', u'SEDENA', u'SEGPRES', u'SG', u'SHIG', u'SLA', u'SLA/U', u'SLV', u'SOCAR', u'SPD', u'SR', u'SRSG', u'STAFFDEL', u'SWIFT', u'TBA', u'TFG', u'TFTP', u'TFTP/SWIFT', u'TIP', u'TSA', u'TSCC', u'TSCTP', u'U.S.-EU', u'U.S.-UK', u'U.S./UK', u'U/SYG', u'UAE', u'UAV', u'UDF', u'UK', u'UMP', u'UN', u'UNCHR', u'UNESCO', u'UNFCCC', u'UNGA', u'UNHCR', u'UNIFIL', u'UNODC', u'UNSC', u'UNSCOL', u'UNSCR', u'UPR', u'US', u'US-CU', u'US-EU', u'US-ROYG', u'USDP', u'USEB', u'USG', u'USTR', u'V/FM', u'VARIG', u'VFM', u'VI', u'VOA', u'VP', u'WEF', u'WTO', u'XVI', u'ZANU-PF'])
    acronyms = find_acronyms('./cable/')
    diff = acronyms ^ current_acronyms
    if diff:
        print 'difference: ', diff
        print sorted(acronyms)


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
Tests references parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from cablemap.core.reader import parse_references

def test_parse_references():
    """
    >>> # 07TBILISI1732
    >>> parse_references('\\nREF: A. TBILISI 1605  B. TBILISI 1352  C. TBILISI 1100  D. 06 TBILISI 2601  E. 06 TBILISI 2590  F. 06 TBILISI 2425  G. 06 TBILISI 2390  H. 06 TBILISI 1532  I. 06 STATE 80908  J. 06 TBILISI 1064  K. 06 TBILISI 0619  L. 06 TBILISI 0397  M. 06 MOSCOW 0546  N. 06 TBILISI 0140  O. 05 TBILISI 3171', 2007)
    [u'07TBILISI1605', u'07TBILISI1352', u'07TBILISI1100', u'06TBILISI2601', u'06TBILISI2590', u'06TBILISI2425', u'06TBILISI2390', u'06TBILISI1532', u'06STATE80908', u'06TBILISI1064', u'06TBILISI619', u'06TBILISI397', u'06MOSCOW546', u'06TBILISI140', u'05TBILISI3171']
    >>> # 08PARIS1698
    >>> parse_references('\\nREF: A. PARIS 1501 \\nB. PARIS 1568 \\nC. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832 \\n0617 08)\\nD. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832 \\n0626 08) ', 2008)
    [u'08PARIS1501', u'08PARIS1568']
    >>> # 08PARIS1501
    >>> parse_references('\\nREF: A. 05 PARIS 5459 \\nB. 06 PARIS 5733', 2008)
    [u'05PARIS5459', u'06PARIS5733']
    >>> # 07TALLINN375
    >>> parse_references('\\nREF: A) TALLINN 366 B) LEE-GOLDSTEIN EMAIL 05/11/07 \\nB) TALLINN 347 ', 2007)
    [u'07TALLINN366', u'07TALLINN347']
    >>> # 07TRIPOLI943
    >>> parse_references('\\nREF: A) STATE 135205; B) STATE 127608; C) JOHNSON-STEVENS/GODFREY E-MAIL 10/15/07; D) TRIPOLI 797; E) TRIPOLI 723 AND PREVIOUS', 2007)
    [u'07STATE135205', u'07STATE127608', u'07TRIPOLI797', u'07TRIPOLI723']
    >>> # 07STATE156011
    >>> parse_references('\\nREF: LA PAZ 2974', 2007)
    [u'07LAPAZ2974']
    >>> # 05PARIS7835
    >>> parse_references('\\nREF: A. (A) PARIS 7682 AND PREVIOUS ', 2005)
    [u'05PARIS7682']
    >>> # 05PARIS7835
    >>> parse_references('\\nREF: A. (A) PARIS 7682 AND PREVIOUS \\n\\nB. (B) EMBASSY PARIS DAILY REPORT FOR OCTOBER 28 - \\nNOVEMBER 16 (PARIS SIPRNET SITE) \\nC. (C) PARIS 7527 ', 2005)
    [u'05PARIS7682', u'05PARIS7527']
    >>> # 09MADRID869
    >>> parse_references('\\nSUBJECT: UPDATES IN SPAIN’S INVESTIGATIONS OF RUSSIAN MAFIA \\nREF: A. OSC EUP20080707950031  B. OSC EUP20081019950022  C. OSC EUP20090608178005  D. MADRID 286  E. OSC EUP20050620950076  F. OSC EUP20080708950049  G. OSC EUP20081029950032  H. OSC EUP 20061127123001\\nMADRID 00000869 001.2 OF 004\\n', 2009)
    [u'09MADRID286']
    >>> # 07STATE152317
    >>> parse_references('\\nREF: (A)STATE 071143, (B)STATE 073601, (C)STATE 72896, (D)BEIJING \\n5361, (E) STATE 148514', 2007)
    [u'07STATE71143', u'07STATE73601', u'07STATE72896', u'07BEIJING5361', u'07STATE148514']
    >>> # 08MANAGUA573
    >>> parse_references('\\nREF: A. MANAGUA 520 \\nB. MANAGUA 500 \\nC. MANAGUA 443 \\nD. MANAGUA 340 \\nE. MANAGUA 325 \\nF. MANAGUA 289 \\nG. MANAGUA 263 \\nH. MANAGUA 130 \\nI. 2007 MANAGUA 2135 \\nJ. 2007 MANAGUA 1730 \\nK. 2007 MANAGUA 964 \\nL. 2006 MANAGUA 2611 ', 2008)
    [u'08MANAGUA520', u'08MANAGUA500', u'08MANAGUA443', u'08MANAGUA340', u'08MANAGUA325', u'08MANAGUA289', u'08MANAGUA263', u'08MANAGUA130', u'07MANAGUA2135', u'07MANAGUA1730', u'07MANAGUA964', u'06MANAGUA2611']
    >>> # 66BUENOSAIRES2481
    >>> parse_references('\\n REF: STATE 106206 CIRCULAR; STATE CA-3400 NOV 2, 1966 ', 1966)
    [u'66STATE106206']
    >>> #04MADRID4063
    >>> parse_references('\\nREF: EMBASSY MADRID E-MAIL TO EUR/WE OF OCTOBER 14\\n', 2004)
    []
    >>> #08RIYADH1134
    >>> parse_references('\\nREF: A. SECSTATE 74879 \\n     B. RIYADH 43 \\n', 2008)
    [u'08STATE74879', u'08RIYADH43']
    >>> #08RIODEJANEIRO165
    >>> parse_references('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\\n\\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ', 2008)
    [u'08RIODEJANEIRO138', u'08RIODEJANEIRO44']
    >>> parse_references('\\nREF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008)
    [u'08STATE54183', u'07BRASILIA1868', u'08STATE57700', u'07STATE17940']
    >>> # 08BRASILIA806
    >>> parse_references('\\nPROGRAM REF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008)
    [u'08STATE54183', u'07BRASILIA1868', u'08STATE57700', u'07STATE17940']
    >>> # 06SAOPAULO276
    >>> parse_references('\\nCARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA REF: (A) 05 SAO PAULO 405; (B) 05 SAO PAULO 402 (C) 02 BRASILIA 2670', 2006)
    [u'05SAOPAULO405', u'05SAOPAULO402', u'02BRASILIA2670']
    >>> # 08BERLIN1387
    >>> parse_references('\\nREF: A. BERLIN 1045\\nB. SECDEF MSG DTG 301601z SEP 08', 2008)
    [u'08BERLIN1045']
    >>> #09NAIROBI1938
    >>> parse_references('\\nREF: A. 08 STATE 81854\\n\\n\\nS e c r e t nairobi 001938', 2009)
    [u'08STATE81854']
    >>> # 02ROME1196
    >>> parse_references('\\nREF: A. STATE 40721\\n CONFIDENTIAL\\nPAGE 02 ROME 01196 01 OF 02 082030Z  B. ROME 1098  C. ROME 894  D. MYRIAD POST-DEPARTMENT E-MAILS FROM 10/01-02/02  E. ROME 348\\nCLASSIFIED BY: POL', 2002)
    [u'02STATE40721', u'02ROME1098', u'02ROME894', u'02ROME348']
    >>> # 10TRIPOLI167
    >>> parse_references('\\nREF: TRIPOLI 115\\n\\n1.(SBU) This is an action request; please see para 4.\\n\\n', 2010)
    [u'10TRIPOLI115']
    >>> # 06BRASILIA882
    >>> parse_references('SUBJECT: ENERGY INSTALLATIONS REF: BRASILIA 861', 2006)
    [u'06BRASILIA861']
    >>> # 08MOSCOW864
    >>> parse_references("TAGS: EPET ENRG ECON PREL PGOV RS\\nSUBJECT: WHAT'S BEHIND THE RAIDS ON TNK-BP AND BP REF: A. MOSCOW 816 B. MOSCOW 768 C. 07 MOSCOW 3054 Classified By: Ambassador William J. Burns for Reasons 1.4 (b/d)\\n", 2008)
    [u'08MOSCOW816', u'08MOSCOW768', u'07MOSCOW3054']
    >>> # 08TRIPOLI402
    >>> parse_references('REF: A) TRIPOLI 199, B) TRIPOLI 227 TRIPOLI 00000402 \\n\\n001.2 OF 003 ', 2008, '08TRIPOLI402')
    [u'08TRIPOLI199', u'08TRIPOLI227']
    """

_TRIPOLI_TESTS = {
'08TRIPOLI564': (
"""
RESIGN SOON 
 
REF: TRIPOLI 227  TRIPOLI 00000564  001.2 OF 002   CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy - Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (S/NF)
""", 2008, [u'08TRIPOLI227']),
'08TRIPOLI494': (
"""
E.O. 12958: DECL:  6/18/2018 
TAGS: PGOV PREL PHUM PINR LY
SUBJECT: JOURNALIST JAILED FOR CRITICIZING GOVERNMENT'S 
POORLY-COORDINATED DEVELOPMENT PROJECTS  CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary:  A respected [...]"""
, 2008, []),
'08TRIPOLI574': (
"""
SUBJECT: U.K. VISIT TO RABTA CHEMICAL WEAPONS PRODUCTION FACILITY 
 
REF: TRIPOLI 466  CLASSIFIED BY: John T. Godfrey, CDA, U.S. Embassy - Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary: T [...]
""", 2008, [u'08TRIPOLI466']),
'08TRIPOLI466': (
"""
TAGS: PARM PREL CWC OPCW CBW CH JA IT LY
SUBJECT: CHEMICAL WEAPONS CONVENTION (CWC): CONVERSION OF THE RABTA CHEMICAL WEAPONS PRODUCTION FACILITY  REF: A) STATE 58476, B) THE HAGUE 482, C) TRIPOLI 119  CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary:  The"""
, 2008, [u'08STATE58476', u'08THEHAGUE482', u'08TRIPOLI119'])
}


def test_malformed_tripoli_cables():
    def check_reference_extraction(content, year, reference_id, expected_result):
        assert parse_references(content, year, reference_id) == expected_result
    for ref_id, params in _TRIPOLI_TESTS.iteritems():
        content, year, result = params
        yield check_reference_extraction, content, year, ref_id, result


if __name__ == '__main__':
    import doctest
    doctest.testmod()

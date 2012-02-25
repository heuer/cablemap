# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2012 -- Lars Heuer <heuer[at]semagia.com>
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
Tests classificationist parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.reader import parse_classificationists

_TEST_DATA = (
    (u'10TOKYO397', u'Marc Wall', u'''FIELD

REF: STATE 015541

Classified By: Acting Deputy Chief of Mission Marc Wall for Reasons 1.4
 (b) and (d)

¶1. (C) SUM'''),
    (u'10GENEVA249', u'Rose E. Gottemoeller', u'''REF: 10 GENEVA 231 (SFO-GVA-VIII-088) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) '''),
    (u'10GENEVA247', u'Rose E. Gottemoeller', u'''REF: 10 GENEVA 245 (SFO-GVA-VIII-086) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) ¶1. (U) This '''),
    (u'10UNVIEVIENNA77', u'Glyn T. Davies', u'''Classified By: Ambassador Glyn T. Davies for reasons 1.4 b and d '''),
    (u'10WARSAW117', u'F. Daniel Sainz', u'''Classified By: Political Counselor F. Daniel Sainz for Reasons 1.4 (b) and (d) '''),
    (u'10STATE16019', u'Karin L. Look', u'''Classified By: Karin L. Look, Acting ASSISTANT SECRETARY, VCI. Reason: 1.4 (b) and (d).'''),
    (u'10LILONGWE59', u'Bodde Peter', u'''CLASSIFIED BY: Bodde Peter, Ambassador; REASON: 1.4(B) '''),
    (u'95ZAGREB4339', u'ROBERT P. FINN', u'''
1.  (U)  CLASSIFIED BY ROBERT P. FINN, DEPUTY CHIEF OF
MISSION.  REASON: 1.5 (D)
 '''),
    (u'95DAMASCUS5748', u'CHRISTOPHER W.S. ROSS', u'''SUBJECT:  HAFIZ AL-ASAD: LAST DEFENDER OF ARABS

1. CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY:
CHRISTOPHER W.S. ROSS, AMBASSADOR.  REASON: 1.5 (D) .

2. SUMMAR'''),
    (u'95TELAVIV17504', (), u'''
1.  CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY SECTION 1.5 (B)
AND (D).  NIACT PRECEDENCE BECAUSE OF GOVERNMENT CRISIS IN
ISRAEL.

2.  SU'''),
    (u'95RIYADH5221', u'THEODORE KATTOUF', u'''
1.  CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY DCM
THEODORE KATTOUF - 1.5 B,D.

2.  (C)'''),
    (u'96ADDISABABA1545', u'JEFFREY JACOBS', u'''
1.  (U)  CLASSIFIED BY POLOFF JEFFREY JACOBS, 1.5 (D).

2.  (C)'''),
    (u'96AMMAN2094', u'ROBERT BEECROFT', u'''
1. (U)  CLASSIFIED BY CHARGE ROBERT BEECROFT; REASON 1.5 (D).

2. (C) '''),
    (u'96STATE86789', u'MARY BETH LEONARD', u'''
1.  CLASSIFIED BY AF/C - MARY BETH LEONARD, REASON 1.5
(D). '''),
    (u'96NAIROBI6573', u'TIMOTHY CARNEY', u'''
1.  CLASSIFIED BY AMBASSADOR TO SUDAN TIMOTHY CARNEY.
REASON 1.5(D).
 '''),
    (u'96RIYADH2406', u'THEODORE KATTOUF', u'''SUBJECT:  CROWN PRINCE ABDULLAH THE DIPLOMAT

1.  (U) CLASSIFIED BY CDA THEODORE KATTOUF, REASON 1.5.D.

2. '''),
    (u'96RIYADH2696', u'THEODORE KATTOUF', u'''
1.  (U)  CLASSIFIED BY CHARGE D'AFFAIRES THEODORE
KATTOUF: 1.5 B, D.
 '''),
    (u'96ISLAMABAD5972', u'THOMAS W. SIMONS, JR.', u'''
1.  (U) CLASSIFIED BY THOMAS W. SIMONS, JR., AMBASSADOR.
REASON:  1.5 (B), (C) AND (D).
 '''),
    (u'96ISLAMABAD5972', u'Thomas W. Simons, Jr.', u'''
1.  (U) CLASSIFIED BY THOMAS W. SIMONS, JR., AMBASSADOR.
REASON:  1.5 (B), (C) AND (D).
 ''', True),
    (u'96STATE183372', u'LEE 0. COLDREN', u''' 
1.  (U) CLASSIFIED BY LEE 0. COLDREN, DIRECTOR, SA/PAB, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 '''),
    (u'96STATE183372', u'Lee O. Coldren', u''' 
1.  (U) CLASSIFIED BY LEE 0. COLDREN, DIRECTOR, SA/PAB, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 ''', True),
    (u'96ASHGABAT2612', u'TATIANA C. GFOELLER', u''' 
1.  (U) CLASSIFIED BY CHARGE TATIANA C. GFOELLER. 
REASON:  1.5 D. 
 '''),
    (u'96BOGOTA8773', u'S.K. ABEYTA', u''' 
1.  CLASSIFIED BY POL/ECONOFF. S.K. ABEYTA.  REASON:  1.5(D) 
 '''),
    (u'96STATE194868', u'E. GIBSON LANPHER, JR.', u''' 
1.   (U) CLASSIFIED BY E. GIBSON LANPHER, JR., ACTING 
ASSISTANT SECRETARY OF STATE FOR SOUTH ASIAN AFFAIRS, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 '''),
    (u'96JAKARTA7841', u'ED MCWILLIAMS', u''' 
1.  (U) CLASSIFIED BY POL COUNSELOR ED MCWILLIAMS; 
REASON 1.5(D) 
 '''),
    (u'96JERUSALEM3094', u'EDWARD G. ABINGTON, JR.', u''' 
1.  CLASSIFIED BY CONSUL GENERAL EDWARD G. ABINGTON, JR.  REASON 
1.5 (B) AND (D). 
 '''),
    (u'96BOGOTA10967', u'S.K. ABEYTA', u''' 
1.  (U)  CLASSIFIED BY POL/ECONOFF S.K. ABEYTA.  REASON 1.5(D). 
 '''),
    (u'04MUSCAT2112', u'Richard L. Baltimore, III', u''' 
Classified By: Ambassador Richard L. Baltimore, III. 
Reasons: 1.4 (b) and (d). 
 '''),
    (u'04MUSCAT2112', u'Richard L. Baltimore, III', u''' 
Classified By: Ambassador Richard L. Baltimore, III. 
Reasons: 1.4 (b) and (d). 
 ''', True),
    (u'05OTTAWA1975', u'Patricia Kim-Scott', u''' 
Classified By: Pol/Mil Officer Patricia Kim-Scott.  Reason E.O. 12958, 
1.4 (b) and (d). 
 '''),
    (u'05BOGOTA6208', u'William B. Wood', u''' 
Classified By: Ambassador William B. Wood; reasons 1.4 
(b) and (d) 
 '''),
    (u'05TAIPEI2839', u'Douglas Paal', u''' 
Classified By: AIT Director Douglas Paal, Reason(s): 1.4 (B/D). 
 '''),
    (u'05DHAKA3073', u'D.C. McCullough', u''' 
Classified By: A/DCM D.C. McCullough, reason para 1.4 (b) 
 '''),
    (u'09NAIROBI1132', u'Jessica Davis Ba', u''' 
Classified By: Pol/Econ Officer Jessica Davis Ba for reasons 1.4(b) and 
 (d) 
 '''),
    (u'08ROME1541', u'Liz Dibble', u''' 
Classified By: Classified by DCM Liz Dibble for reasons 1.4 (b) and 
(d). 
 '''),
    (u'06BAGHDAD2082', u'DANIEL SPECKHARD', ur''' 
Classified By: CHARGE D\'AFFAIRES DANIEL SPECKHARD FOR REASONS 1.4 (A), 
(B) AND (D) 
 '''),
    (u'05ANKARA4653', u'Nancy McEldowney', u''' 
Classified By: (U) CDA Nancy McEldowney; E.O. 12958, reasons 1.4 (b,d) 
 '''),
    (u'05QUITO2057', u'LARRY L. MEMMOTT', u''' 
Classified By: ECON LARRY L. MEMMOTT, REASONS 1.4 (B,D) 
 '''),
    (u'06HONGKONG3559', u'LAURENT CHARBONNET', u''' 
CLASSIFIED BY: ACTING DEPUTY PRINCIPAL OFFICER LAURENT CHARBONNET.  REA 
SONS: 1.4 (B,D) 
 '''),
    (u'09BAGHDAD791', u'Patricia Butenis', u''' 
Classified By: Charge d\' Affairs Patricia Butenis for reasons 1.4 (b) a 
nd (d) 
 '''),
    (u'06OSLO19', u'Christopher W. Webster', u''' 
Classified By: Charge d\'Affaires a.i. Christopher W. Webster, 
reason 1.4 (b) and (d) 
 '''),
    (u'08BEIJING3386', u'Aubrey Carlson', u''' 
Classified By: Political Section Minister Counselor Aubrey Carlson.  Re 
asons 1.4 (b/d). 
 '''),
    (u'09MOSCOW2393', u'Susan M. Elliott', u''' 
Classified By: Political Minister Counselor Susan M. Elliott for reason 
s:  1.4 (b), (d). 
 '''),
    (u'10BRUSSELS66', u'Christopher R. Davis', u''' 
Classified By: Political Minister-Counselor Christopher R. Davis for re 
ason 1.4 (b/d) 
 '''),
    (u'06BEIJING22125', u'ROBERT LUKE', u''' 
Classified By: (C) CLASSIFIED BY MINISTER COUNSELOR FOR ECONOMIC AFFAIR 
S ROBERT LUKE; REASON 1.4 (B) AND (D). 
 '''),
    (u'07CAIRO622', u'William R. Stewart', u''' 
Classified by:  Minister Counselor for Economic and 
Political Affairs William R. Stewart for reasons 1.4(b) and 
(d). 
 '''),
    (u'07BAGHDAD1188', u'Daniel Speckhard', u''' 
Classified By: Charge Affaires Daniel Speckhard.  Reasons: 1.4 (b) and 
(d). 
 '''),
    (u'08PARIS1131', u'STUART DWYER', u''' 
Classified By: ECONCOUNS STUART DWYER FOR REASONS 1.4 B AND D 
 '''),
    (u'08ATHENS985', u'Jeff Hovenier', u''' 
Classified By: A/Political Counselor Jeff Hovenier for 
1.4 (b) and (d) 
 '''),
    (u'09BEIJING2690', u'William Weinstein', u''' 
Classified By: This message classified by Econ Minister Counselor 
William Weinstein for reasons 1.4 (b), (d) and (e). 
 '''),
    (u'06VILNIUS945', u'Rebecca Dunham', u''' 
Classified By: Political and Economic Section Chief Rebecca Dunham for 
reasons 1.4 (b) and (d) 
 '''),
    (u'07BAGHDAD2781', u'Howard Keegan', u''' 
Classified By: Kirkuk PRT Team Leader Howard Keegan for reason 1.4 (b) 
and(d). 
 '''),
    (u'09HARARE864', u'Donald Petterson', u''' 
Classified By: Charge d\'affaires, a.i. Donald Petterson for reason 1.4 
(b). 
 '''),
    (u'04MANAMA525', u'Robert S. Ford', u''' 
Classified By: Charge de Affaires Robert S. Ford for reasons 
1.4 (b) and (d). 
 '''),
    (u'08STATE56778', u'Patricia A. McNerney', u''' 
Classified By: ISN Acting Assistant Secretary 
Patricia A. McNerney, Reasons 1.4 b, c, and d 
 '''),
    (u'07BRUSSELS1462', u'Larry Wohlers', u''' 
Classified By: USEU Political Minister Counselor Larry Wohlers 
for reasons 1.4 (b) and (d). 
 '''),
    (u'09KABUL2261', u'Hoyt Yee', u''' 
Classified By: Interagency Provincial Affairs Deputy Coordinator Hoyt Y 
ee for reasons 1.4 (b) and (d) 
 '''),
    (u'09KABUL1233', u'Patricia A McNerney', u''' 
Classified By: PRT and Sub-National Governance Acting Director Patricia 
 A McNerney for reasons 1.4 (b) and (d) 
 '''),
    (u'09BRUSSELS1288', u'CHRISTOPHER DAVIS', u''' 
Classified By: CLASSIFIED BY USEU MCOUNSELOR CHRISTOPHER DAVIS, FOR REA 
 
SONS 1.4 (B) AND (D) 
 '''),
    (u'06TAIPEI3165', u'Stephen M. Young', u''' 
Classified By: Classified by AIT DIR Stephen M. Young. 
Reasons:  1.4 b, d. 
 '''),
    (u'07BRUSSELS1208', u'Courtney Nemroff', u''' 
Classified By: Institutional Affairs Unit Chief Courtney Nemroff for re 
asons 1.4 (b) & (d) 
 '''),
    (u'05CAIRO8602', u'Michael Corbin', u''' 
Classified by ECPO Minister-Counselour Michael Corbin for 
reasons 1.4 (b) and (d). 
 '''),
    (u'09MADRID1210', u'Arnold A. Chacon', u''' 
Classified By: Charge d'Affaires, a.i., Arnold A. Chacon 
 
1.(C) Summary:  In his meetings with Spanish officials, 
Special Envoy for Eurasian Energy'''),
    (u'05SINGAPORE887', u'Laurent Charbonnet', u''' 
Classified By: E/P Counselor Laurent Charbonnet, Reasons 1.4(b)(d) 
 '''),
    (u'09SINGAPORE677', u'Dan Jassem', u''' 
Classified By: Acting E/P Counselor Dan Jassem for reasons 1.4 (b) and 
(d) 
 '''),
    (u'08BELGRADE1189', u'Thatcher Scharpf', u''' 
Classified By: Acting Deputy Chief of Mission Thatcher Scharpf for reas 
ons 1.4(b/d). 
 '''),
    (u'09BAGHDAD3319', u'Rachna Korhonen', u''' 
Classified By: PRT Kirkuk Governance Section Head Rachna Korhonen for r 
easons 1.4 (b) and (d). 
 '''),
    (u'04ANKARA5897', u'Thomas Goldberger', u''' 
Classified By: (U) Classified by Economic Counselor Thomas Goldberger f 
or reasons 1.4 b,d. 
 '''),
    (u'00HARARE3759', u'TOM MCDONALD', u''' 
CLASSIFIED BY AMBASSADOR TOM MCDONALD. 
                       CONFIDENTIAL 
 
PAGE 02        HARARE  03759  01 OF 03  111533Z 
REASONS: 1.5 (B) AND (D). 
 
1.  (C)  SUMMARY:  ALTHOUGH WIDESPREAD FEARS OF A 
SPIKE'''),
    (u'07STATE156455', u'Glyn T. Davies', u''' 
Classified By: Glyn T. Davies 
 
SUMMARY 
------- 
 '''),
    (u'03GUATEMALA1727', u'Erik Hall', u''' 
Classified By: Labor Attache Erik Hall.  Reason 1.5 (d). 
 '''),
    (u'05VILNIUS503', u'LARRY BEISEL', u''' 
Classified By: DEFENSE ATTACHE LTC LARRY BEISEL FOR REASONS 1.4 (B) AND 
 (D). 
 '''),
    (u'08USUNNEWYORK729', u'Carolyn L. Willson', u''' 
Classified By: USUN Legal Adviser Carolyn L. Willson, for reasons 
1.4(b) and (d) 
 '''),
    (u'04BRUSSELS4688', u'Jeremy Brenner', u''' 
Classified By: USEU polmil officer Jeremy Brenner for reasons 1.4 (b) a 
nd (d) 
 '''),
    (u'08GUATEMALA1416', u'Drew G. Blakeney', u''' 
Classified By: Pol/Econ Couns Drew G. Blakeney for reasons 1.4 (b&d). 
 '''),
    (u'08STATE77798', u'Brian H. Hook', u''' 
Classified By: IO Acting A/S Brian H. Hook, E.O. 12958, 
Reasons: 1.4(b) and (d) 
 
 '''),
    (u'05ANKARA1071', u'Margaret H. Nardi', u''' 
Classified By: Acting Counselor for Political-Military Affiars Margaret 
 H. Nardi for reasons 1.4 (b) and (d). 
 '''),
    (u'08MOSCOW3655', u'David Kostelancik', u''' 
Classified By: Deputy Political M/C David Kostelancik.  Reasons 1.4 (b) 
 and (d). 
 '''),
    (u'09STATE75025', u'Richard C. Holbrooke', u''' 
Classified By: Special Representative for Afghanistan and Pakistan 
Richard C. Holbrooke 
 
1.  (U)  This is an action request; see paragraph 4. 
 '''),
    (u'10KABUL688', u'Joseph Mussomeli', u''' 
Classified By: Assistant Chief of Mission Joseph Mussomeli for Reasons 
1.4 (b) and (d) 
 '''),
    (u'98USUNNEWYORK1638', u'HOWARD STOFFER', u''' 
CLASSIFIED BY DEPUTY POLITICAL COUNSEL0R HOWARD STOFFER 
PER 1.5 (B) AND (D).  ACTION REQUEST IN PARA 10 BELOW. 
 '''),
    (u'02ROME3119', u'PIERRE-RICHARD PROSPER', u''' 
CLASSIFIED BY: AMBASSADOR-AT-LARGE PIERRE-RICHARD PROSPER 
FOR REASONS 1.5 (B) AND (D) 
 '''),
    (u'02ANKARA8447', u'Greta C. Holtz', u''' 
 
Classified by Consul Greta C. Holtz for reasons 1.5 (b) & (d). 
 '''),
    (u'09USUNNEWYORK282', u'SUSAN RICE', u''' 
Classified By: U.S. PERMANENT REPRESENATIVE AMBASSADOR SUSAN RICE 
FOR REASONS 1.4 B/D 
 '''),
    (u'09DHAKA339', u'Geeta Pasi', u''' 
Classified By: Charge d'Affaires, a.i. Geeta Pasi.  Reasons 1.4 (b) and 
 (d) 
 '''),
    (u'06USUNNEWYORK2273', u'Alejandro D. Wolff', u''' 
Classified By: Acting Permanent Representative Alejandro D. Wolff 
 per reasons 1.4 (b) and (d) 
 '''),
    (u'08ISLAMABAD1494', u'Anne W. Patterson', u''' 
Classified By: Ambassador Anne W. Patterson for reaons 1.4 (b) and (d). 
 
1. (C) Summary: During'''),
    (u'08BERLIN1150', u'Robert Pollard', u''' 
Classified By: Classified by Economic Minister-Counsellor 
Robert Pollard for reasons 1.4 (b) and (d) 
 '''),
    (u'08STATE104902', u'DAVID WELCH', u''' 
Classified By: 1. CLASSIFIED BY NEA ASSISTANT SECRETARY DAVID WELCH 
REASONS: 1.4 (B) AND (D) 
 '''),
    (u'07VIENTIANE454', u'Mary Grace McGeehan', u''' 
Classified By: Charge de'Affairs ai. Mary Grace McGeehan for reasons 1. 
4 (b) and (d) 
 '''),
    (u'07ROME1948', u'William Meara', u''' 
Classified By: Acting Ecmin William Meara for reasons 1.4 (b) and (d) 
 '''),
    (u'07USUNNEWYORK545', u'Jackie Sanders', u''' 
Classified By: Amb. Jackie Sanders. E.O 12958. Reasons 1.4 (B&D). 
 '''),
    (u'06USOSCE113', u'Bruce Connuck', u''' 
Classified By: Classified by Political Counselor Bruce Connuck for Reas 
(b) and (d). 
 '''),
    (u'09DOHA404', u'Joseph LeBaron', u''' 
Classified By: Ambassaor Joseph LeBaron for reasons 1.4 (b and d). 
 '''),
#    (u'09DOHA404', u'Joseph LeBaron', u''' 
#Classified By: Ambassaor Joseph LeBaron for reasons 1.4 (b and d). 
# ''', True),
    (u'09RANGOON575', u'Thomas Vajda', u''' 
Classified By: Charge d'Afairs (AI) Thomas Vajda for Reasons 1.4 (b) & 
 (d 
 '''),
    (u'03ROME3107', u'TOM COUNTRYMAN', u''' 
Classified By: POL MIN COUN TOM COUNTRYMAN, REASON 1.5(B)&(D). 
 '''),
    (u'06USUNNEWYORK732', u'Molly Phee', u''' 
Classified By: Deputy Political Counselor Molly Phee, 
for Reasons 1.4 (B and D) 
 '''),
    (u'06BAGHDAD1552', u'David M. Satterfield', u''' 
Classified By: Charge d'Affaires David M. Satterfield for reasons 1.4 ( 
b) and (d) 
 '''),
    (u'06ABUJA232', u'Erin Y. Tariot', u''' 
Classified By: USDEL Member Erin Y. Tariot, reasons 1.4 (b,d) 
 '''),
    (u'09ASTANA184', u'RICAHRD E. HOAGLAND', u''' 
Classified By: AMBASSADOR RICAHRD E. HOAGLAND: 1.2 (B), (D) 
 '''),
#    (u'09ASTANA184', u'Richard E. Hoagland', u''' 
#Classified By: AMBASSADOR RICAHRD E. HOAGLAND: 1.2 (B), (D) 
# ''', True),
    (u'09CANBERRA428', u'John W. Crowley', u''' 
Classified By: Deputy Political Counselor: John W. Crowley, for reasons 
 1.4 (b) and (d) 
 '''),
    (u'08TASHKENT706', u'Molly Stephenson', u''' 
Classified By: Classfied By: IO Molly Stephenson for reasons 1.4 (b) a 
nd (d). 
 '''),
    (u'08CONAKRY348', u'T. SCOTT BROWN', u''' 
Classified By: ECONOFF T. SCOTT BROWN FOR REASONS 1.4 (B) and (D) 
 '''),
    (u'07STATE125576', u'Margaret McKelvey', u''' 
Classified By: PRM/AFR Dir. Margaret McKelvey-reasons 1.4(b/d) 
 '''),
    (u'09BUDAPEST372', u'Steve Weston', u''' 
Classified By: Acting Pol/Econ Counselor:Steve Weston, 
reasons 1.4 (b and d) 
 '''),
    (u'04TAIPEI3162', u'David J. Keegan', u'''' 
Classified By: AIT Deputy Director David J. Keegan, Reason: 1.4 (B/D) 
 '''),
    (u'04TAIPEI3521', u'David J. Keegan', u''' 
Classified By: AIT Acting Director David J. Keegan, Reason: 1.4 (B/D) 
 '''),
    (u'04TAIPEI3919', u'David J. Keegan', u''' 
Classified By: AIT Director David J. Keegan, Reason 1.4 (B/D) 
 '''),
    (u'08JAKARTA1142', u'Stanley A. Harsha', u''' 
Classified By: Acting Pol/C Stanley A. Harsha for reasons 1.4 (b+d). 
 '''),
    (u'06ISLAMABAD16739', u'MARY TOWNSWICK', u''' 
Classified By: DOS CLASSIFICATION GUIDE BY MARY TOWNSWICK 
 
1.  (C)  Summary.  With limited government support, Islamic 
banking has gained momentum in Pakistan in the past three 
years.  The State Bank of Pakistan (SBP) reports that the 
capital base of the Islamic banking system has more than 
doubled since 2003 as the number of Islamic banks operating 
in Pakistan rose from one to four.  A media analysis of 
Islamic banking in Pakistan cites an increase in the number 
of conventional banks'''),
    (u'05DJIBOUTI802', u'JEFFREY PURSELL', u''' 
 (U) CLASSIFIED BY TDY RSO JEFFREY PURSELL FOR REASON 1.5 C. 
 '''),
    (u'09STATE82567', u'Eliot Kang', u''' 
Classified By: Acting DAS for ISN Eliot Kang. Reasons 1.4 (b) and (d) 
 
 '''),
    (u'04ANKARA5764', u'Charles O. Blah a', u''' 
Classified By: Classified by Deputy Political Counselor Charles O. Blah 
a, E.O. 12958, reasons 1.4 (b) and (d). 
 '''),
#    (u'04ANKARA5764', u'Charles O. Blaha', u''' 
#Classified By: Classified by Deputy Political Counselor Charles O. Blah 
#a, E.O. 12958, reasons 1.4 (b) and (d). 
# ''', True),
    (u'04ANKARA5764', u'Charles O. Blah a', u''' 
Classified By: Classified by Deputy Political Counselor Charles O. Blah 
a, E.O. 12958, reasons 1.4 (b) and (d). 
 '''),
    (u'10VIENNA195', u'J. Dean Yap', u''' 
Classified by: DCM J. Dean Yap (acting) for reasons 1.4 (b) 
and (d). 
 '''),
    (u'03HARARE175', u'JOHN S. DICARLO', u''' 
Classified By: RSO - JOHN S. DICARLO. REASON 1.5(D) 
 '''),
    (u'08LONDON2968', u'Greg Berry', u''' 
Classified By: PolMinCons Greg Berry, reasons 1.4 (b/d). 
 '''),
    (u'08HAVANA956', u'Jonathan Farrar', u''' 
Classified By: COM Jonathan Farrar for reasons 1.5 (b) and (d) 
 '''),
    (u'09BAGHDAD253', u'Robert Ford', u''' 
Classified By: Acting Deputy Robert Ford.  Reasons 1.4 (b) and (d) 
 '''),
    (u'09TIRANA81', u'JOHN L. WITHERS II', u''' 
Classified By: AMBASSADOR JOHN L. WITHERS II FR REASONS 1.4 (b) AND (d 
). 
 '''),
    (u'05HARARE383', u'Eric T. Schultz', u''' 
Classified By: Charge d'Affaires a.i. Eric T. Schultz under Section 1.4 
 b/d 
 '''),
    (u'07LISBON2591', u'Jenifer Neidhart', u''' 
Classified By: Pol/Econ Off Jenifer Neidhart for reasons 1.4 (b) and (d 
) 
 '''),
    (u'07STATE171234', u'Lawrence E. Butler', u''' 
Classified By:  NEA Lawrence E. Butler for reasons EO 12958 
1.4(b),(d), and (e). 
 '''),
    (u'04AMMAN8544', u'David Hale', u''' 
Classified By: Charge d'Affaries David Hale for Reasons 1.4 (b), (d) 
 '''),
    (u'07NEWDELHI5334', u'Ted Osius', u''' 
Classified By: Acting DCM/Ted Osius for reasons 1.4 (b and d) 
 '''),
    (u'04JAKARTA5072', u'ANTHONY C. WOODS', u''' 
Classified By: EST&H OFFICER ANTHONY C. WOODS FOR REASON 1.5 (b, d) 
 '''),
    (u'03AMMAN2822', u'Edward W. Gnehm', u''' 
Classified By: Ambassador Edward W. Gnehm.  Resons 1.5 (B) and (D) 
 '''),
    (u'08CANBERRA1335', u'Daniel A. Clune', u''' 
Classified By: Deputy Chief of Mission: Daniel A. Clune: Reason: 1.4 (c 
) and (d) 
 '''),
    (u'09HAVANA665', u'Charles Barclay', u''' 
Classified By: CDA: Charles Barclay for reQ#8$UQ8ML#C may choke oQhQGTzovisional\" controls, such as 
price caps and limits on the amount any one person could buy. 
 
 
3.  (SBU) Furthering speculation that the private markets 
were under the gun, official reports have resurfaced in 
recent months accusing private markets of artificially 
maintaining higher'''),
    (u'08STATE8993', u'Gregory B. Starr', u''' 
1. (U) Classified by Acting Assistant Secretary for Diplomatic 
Security Gregory B. Starr for E.O. 12958 reasons 1.4 (c) and 
(d). 
 '''),
    (u'09ISTANBUL137', u'Sandra Oudkirk', u''' 
Classified By: ConGen Istanbul DPO Sandra Oudkirk; Reason 1.5 (d) 
 '''),
 (u'08BANGKOK1778', u'James F. Entwistle', u''' 
Classified By: Charge, d,Affaires a. i. James F. Entwistle, reason 1.4 
(b) and (d). 
 '''),
 (u'08MANAMA301', u'Christopher Henzel', u''' 
Classified By: Charge d,Affaires a.i. Christopher Henzel, reasons 1.4(b 
) and (d). 
 
 '''),
    (u'06COLOMBO123', u'Robert O. Blake, Jr.', u''' 
Classified By: Abassador Robert O. Blake, Jr. for reasons 
1.4 (b and (d). 
 '''),
    (u'08YEREVAN907', u'Marie Yovanovitch', u''' 
Classified By: Amabassador Marie Yovanovitch.  Reason 1.4 (B/D) 
 '''),
    (u'09QUITO329', u'Heather M. Hodges', u''' 
Classified By: AMB Heather M. Hodges for reason 1.4 (D) 
 '''),
    #TODO: Should be: [Karl Wycoff, Shari Villarosa]
    (u'09STATE38028', u'KARL WYCOFF', u''' 
CLASSIFIED BY AF KARL WYCOFF, ACTING AND S/CT DAS SHARI 
VILLAROSA ; E.O. 12958 REASON: 1.4 (B) AND (D) 
 '''),
    (u'04ABUJA2060', u'BRUCE EHRNMAN', u''' 
Classified By: AF SPECIAL ADVISOR BRUCE EHRNMAN FOR REASONS 1.5 (B) AND 
 (D) 
 '''),
    (u'06ISLAMABAD3684', u'RCROCKER', u''' 
Classified By: AMB:RCROCKER, Reasons 1.4 (b) and (c) 
 '''),
    (u'06MANAMA184', u'William T.Monroe', u''' 
Classified By: Classified by Ambassadior William T.Monroe.  Reasons: 1. 
4 (b)(d) 
 '''),
    (u'07SANSALVADOR263', u'Charles Glazer', u''' 
Classified By: Ambasasdor Charles Glazer, Reasons 
1.4 (b) and (d) 
 '''),
    (u'05BRUSSELS1549', u'Michael Ranneberger', u''' 
Classified By: AF PDAS Michael Ranneberger.  Reasons 1.5 (b) and (d). 
 '''),
    (u'09STATE14163', u'Mark Boulware', u''' 
Classified By: AF Acting DAS Mark Boulware,  Reasons 1.4 (b) and (d). 
 '''),
    (u'06AITTAIPEI1142', u'Michael R. Wheeler', u''' 
Classified By: IPO Michael R. Wheeler for reason 1.4(G)(E) 
 '''),
    (u'08TAIPEI1038', u'Stephen M. Young', u''' 
Classified By: AIT Chairman Stephen M. Young, 
Reasons: 1.4 (b/d) 
 '''),
    (u'09STATE96519', u'Ellen O. Tauscher', u''' 
Classified By: T U/S Ellen O. Tauscher for Reasons 1.4 a,b,and d. 
 '''),
    (u'08NAIROBI232', u'JOHN M. YATES', u''' 
Classified By: SPECIAL ENVOY JOHN M. YATES 
 
1.  (C) '''),
)


def test_parse_classificationist():
    def check(cable_id, expected, content, normalize):
        if not isinstance(expected, tuple):
            expected = (expected,)
        eq_(expected, tuple(parse_classificationists(content, normalize)))
    for testcase in _TEST_DATA:
        if len(testcase) == 3:
            cable_id, expected, content = testcase
            normalize = False
        else:
            cable_id, expected, content, normalize = testcase
        yield check, cable_id, expected, content, normalize


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

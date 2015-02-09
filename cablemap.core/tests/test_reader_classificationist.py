# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests classificationist parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_, ok_
from cablemap.core import cable_by_id
from cablemap.core.reader import parse_classificationists

_TEST_DATA = (
    (u'10TOKYO397', u'Marc Wall', u'''FIELD

REF: STATE 015541

Classified By: Acting Deputy Chief of Mission Marc Wall for Reasons 1.4
 (b) and (d)

¶1. (C) SUM'''),
    (u'10GENEVA249', u'Rose E. Gottemoeller', u'''REF: 10 GENEVA 231 (SFO-GVA-VIII-088) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) '''),
    (u'10GENEVA247', u'Rose E. Gottemoeller', u'''REF: 10 GENEVA 245 (SFO-GVA-VIII-086) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) ¶1. (U) This '''),
    (u'10UNVIEVIENNA77', u'Glyn T. Davies', u'''\nClassified By: Ambassador Glyn T. Davies for reasons 1.4 b and d '''),
    (u'10WARSAW117', u'F. Daniel Sainz', u'''\nClassified By: Political Counselor F. Daniel Sainz for Reasons 1.4 (b) and (d) '''),
    (u'10STATE16019', u'Karin L. Look', u'''\nClassified By: Karin L. Look, Acting ASSISTANT SECRETARY, VCI. Reason: 1.4 (b) and (d).'''),
    (u'10LILONGWE59', u'Bodde Peter', u'''\nCLASSIFIED BY: Bodde Peter, Ambassador; REASON: 1.4(B) '''),
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
    (u'09DOHA404', u'Joseph LeBaron', u''' 
Classified By: Ambassaor Joseph LeBaron for reasons 1.4 (b and d). 
 ''', True),
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
    (u'09ASTANA184', u'Richard E. Hoagland', u''' 
Classified By: AMBASSADOR RICAHRD E. HOAGLAND: 1.2 (B), (D) 
 ''', True),
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
    (u'04ANKARA5764', u'Charles O. Blaha', u''' 
Classified By: Classified by Deputy Political Counselor Charles O. Blah 
a, E.O. 12958, reasons 1.4 (b) and (d). 
 '''),
    (u'04ANKARA5764', u'Charles O. Blaha', u''' 
Classified By: Classified by Deputy Political Counselor Charles O. Blah 
a, E.O. 12958, reasons 1.4 (b) and (d). 
 ''', True),
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
    (u'09STATE38028', (u'KARL WYCOFF', u'SHARI VILLAROSA'), u''' 
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
    (u'07COLOMBO769', u'Robert O. Blake, Jr.', u''' 
Classified By: Ambassodor Robert O. Blake, Jr. for reasons 1.4 (b, d). 
 '''),
    (u'04DJIBOUTI1541', u'MARGUERITA D. RAGSDALE', u''' 
Classified By: AMBASSSADOR MARGUERITA D. RAGSDALE. 
REASONS 1.4 (B) AND (D). 
 '''),
    (u'08MOSCOW3202', u'David Kostelancik', u''' 
Classified By: Acting Political MC David Kostelancik for reasons 1.4(b) 
 and (d). 
 '''),
    (u'09BEIJING939', u'Ben Moeling', u''' 
Classified By: Acting Political Minister-Couselor 
Ben Moeling, reasons 1.4 (b/d). 
 '''),
    (u'09HAVANA689', u'Jonathan Farrar', u''' 
Classified By: Principal Office Jonathan Farrar for reasons 1.4 (b) and 
 (d) 
 '''),
    (u'07VIENNA2687', u'J. Dean Yap', u''' 
Classified By: Political Economic Counselr J. Dean Yap for reasons 1.4 
 (b) and (d) 
 '''),
    (u'08LONDON1485', u'Maura Connelly', u''' 
Classified By: Political Minister Counsel Maura Connelly for reasons 1. 
4 (b/d). 
 '''),
    (u'07LONDON3228', u'JOHN MCNAMARA', u''' 
Classified By: A E/MIN COUNS. JOHN MCNAMARA, REASONS 1.4(B) AND (D) 
 '''),
    (u'05ABUJA2031', u'Rich Verrier', u''' 
Classified By: ARSO Rich Verrier for reason 1.4 (d) 
 '''),
    (u'09USOSCE235', u'Chris Ellis', u''' 
Classified By: Acting Chief Arms Control Delegate Chris Ellis, 
for reasons 1.4(b) and (d). 
 '''),
    (u'06RANGOON1542', u'Walter Parrs III', u''' 
Classified By: Conoff Walter Parrs III for Reasons 1.4 (b) and (d) 
 '''),
    (u'08STATE109148', u'Pam Durham', u''' 
Classified By: ISN/MTR Direcotr Pam Durham. 
Reason:  1.4 (B), (D). 
 '''),
    (u'08STATE3581', u'AFriedt', u''' 
Classified By: EUR/PRA, Dir. AFriedt, Reason 1.4 (b/d) 
 '''),
    (u'06HONGKONG3109', u'JEFF ZAISER', u''' 
CLASSIFIED BY: ACTING E/P CIEF JEFF ZAISER.  REASONS: 1.4(B,D). 
 '''),
    (u'07LAPAZ123', u'Brian Quigley', u''' 
Classified By: Acting Ecopol Councilor Brian Quigley for reasons 1.4 (d 
) and (e). 
 '''),
    (u'08BAGHDAD3818', u'Michael Dodman', u''' 
Classified By: A/EMIN Michael Dodman, Reasons 1.4 (b,d). 
 '''),
    (u'09BAGHDAD565', u'Michael Dodman', u''' 
Classified By: Acting EMIN Michael Dodman, reasons 1.4 (b,d). 
 '''),
    (u'09BUDAPEST198', u'Jon Martinson', u''' 
Classified By: Acting P/E Counseor Jon Martinson, reasons 1.4 (b,d) 
 '''),
    (u'09BUDAPEST276', u'Jon Martinson', u''' 
Classified By: Acting P/E Counsleor Jon Martinson, reasons 1.4 (b,d) 
 '''),
    (u'08STATE67468', u'George Krol', u''' 
Classified By: SCA/DAS for Central Asia George Krol 
 
 1.  (C) '''),
    (u'09STATE24316', u'GEORGE KROL', u''' 
Classified By: DEPUTY ASSISTANT SECRETARY OF STATE FOR 
CENTRAL ASIA GEORGE KROL FOR REASONS 1.4 (B) AND (D) 
 '''),
    (u'08STATE82744', u'BRIAN HOOK', u''' 
Classified By: CLASSIFIED BY IO A/S ACTING BRIAN HOOK 
FOR REASONS 1.4(B) AND (D). 
 '''),
    (u'09SINGAPORE773', u'Daniel Shields', u''' 
Classified By: Charge d'Affaires (CDA) Daniel Shields for Reasons 1.4 ( 
b/b) 
 '''),
    (u'07ASHGABAT350', u'Richard Hoagland', u''' 
Classified By: Classified by Acting Charge d\'Affaires, Ambassador Richa 
rd Hoagland, for reasons 1.4(B) and (D). 
 '''),
    (u'05NEWDELHI8162', u'Bob Blake', u''' 
Classified By: Charge' Bob Blake for Reasons 1.4 (B, D) 
 '''),
    (u'07RIYADH1028', u'BOB SILVERMAN', u''' 
Classified By: ECONOMIC COUNSELOR BOB SILVERMAN 
 FOR 12958 1.4 B, D, AND E 
 '''),
    (u'05ROME3781', u'ANNA BORG', u''' 
Classified By: DCM ANNA BORG BASED ON E.O.12958 REASONS 1.4 (b) and (d) 
 '''),
    (u'09STATE2508', u'PATRICIA A. MCNERNEA', u''' 
CLASSIFIED BY: ISN ? PATRICIA A. MCNERNEA, ACTING 
ASSISTANT SECRETARY, REASON 1.4 (B) AND (D) 
 '''),
    (u'03OTTAWA2182', u'Mary Witt', u''' 
Classified By: A/ Pol Min Mary Witt for reasons 1.5(b) and (d) 
 '''),
    (u'03KUWAIT3762', u'FRANK URBANCIC', u''' 
Classified By: CDA FRANK URBANCIC BASED UPON REASONS 1.5 (B) AND (D) 
 '''),
    (u'07DAKAR1464', u'GARY SCHAAF', u''' 
Classified By: A/LEGATT GARY SCHAAF FOR RASONS 1.4 (B) AND (D). 
 '''),
    (u'07HARARE680', u'Glenn Warren', u''' 
Classified By: Pol/Econ Chief Glenn Warren under 1.4 b/d 
 '''),
    (u'09DHAKA775', u'James Moriarty', u''' 
Classified By: Ambassador James Moriarty for for reasons 1.4 b and d. 
 '''),
    (u'', u'Kelly A. Keiderling', u'''
Classified By: CDA Kelly A. Keiderling under 1.4 (b) and (d)
'''),
    (u'04HARARE1722', u'Paul Weisenfeld', u''' 
Classified By: Classified by Charge d'Affaires Paul Weisenfeld under Se 
ction 1.5 b/d 
 '''),
    (u'05SANTIAGO2540', u'SEAN MURPHY', u''' 
Classified By: CONSUL GENERAL SEAN MURPHY 
 
1. In a December 19 m'''),
    (u'04HELSINKI1420', u'Earle I. Mack', u''' 
Classified By: Ambassador Earle I. Mack for reasons 1.5(B) and (D) 
 
Summary 
------- 
 '''),
    (u'08PORTAUPRINCE520', u'Janet A. Sanderson', u''' 
Classified By: Ambassado Janet A. Sanderson for reasons 1.4 (b) and (d 
) 
 '''),
    (u'97SOFIA3097', u'B0HLEN', u''' 
1.(U)  CLASSIFIED BY AMBASSAD0R B0HLEN.  REAS0N: 
1.5(B,D). 
 '''),
    (u'99TUNIS2120', u'R0BIN L. RAPHEL', u''' 
(U)  CLASSIFIED BY AMBASSAD0R R0BIN L. RAPHEL BASED 0N 1.5 (B) 
AND (D). 
 '''),
    (u'08TBILISI1121', u'John F. Tefft', u''' 
Classified By: Ambassadot John F. Tefft for reason 1.4 (b) and (d). 
 '''),
    (u'07ANKARA2522', u'ROSS WILSON', u''' 
Classified By: AMBASSADR ROSS WILSON FOR REASONS 1.4 (B) AND (D) 
 '''),
    (u'09UNVIEVIENNA531', u'Glyn T. Davies', u''' 
Classified By: Ambassadro Glyn T. Davies, reasons 1.4 (b) and (d) 
 '''),
    (u'09TBILISI463', u'JOHN F. TEFFT', u''' 
Classified By: AMBSSADOR JOHN F. TEFFT.  REASONS:  1.4 (B) AND (D). 
 '''),
    (u'09LUSAKA523', u'Donald E. Booth', u''' 
Classified By: Classified By: Ambbassador Donald E. Booth for 
Reasons 1.4 (b) and (d) 
 
 '''),
    (u'07BAKU486', u'Anne E. Derse', u''' 
Classified By: Ambssador Anne E. Derse, Reasons 1.4 (b,d) 
 '''),
    (u'09ANKARA63', u'A.F. Godfrey', u''' 
Classified By: Pol-Mil Counselor A.F. Godfrey 
 
Will Not Break Silence... 
------------------------- 
 
1. (C) I'''),
    (u'03SANAA1319', u'ALAN MISENHEIMER', u''' 
Classified By: CHARGE ALAN MISENHEIMER F0R REASONS 1.5 (B) AND (D) 
 '''),
    (u'08BAKU668', u'Alan Eyre', u''' 
Classified By: Acting Pol/Econ Chief Alan Eyre 
 
(S) In '''),
    (u'07SINGAPORE285', u'Ike Reed', u''' 
Classified By: Economical and Political Chief Ike Reed; 
reasons 1.4 (b) and (d) 
 '''),
    (u'07KHARTOUM832', u'Roberto Powers', r''' 
Classified By: CDA Roberto Powers a.y., Sea3on: Sectaons 9.Q (b+`ald$hd 
)Q 
Q,----/-Qswmmfrq 
=,=--=HQ(@(RBF!&}ioSQB3wktf0r,vu qDWTel$1` \ulQlQO~jcvq>&Mw~ifw(U= ;QGM?QQx7Ab8QQ@@)\Minawi suggested that 
intelligence chief Salah Ghosh was the sole interlocutor with 
the "statesmanship" and influence within the regime to defuse 
tensions with the international community.  Embassy officials 
told Minawi that the NCP would need to demonstrate its 
genuine desire for better relations by agreeing to an 
effective UN peace-keeping operation, which could then lay 
the basis for future discussions.  Minawi also commented on 
Chad's obstruction of the Darfur peace process and an 
upcoming visit of Darfurian officials to Arab capitals.  End 
summary. 
 
-------------'''),
    (u'05ANKARA7671', u'Nancy McEldowney', u''' 
Classified By: ADANA 222 
ADANA 216 
ADANA 207 
ANKARA 6772 
 
Classified by DCM Nancy McEldowney; reasons 1.4 b and d. 
 '''),
    (u'04HARARE766', u'ROBERT E. WHITEHEAD', u''' 
Classified By: DCM ROBERT E. WHITEHEAD DUE TO 1,4 (C) AND (D). 
 '''),
    (u'00TELAVIV4462', u'PSIMONS', u'''C O N F I D E N T I A L TEL AVIV 004462 
 
- - C O R R E C T E D  C O P Y - - CLASSIFIED BY LINE ADDED 
 
E.O. 12958: DECL: 08/24/05 
TAGS: KWBG, PTER, PGOV, PREL, IS 
SUBJECT: BIN LADIN CONNECTION IN GAZA FOUND PUZZLING; 
CONNECTION TO HAMAS QUESTIONED 
 
CLASSIFIED BY DCM PSIMONS PER 1.5 (B) AND (D) 
 
 '''),
)


_TEST_CABLES = (
    (u'10BANGKOK468', ()),
    (u'08STATE110079', ()),
    (u'05VILNIUS1093', u'Derrick Hogan'),
    (u'08STATE20184', ()),
    (u'08STATE20332', ()),
    (u'09ANKARA63', u'A.F. Godfrey'),
    (u'03COLOMBO1348', u'Alex Moore'),
    (u'03COLOMBO1810', u'Alex Moore'),
    (u'66BUENOSAIRES2481', ()),
    (u'05TAIPEI153', ()),
    (u'09TELAVIV2643', ()),
    (u'09BOGOTA2917',()),
    (u'07TOKYO5202', ()),
    (u'07USUNNEWYORK319', ()),
    (u'07VIENNA1239', ()),
    (u'09HONGKONG2247', ()),
    (u'07TOKYO3205', ()),
    (u'09HONGKONG2249', ()),
    (u'07BELGRADE533', u'Ian Campbell'),
    (u'05AMMAN646', ()),
    (u'08BAGHDAD1451', u'Jess Baily'),
    (u'08BAGHDAD1650', u'Jess Baily'),
    (u'98STATE145892', u'Jeff Millington'),
    (u'07TOKYO1414', ()),
    (u'06COPENHAGEN1020', u'Bill Mozdzierz'),
    (u'07ANKARA1581', u'Eric Green'),
    (u'08ANKARA266', u'Eric Green'),
    (u'08CHISINAU933', u'Daria Fane'),
    (u'10RIGA27', u'Brian Phipps'),
    (u'09WARSAW433', u'Jackson McDonald'),
    (u'09BAGHDAD2784', u'Anbar'),
    (u'05PARIS8353', u'Andrew, C. Koss'),
    (u'05ANKARA581', u'John Kunstadter'),
    (u'08RANGOON951', u'Drake Weisert'),
    (u'10BAGHDAD488', u'John Underriner'),
    (u'08STATE2004', u'Gordon Gray'),
    (u'10BAGHDAD370', ()),
    (u'09BEIJING951', u'Ben Moeling'),
    (u'09TOKYO1878', u'Ray Hotz'),
    (u'07OTTAWA100', u'Brian Mohler'),
    (u'07BAMAKO1322', ()),
    (u'09PRISTINA336', u'Michael J. Murphy'),
    (u'09PRISTINA345', u'Michael J. Murphy'),
    (u'06BAGHDAD4604', u'L. Hatton'),
    (u'05ROME178', (u'Castellano', u'Anna della Croce', u'Giovanni Brauzzi')),
    (u'08USNATO348', u'W.S. Reid III'),
    (u'09KHARTOUM107', u'Alberto M. Fernandez'),
    (u'09ABUDHABI901', u'Douglas Greene'),
    (u'03KUWAIT2352', u'Frank C. Urbancic'),
    (u'09BUENOSAIRES849', u'Tom Kelly'),
    (u'08BAGHDAD358', u'Todd Schwartz'),
    (u'09BAGHDAD419', u'Michael Dodman'),
    (u'10ADDISABABA186', ()),
    (u'10ADDISABABA195', ()),
    (u'10ASHGABAT178', u'Sylvia Reed Curran'),
    (u'09MEXICO2309', u'Charles Barclay'),
    (u'09MEXICO2339', u'Charles Barclay'),
    (u'05ATHENS1903', u'Charles Ries'),
    (u'02VATICAN25', u'Joseph Merante'),
    (u'07ATHENS2029', u'Robin'),
    (u'09HONGKONG934', ()),
    (u'03KATHMANDU1044', u'Robert Boggs'),
    (u'08CARACAS420', u'Robert Richard Downes'),
    (u'08DHAKA812', u'Geeta Pasi'),
    (u'09ULAANBAATAR87', ()),
    (u'96JEDDAH948', u'Douglas Neumann'),
    (u'09KABUL3161', u'Hoyt Yee'),
    (u'03OTTAWA202', u'Brian Flora'),
    (u'10GUATEMALA25', u'Drew G. Blakeney'),
    (u'07CARACAS2254', u'Robert Downes'),
    (u'09BUCHAREST115', u'Jeri Guthrie-Corn'),
    (u'09BUCHAREST166', u'Jeri Guthrie-Corn'),
    (u'06PANAMA2357', u'Luis Arreaga'),
    (u'09JAKARTA1580', u'Ted Osius'),
    (u'09JAKARTA1581', u'Ted Osius'),
    (u'07ATHENS2219', u'Thomas Countryman'),
    (u'09ANKARA1084', u"Daniel O'Grady"),
    (u'10ANKARA173', u"Daniel O'Grady"),
    (u'10ANKARA215', u"Daniel O'Grady"),
    (u'10ANKARA224', u"Daniel O'Grady"),
    (u'07BAGHDAD1513', u'Daniel V. Speckhard'),
    (u'08TASHKENT1089', u'Jeff Hartman'),
    (u'07HELSINKI636', u'Joy Shasteen'),
    (u'09STATE57323', u'James Townsend'),
    (u'09STATE59436', u'James Townsend'),
    (u'07TASHKENT2064', (u'Jeff Hartman', u'Steven Prohaska')),
    (u'07DUSHANBE337', u'David Froman'),
    (u'07DUSHANBE1589', u'David Froman'),
    (u'08SANJOSE762', u'David E. Henifin'),
    (u'05BAGHDAD3037', u'David M. Satterfield'),
    (u'04AMMAN4133', u'D.Hale'),
    (u'06YEREVAN237', u'A.F. Godfrey'),
    (u'07DHAKA909', u'Dcmccullough'),
    (u'07BAKU1017', u'Donald Lu'),
    (u'07USNATO92', u'Clarence Juhl'),
    (u'09KAMPALA272', u'Dcronin'),
    (u'06LAGOS12', u'Sam Gaye'),
    (u'07USNATO548', u'Clarence Juhl'),
    (u'07TOKYO436', u'Carol T. Reynolds'),
    (u'08STATE116100', u'Theresa L. Rusch'),
    (u'07NEWDELHI5334', u'Ted Osius'),
    (u'06BAGHDAD4350', u'Zalmay Khalilzad'),
    (u'07STATE141771', u'Scott Marciel'),
    (u'08STATE66299', u'David J. Kramer'),
    (u'09STATE29700', u'Karen Stewart'),
    (u'07NAIROBI4569', u'Jeffrey M. Roberts'),
    (u'02HARARE2628', u'Rewhitehead'),
    (u'04HARARE766', u'Robert E. Whitehead'),
    (u'04ANKARA7050', u'John Kunstadter'),
    (u'04ANKARA6368', u'Charles O. Blaha'),
    (u'09BAGHDAD280', ()),
    (u'05ABUJA1323', ()),
    (u'07MONROVIA1375', u'Donald E. Booth'),
    (u'03SANAA2434', u'Austin G. Gilreath'),
    (u'07BRUSSELS3482', u'Maria Metcalf'),
    (u'02KATHMANDU1201', u'Pete Fowler'),
    (u'09STATE2522', u'Donald A. Camp'),
    (u'09STATE100197', u'Roblake'),
    (u'08COLOMBO213', u'Robert O. Blake, Jr.'),
    (u'07MEXICO2653', u'Charles V. Barclay'),
    (u'09SOFIA89', u'Mceldowney'),
    (u'09ADDISABABA2168', u'Kirk McBride'),
    (u'06MINSK338', u'George Krol'),
    (u'10ADDISABABA195', ()),
    (u'04AMMAN9411', u'Christopher Henzel'),
    (u'06CAIRO4258', u'Catherine Hill-Herndon'),
    (u'08NAIROBI233', u'John M. Yates'),
    (u'06MADRID2993', ()),
    (u'08AMMAN1821', ()),
    (u'09KABUL1290', u'Patricia A. McNerney'),
    (u'06JEDDAH765', u'Tatiana C. Gfoeller'),
    (u'07BAGHDAD2045', u'Stephen Buckler'),
    (u'07BAGHDAD2499', u'Steven Buckler'),
    (u'04THEHAGUE1778', 'Liseli Mundie'),
    (u'04THEHAGUE2020', u'John Hucke'),
    (u'03HARARE1511', u'R.E. Whitehead'),
    (u'03BRUSSELS4518', u'Van Reidhead'),
    (u'02ROME4724', u'Douglas Feith'),
    (u'08BRUSSELS1149', u'Chris Davis'),
    (u'04BRUSSELS862', u'Frank Kerber'),
    (u'08BRUSSELS1245', u'Chris Davis'),
    (u'08BRUSSELS1458', u'Chris Davis'),
    (u'07ISLAMABAD2316', u'Peter Bodde'),
    (u'04MADRID764', u'Kathleen Fitzpatrick'),
    (u'06BELGRADE1092', u'Ian Campbell'),
    (u'07JERUSALEM1523', u'Jake Walles'),
    (u'09PANAMA518', u'Barbar J. Stephenson'),
    (u'06ABUDHABI409', u'Michelle J Sison'),
    (u'07DOHA594', ()),
    (u'07LAPAZ3136', u'Mike Hammer'),
    (u'08BOGOTA4462', u'John S. Creamer'),
    (u'09ATHENS1515', u'Deborah McCarthy'),
    (u'09LONDON2347', u'Robin Quinville'),
    (u'08LONDON821', u'Richard Mills, Jr.'),
    (u'06BUENOSAIRES497', u'Line Gutierrez'),
    (u'06BUENOSAIRES596', u'Line Gutierrez'),
    (u'06BUENOSAIRES1243', u'Line Gutierrez'),
    (u'05BAGHDAD3919', u'Robert Heine'),
    (u'06RIYADH8836', u'Mgfoeller'),
    (u'06BAGHDAD4422', u'Margaret Scobey'),
    (u'08STATE129873', u'David Welch'),
    (u'09BAGHDAD2299', u'Patricia Haslach'),
    (u'09BAGHDAD2256', u'Phaslach'),
    (u'09BAGHDAD2632', u'Phaslach'),
    (u'04BAGHDAD697', u'Matthew Goshko'),
    (u'05CAIRO8812', u'John Desrocher'),
    (u'06HONGKONG4299', ()),
    (u'06QUITO646', u'Vanessa Schulz'),
    (u'08RIYADH1616', u'Scott McGehee'),
    (u'08RIYADH1659', u'Scott McGehee'),
    (u'10BAGHDAD481', u'W.S. Reid'),
    (u'02KATHMANDU485', u'Pmahoney'),
    (u'09BAGHDAD990', u'Robert Ford'),
    (u'08BAGHDAD3023', u'Robert Ford'),
    (u'09USNATO530', u'Kelly Degnan'),
    (u'07LISBON2305', u'Lclifton'),
    (u'08BAGHDAD4004', u'John Fox'),
    (u'04THEHAGUE2346', u'A. Schofer'),
    (u'07TALLINN173', u'Jessica Adkins'),
    (u'09BAKU80', u'Rob Garverick'),
    (u'06PHNOMPENH1757', u'Jennifer Spande'),
    (u'06QUITO1401', u'Ned Kelly'),
    (u'05ZAGREB724', u'Justin Friedman'),
    (u'05TOKYO1351', u'David B. Shear'),
    (u'07KIGALI73', u'G Learned'),
    (u'08ZAGREB554', u"Peter D'Amico"),
    (u'07TASHKENT1950', (u'R. Fitzmaurice', u'T. Buckley')),
    (u'07TASHKENT1679', (u'Richard Fitzmaurice', u'Steven Prohaska')),
    (u'07TASHKENT1894', (u'Steven Prohaska', u'Richard Fitzmaurice')),
    (u'08STATE68478', u'Margaret McKelvey'),
    (u'04BRUSSELS416', u'Marc J. Meznar'),
    (u'07BAGHDAD777', u'Jim Soriano'),
    (u'05ALMATY3450', u'John Ordway'),
    (u'05ACCRA2548', u'Nate Bluhm'),
    (u'07ADDISABABA2523', u'Kent Healy'),
    (u'09USUNNEWYORK746', u'Bruce C. Rashkow'),
    (u'09STATE108370', u'Daniel Fried'),
    (u'09BAGHDAD3120', u'Mark Storella'),
    (u'09STATE64621', u'Richard C Holbrooke'),
    (u'05NAIROBI4757', u'Chris Padilla'),
    (u'05CAIRO5945', u'Stuart E. Jones'),
    (u'07BAGHDAD1544', u'Steven R. Buckler'),
    (u'07BAGHDAD1632', u'Steven R. Buckler'),
    (u'02HARARE555', u'Aaron Tarver'),
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


def test_cable_classificationist():
    def check(cable_id, expected, normalize):
        if not isinstance(expected, tuple):
            expected = (expected,)
        cable = cable_by_id(cable_id)
        ok_(cable, 'Cable "%s" not found' % cable_id)
        eq_(expected, tuple(cable.classificationists))
    for testcase in _TEST_CABLES:
        if len(testcase) == 2:
            cable_id, expected = testcase
            normalize = False
        else:
            cable_id, expected, normalize = testcase
        yield check, cable_id, expected, normalize


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

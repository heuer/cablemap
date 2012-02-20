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
Tests cablemap.core.reader.parse_signers.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id
from cablemap.core.reader import parse_signers

_TEST_DATA = (
    # 7575LIBREVILLE1895
    (u'STEIGMAN', u'''4. AMBASSADOR KIM WILL ATTEMPT CALL PARK IN NEW YORK
AT OPENING OF BUSINESS TO CONFIRM RECEIPT OF INSTRUCTIONS,
AND HAS EXTRACTED PROMISE FROM REKANGALT TO
PHONE ESSONGHE DIRECTLY THIS AFTERNOON IF HE STILL
APPEARS TO BE WAVERING.
STEIGMAN
CONFIDENTIAL
''', False),
    # 78TEHRAN389
    (u'SULLIVAN', u'''SHAH AND/OR USG. BY THE SAME TOKEN, IT IS POSSIBLE TO
CONCLUDE THAT RELATIVE POLICE LENIENCY, AS FOR EXAMPLE IN
LACK OF EFFECTIVE REACTION TO STUDENT DEMONSTRATION JAN 7,
ENCOURAGED MORE VIOLENT DEMONSTRATION WHICH NECESSITATED
VIOLENT REPRESSION TO PUT DOWN. AT LEAST IT IS CONCEIVABLE
THAT THE MANY PROPONENTS OF THE MAILED FIST IN GOI
ESTABLISHMENT MIGHT SO ARGUE TO THE SHAH AND PRIMIN
AMOUZEGAR IN EFFORT TO REVERSE RELATIVE LIBERALIZATION OF
RECENT MONTHS.

SULLIVAN

CONFIDENTIAL

Declassified/Released US Department of State EO Systematic
Review 30 JUN 2006
''', False),
    # 79TEHRAN8980
    (u'LAINGEN', u'''- --FINALLY, ONE SHOULD BE PREPARED FOR THE THREAT
OF BREAKDOWN IN NEGOTIATIONS AT ANY GIVEN MOMENT AND NOT
BE COWED BY THE POSSIBLITY. GIVEN THE PERSIAN
NEGOTIATOR\'S CULTURAL AND PSYCHOLOGICAL LIMITATIONS, HE
IS GOING TO RESIST THE VERY CONCEPT OF A RATIONAL
(FROM THE WESTERN POINT OF VIEW) NEGOTIATING PROCESS.


LAINGEN

CONFIDENTIAL
'''),
    # 79ANKARA6618
    (u'SPIERS', u'''4. THE POSSIBILITY OF ARMED ACTION NEAR THE IRAQI BORDER ALSO RAISED THE QUESTION OF IRAQI RESPONSE.  SO FAR THE GOT WAS UNCLEAR WHAT GAME IRAQ WAS PLAYING VIS-A-VIS IRAN.  ON THE ONE HAND INSTABILITY IN THE REGION WAS AS UNHELPFUL TO IRAQ AS IT WAS TO ANYONE ELSE.  ON THE OTHER HAND, THERE WERE SUFFICIENT POINTS OF FRICTION BETWEEN A REVOLUTIONARY IRAN AND IRAQ THAT THE LATTER MIGHT WELL WISH TO STRENGTHEN ANTI-KHOMEINI FORCES.

5. REGARDING TIES BETWEEN IRANIAN KURDS AND OUTSIDE COUNTRIES, KOKSAL SAID THAT THERE WERE MANY REPORTS, BUT NOT MUCH HARD EVIDENCE, OF FOREIGN INVOLVEMENT WITH THE IRANIAN KURDS.  HE ASSUMED THAT OUTSIDE POWERS NOTWITHSTANDING PREDICTABLE DENIALS WOULD FEEL STRONG URGE TO INVOLVE THEMSELVES IN KURDISH ACTIVITIES.  REGARDING LINKS BETWEEN TURKISH AND IRANIAN KURDS, KOKSAL EMPHASIZED THAT RECENT PRESS REPORTS THAT TURKISH KURDS WERE PROVIDING LARGE-SCALE ASSISTANCE WERE TOTAL JOURNALISTIC FABRICATIONS.  TO DATE, GOT DID NOT HAVE IMPRESSION THAT THERE WAS ANY SUBSTANTIAL LINKAGE ALTHOUGH, OBVIOUSLY, WHAT HAPPENED WITH THE KURDS IN IRAN WOULD HAVE A GREAT IMPACT ON ATTITUDES OF TURKISH KURDS.

6. BECAUSE OF THIS, AS WELL AS IN THE INTEREST OF REGIONAL STABILITY, TURKEY\'S OVERRIDING CONCERN WAS THAT IRAN MAINTAIN ITS TERRITORIAL INTEGRITY AND HAVE A STRONG AND EFFECTIVE CENTRAL GOVERNMENT.  FOR THIS REASON THE GOT HAD NOTED WITH INTEREST AND APPROVAL CHARGE LAINGEN\'S RECENT STATEMENT AFFIRMING US SUPPORT FOR IRAN\'S TERRITORIAL INTEGRITY.

7. COMMENT: WHILE NEW TO THE JOB, KOKSAL, FORMERLY WITH THE POLICY PLANNING STAF, WAS SUBSTANTIALLY MORE OPEN THAN HIS PREDECESSORS IN DISCUSSING KURDISH QUESTION.

SPIERS
'''),
    # 79TEHRAN12130
    (u'LAINGEN', u'''1. (C - ENTIRE TEXT).

2. AT DINNER RECENTLY SOVIET AMBASSADOR VINOGRADOV SPOKE CANDIDLY OF PGOI. HE HAS SEEN VIRTUALLY ALL KEY LEADERS. AS AMIR-ENTEZAM OBSERVED, \"IF YOU CLOSE ONE DOOR, HE COMES IN THE OTHER WITH A PROPOSAL OR SOME DEAL.\"

3. VINOGRADOV HAS SEEN KHOMEINI FOUR TIMES. HE DESCRIBED THE AYATOLLAH AS A MAN OF GREAT RECTITUDE, A TEACHER DISINCLINED TO LISTEN AND LITTLE VERSED IN POLITICAL REALITIES DOMESTICALLY OR INTERNATIONALLY.  TALAGHANI, THE AMBASSADOR SAID, WAS MUCH MORE THE REALIST. VINOGRADOV THOUGHT SKHESHTI WAS THE MOST INTELLIGENT AND POLITICALLY SKILLFUL OF THE RELIGIOUS LEADERSHIP. BANI SADR MERITED ONLY SCORN.

4. THE SOVIETS THINK THE PGOI\'S MOST DANGEROUS PROBLEM IS THE KURDISH REVOLT, FOLLOWED CLOSELY BY THE STAGNATED ECONOMY. VINOGRADOV FEELS THE IRANIANS ARE TRYING TO MANAGE THE KURDS WITH FORCE AND THE ECONOMY WITH DREAMY ISLAMIC THEORIES.  NEITHER WILL WORK.  ALTHOUGH THE KURDISH PROBLEM MAY EVENTUALLY BE SETTLED, THERE WAS A REAL PROSPECT OF SHORTAGES, UNEMPLOYMENT AND OTHER SERIOUS ECONOMIC GRIEVANCES LEADING TO DISAFFECTION OF THE LOWER CLASSES FROM KHOMEINI.  IT HAS ALREADY STARTED, BUT THE PROCESS COULD CONTINUE FOR A COUPLE YEARS.  HE SUSPECTED THE IRAQIS MIGHT BE INVOLVED IN CAUSING PROBLEMS WITH IRAN\'S KURDS AND ARABS, BUT DISMISSED THE THOUGHT THAT THESE USSR MIGHT HAVE INFLUENCE IN BAGHDAD TO RESTRAIN THE IRAQIS.  \"THEY ARE JUST CRAZY PEOPLE.\"

LAINGEN
''', False),
    (u'CLARK', u'''AN OVERALL ANTARCTIC QUOTA FOR GOJ OF
1,924 (OR 1,941) OR WHETHER THE QUOTA FOR EACH
AREA WOULD BE EXAMINED IN ANY USG EVALUATION OF
WHETHER MINKE CATCH LIMITS ARE BEING EXCEEDED THIS
SEASON.
-
5.  (U) REGARDING REFTEL\'S PARA 5, AKIYAMA
CONFIRMED THAT 106 SPERM WHALES, ALL MALES,
HAD BEEN HARVESTED BY THE JAPANESE COASTAL
WHALING FLEET THROUGH JANUARY 7.
-
CLARK
''', False),
    (u'BARTHOLOMEW', u'''INEVITABLY ACCUSED ISRAEL OF BEING BEHIND BLASTS,
WHILE THE SYRIAN BA\'ATH PARTY HAS SINGLED OUT
PRO-ARAFAT PALESTINIANS.  JOURNALISTS RESIDENT IN
THE WEST VARIOUSLY ATTRIBUTE THE BLASTS TO THE MUR-
ABITUN, WHICH THEY SAY IS RETURNING TO THE AREA IN
FORCE AND REINVIGORATING THE OLD MURABITUN-PSP FEUD,
OR HIZBALLAH,SIGNS OF WHOSE PRESENCE THEY SAY ARE
INCREASINGLY DAILY.  IN THIS REGARD, U.S. JOURNALISTS
DESCRIBED THE QUALITY OF LIFE IN WEST BEIRUT AS
HAVING SUNK TO TRULY HOBBESIAN LEVELS OF NASTINESS
IN LAST MONTH, WITH THE COMBINATION OF CAR BOMBS
AND ARMED ROBBERIES KEEPING MQST PEOPLE LOCKED
INDOORS AT NIGHT.  THERE ARE PRESENTLY REPRESENTA-
TIVES OF ONLY THREE AMERICAN NEWS MEDIA RESIDENT
IN BEIRUT (ASSOCIATED PRESS, LOS ANGELES TIMES,
AND NEW YORK TIMES); SOME OF THESE ARE THINKING ABOUT
LEAVING.


BARTHOLOMEW
''', False),
    (u'MAINO', u'''SEDETLY ABOUT TWO WEEKS AGO IN A GABORONE MOTEL WITH BOPHUTHATSWANA
OFFICIALS. THE GUARDIAN SAID THAT DR. CHIEPE HAS \"EMPHATICALLY DENIED
ANY KNOWLEDGE OF SUCH A MEETING. THE GUARDIAN CONTINUED THAT
INFORMED SOURCES HAVE INDICATED THAT THE BANTUSTAN GOVERMMENT SEEKS
ASSURANCE FROM GABORONE THAT ANC FREEDOM FIGHTERS ARE NOT OPERATING
FROM BOTSWANA.\" THE PRESS RELEASE ALSO FOLLOWS A SIRO REPORT OF AN
ARMED CLASH FEBRUARY 3 ON THE FRONTIER TWO KILOMETERS NORTH OF THE
TLOKWENG BORDER POST BETWEEN 3 ARMED ANC CADRE AND A SOUTH AFRICAN
DEFENSE FORCE PATROL IN WHICH ONE SOUTH AFRICAN SOLDIER WAS SAID TO
HAVE BEEN CRITICALLY WOUNDED. THE ANC GROUP REPORTEDLY FLED BACK INTO
BOTSWANA. END COMMENT.


MAINO
''', False),
    (u'EAGLETON', u'''19.  BUT HIS NEED FOR THIS \"PARDON\" AT THIS TIME GOES
DEEPER.  HAMA CONTINUES AS A VERY PRESENT, VERY
HORRIBLE NATIONAL MEMORY.  NOTHING LIKE HAMA HAD EVER
OCCURRED IN LIVING MEMORY.  (JAMAL PASHA\'S HUPPRESSION
OF CHRISTIAN MINORITIES INVOLVED TURKISH BUTCHERY
OF CHRISTIANS, MOSTLY ARMENIANS AND MARONITES--THUS
THIS IS NOT A MEMORY OF SYRIANS BUTCHERING FELLOW
SYRIANS.)  WE BELIEVE THAT ASAD SOUGHT TO GO INTO HIS
THIRD TERM \"CLEANSED,\" WITH THE HORROR OF HAMA PUT
BEHIND HIM.  AT THE SAME TIME, THE MEMORY OF HAMA HAS
ITS UTILITY, IN REMINDING THE PEOPLE THAT ASAD IS
WILLING TO BE UNIMAGINABLY TOUGH WHEN HE HAS TO BE.
THUS, HE GAVE DOUBLE, APPARENTLY CONTRADICTORY
MESSAGES--THE \"PARDON,\" AND THE EIGHTH CONGRESS FINAL
DECLARATION ON THE SAME DAY STRESSING CONTINUED TOUGH-
NESS.  INDEED, THE \"PARDON\" IS ALSO QUITE TOUGH IN
ITS CONDEMNATION OF THOSE \"TRADING IN THE NAME OF
RELIGION\" AND \"DISTORTING  THE NOBLE RELIGION.\"
ASAD SEEKS TO GIVE AN IMAGE OF BEING \"BENEVOLENT,\"
\"TOUGH,\" AND THE \"UPHOLDER OF RELIGION\" (THOUGH ALAWI)
ALL AT THE SAME TIME.

-
20.  NOTE:  POST WOULD WELCOME CRITICISMS AND
CONTRIBUTIONS TO THIS STUDY FROM DEPARTMENT, CIA, AND
DIA, AND EMBASSIES BAGHDAD, AMMAN, AND RIYADH.  OUR
OWN HISTORICAL SOURCES ARE EXTREMELY LIMITED.

21.  BEIRUT MINIMIZE CONSIDERED.  EAGLETON
''', False),
    (u'KING', u'''11.  THE CONCLUSION IS THAT, FOR WHATEVER REASON, THE ROYAL
FAMILY DOMINATES THE MALAY BUSINESS COMMUNITY TO AN EXTENT THAT
PROBABLY IS CAUSING GREATER DISSATISFACTION THAN THE EXTENT TO
WHICH THEY DOMINATE THE NATION\'S POLITICS.  MOTIVES MAY BE
TRADITIONAL BUSINESS REASONS, AND THE ECONOMIC DOMINANCE
INADVERTENT, MERELY THE NATURAL RESULT OF BETTER FINANCING AND
GOOD CONNECTIONS, BUT THE RESENTMENT BEARS WATCHING.  OFFICIALS
OF THE TWO BIG COMPANIES THEMSELVES ARE AWARE OF IT, BUT THE
EXTENT TO WHICH THE ROYAL FAMILY BELIEVES IT SOMETHING TO
BE CONCERNED ABOUT IS UNKNOWN.  PRINCE SUFRI\'S BUSINESS
PROSPECTS MAY BE BOTH DEPENDENT ON AND AN INDICATION OF THE
EXISTENCE OF SUCH CONCERN.


KING
''', False),
    (u'VERSHBOW', u'''21.  (C) What all this means is that your meeting with FM Yu
may fall short on specifics, especially on politically
sensitive issues such as beef.  Still, this is a very
different Administration than the one we have had to deal
with under Roh Moo-hyun.  On Monday, MOFAT let us know that
Korea was ready to recognize Kosovo; a few weeks ago, the
ROKG UN delegation heavily criticized the North on human
rights; in the near future, we expect the Koreans will sign
on to PSI.  All of this could not have taken place with Roh
in the Blue House.  We all remain hopeful that Lee can
stabilize his political base and that we can make more
significant progress soon.
VERSHBOW
''', False),
    (u'STRAUSZ-HUPE', u'''7. COMMENT:  THE TURKS HAVE AN INTEREST IN AVOIDING
AN ALARMING VIEW OF RECENT DEVELOPMENTS IN THE WAR
WHICH MIGHT PREJUDICE THEIR CURRENT NEGOTIATIONS WITH
IRAQ OVER CREDIT TERMS.  AT THE SAME TIME THE GOT
WANTS TO AVOID INDICATIONS THAT THEIR SUBSTANTIAL
STAKES IN IRAQ--INCLUDING THE PIPELINE AND OVER A
BILLION DOLLARS IN OUTSTANDING DEBT--MIGHT BE IN
JEOPARDY.

STRAUSZ-HUPE
''', False),
    (u'RICKERT', u'''5.  BIO NOTE:  BURCUOGLU APPEARS TO BE IN HIS FORTIES
AND SPEAKS GOOD, ALTHOUGH OCCASIONALLY LABORED, ENGLISH.
HE MENTIONED THAT, DURING A PREVIOUS TOUR OF DUTY IN
CONFIDENTIAL

SIPDIS

CONFIDENTIAL

SIPDIS

PAGE 03        SOFIA  03382  111320Z

IRAN, HE WAS SENT BY HIS AMBASSADOR (\"BECAUSE I SPOKE
SOME FARSI AND AZERI TURKISH\") ONTO THE GROUNDS OF THE
US EMBASSY IN TEHRAN IMMEDIATELY AFTER THE 1979
HOSTAGE SEIZURE.  BECAUSE HE WAS SHOUTING \"DEATH TO
AMERICA\" AND \"ALLAHU AKBAR,\"  HE WAS ADMITTED TO THE
EMBASSY GROUNDS AND WAS NOT HINDERED IN HIS OBSERVATIONS.
RICKERT


CONFIDENTIAL

SIPDIS
''', False),
    (u'BARTHOLOMEW', u'''STORE VARIETY.  THE SITUATION APPROACHES NORMAL IN
EASTERN AREAS FURTHER FROM THE GREEN LINE.  ALL GREEN
LINE CROSSINGS ARE OFFICIALLY CLOSED.

6.  COMMENT.  IT IS STILL TOO SOON TO TELL IF RECENT
OUTBREAKS REPRESENT SPONTANEOUS OUTBURSTS OR ARE
POLITICALLY MOTIVATED.  WE EXPECT THE SHARP FIGHTING
ALONG THE GREEN LINE TO CONTINUE.  HOWEVER, DESPITE
UNSUBSTANTIATED RUMORS OF TROOP MOVEMENTS AND FEARS OF
IMPENDING CLASHES, SUQ AL-GHARB HAS REMAINED CURIOUSLY
QUIET.  END COMMENT.

BARTHOLOMEW

NOTE BY OC/T:  HEADING AS RECEIVED.  CORRECTION TO FOLLOW.
''', False),
    (u'GILLESPIE', u'''3. (C) COMMENT: THIS INCIDENT ILLUSTRATES THE
AMBIGUITIES OF THE COLOMBIAN PEACE PROCESS WHICH FAVOR
SUCH ACTIONS BY THE FARC.  THE FARC CAN EITHER ATTRIBUTE
THE EXTORTION TO ANOTHER GUERRILLA GROUP OR ALLEGEDLY
DISCIPLINE ITS DISOBEDIENT UNIT.  IN EITHER
CIRCUMSTANCE, THE FARC CAN BOLSTER ITS IMAGE, AND THAT
OF THE UP, AS FAITHFUL ADHERENTS TO THE PEACE PROCESS.
AS IN ITS UPCOMING DEALINGS WITH THE PEACE COMMISSION
(SEE REFTEL), THE FARC CAN CULTIVATE SUCH A POSITIVE
IMAGE WHILE PROCEEDING WITH BUSINESS AS USUAL.

GILLESPIE##
''', False),
    (u'HORAN', u'''1974  SPAIN
1975  UNITED KINGDOM
1975  UNITED STATES
1984  UNITED KINGDOM
1984  SPAIN
1985  FRANCE
1985  AUSTRIA


HOBBIES:

READING AND HORSEMANSHIP, IN THE ARAB TRADITION.  THE
CROWN PRINCE IS PRESIDENT OF THE SAUDI EQUESTRIAN CLUB
IN RIYADH.


END TEXT.


HORAN##
''', False),
    (u'MCNAMARA', u'''OFFICIALS; IMMEDIATE DETENTION OF PERSONS SUSPECTED OF
CONSPIRING AGAINST PUBLIC ORDER; AN INCREASE IN MILITARY
AND POLICE RECRUITMENT AND THE CREATION OF SPECIAL
GROUPS TO COMBAT TERRORISM; ADDITIONAL MATERIALS
RESOURCES FOR THE ARMED FORCES TO IMPROVE MOBILITY; THE
SPECIAL PROTECTION OF JUDGES AND MAGISTRATES
INVESTIGATING MASSACRES OR ATTACKS AND THE ELIMINATION
OF TRIAL BY JURY IN CASES OF \"MONSTROUS CRIMES\".  THESE
DECREES ARE, HOWEVER, SUBJECT TO AUTOMATIC SUPREME COURT
REVIEW, AND SEVERAL, PARTICULARLY THE MANDATORY LIFE
SENTENCE, ARREST ON SUSPICION OF CONSPIRACY AND THE
ELIMINATION OF JURY TRIAL FOR SOME MURDER TRIALS, ARE
APT TO BE OVERTURNED.

MCNAMARA.
''',
        False),
    (u'BAKER', u'''                    JANUARY BY THE 1ST OF MAY GROUP,
                    WHICH MAY BE LINKED TO 17
                    NOVEMBER.)

     FEBRUARY 22    THREE UNOCCUPIED RESIDENCES WERE
                    BOMBED TO CALL ATTENTION TO HIGH
                    HOUSING COSTS.

     MAY 8          FORMER MINISTER OF PUBLIC ORDER
                    GEORGE PETSOS, ALONG WITH TWO
                    BODY GUARDS, WERE INJURED IN A
                    REMOTE-DETONATED CAR BOMB
                    EXPLOSION.

                     //END//

       THE OFFICE OF THE COORDINATOR FOR
     COUNTER-TERRORISM APPRECIATES THE ASSISTANCE OF
     THE THREAT ANALYSIS DIVISION OF THE BUREAU OF
     DIPLOMATIC SECURITY WHICH COMPILED THIS
     REPORT.  END OF TEXT. BAKER


UNCLASSIFIED
''', False),
    (u'SACCIO', u'''FISHING; (E) ELIMINATE LAST THREE PARS OF AIDE-MEMOIRE HANDED
TO CANADIAN AMB.

8.  IF AUTHORIZED, ENVISAGE TWO-STEP APPROACH TO FONOFF.
FIRST, INFORMAL AND ORAL, STRESSING OUR INTEREST IN FREEDOM OF
HIGH SEAS, NOTING EARLIER FONOFF CONFIRMATION NEW LAW UNDER
STUDY, OUTLINING OUR PROPOSAL IN GENERAL TERMS.  ON BASIS
FONOFF REACTION, WE WOULD THEN COUCH AIDE-MEMOIRE IN TERMS
WHICH WOULD APPEAR MOST LIKELY TO SUCCEED.

GP-3
SACCIO
''', False),
    (u'EINIK', u'''
PAGE 03        ZAGREB  01569  04 OF 04  071629Z

16.  THE CROATIAN ARMY IS LEADING AND WILL LEAD THE
LIBERATION WAR FOR EVERY INCH OF ITS HOMELAND
ACCORDING TO INTERNATIONAL CONVENTIONS.  BY THE DIRTY
WAR WHICH WAS IMPOSED UPON US NOT ONLY FROM THE
GRUBISNO POLJE REGION, BUT FROM THE WHOLE CROATIAN
TERRITORY, ALL WILL DISAPPEAR WHO REACHED OUT FOR
CROATIAN TERRITORY AND ALSO THOSE WHO VIOLATED THE
CROATIAN STATE.  THERE WILL BE NO MERCY IN THE NAME
OF ALL INNOCENT VICTIMS FROM VUKOVAR TO DUBROVNIK.
ALL LOYAL CITIZENS OF THE CROATIAN REPUBLIC HAVE NO
REASON FOR FEAR.  CROATIAN SOLDIERS ARE DEFENDING
UNCLASSIFIED

SIPDIS

WITH THE INTERNATIONAL RULES OF MILITARY BEHAVIOR IN
DISTINCTION FROM THOSE WHO DID NOT

WP
UNCLASSIFIED

SIPDIS

SUCCEED TO LEARN IT DURING MILITARY SCHOOLING.  (NO
WONDER THAT THERE ARE SO MANY CRIMES|)

17.  CROATIAN ARMY WILL WIN, FIGHTING TO THE LAST
DROP OF BLOOD IF THIS IS NECESSARY FOR ITS HOMELAND,
BUT THE FLAME WHICH BURNS ON THE GROUND OF THE
FORMER YUGOSLAVIA IS THREATENING WITH INCREASED
PROPORTIONS.  IT IS THE VERY LAST MOMENT THAT THE
WORLD, WHICH SEES AND UNDERSTANDS ALL, VERY WELL,
UNDERTAKES SOMETHING.  END TEXT.
EINIK
                       UNCLASSIFIED


                       UNCLASSIFIED

PAGE 04        ZAGREB  01569  04 OF 04  071629Z



                       UNCLASSIFIED









NNNN
'''),
    # 85BAGHDAD3988
    (u'NEWTON', u'''11. FINALLY, FEARS THAT THE SOVIETS WILL MAKE INROADS INTO IRAN
WOULD SEEM GROSSLY EXAGGERATED. THE SOVIET UNION, NOT THE U.S.,
IS IRAQ\'S PRINCIPAL ARMS SUPPLIER; THE ENEMY OF THE MUJAHIDIN
IN AFGHANISTAN; THE BACKER OF THE TUDEH PARTY; AND THE RULERS
OF 40 MILLION MUSLIMS INSIDE ITS OWN BORDERS. THE SOVIETS HAVE
HARDLY RESPONDED POSITIVELY TO RECENT IRANIAN OVERTURES LARGELY
BECAUSE THE IDEOLOGY OF IRAN\'S RULING CLERICS PREVENTS THEM FROM
MAKING THE SOVIETS A SUFFICIENTLY ATTRACTIVE OFFER TO SWITCH
SIDES.-/


NEWTON
'''),
    # 86STATE29781
    (u'SHULTZ', u'''IN HIS WRITINGS, MUSEVENI HAS FAVORED ACTIVE STATE
GUIDANCE OVER THE ECONOMY.  BUT HE HAS ALSO RECOGNIZED
THAT FREE ENTERPRISE BASED ON SMALLHOLDER AGRICULTURE
IS THE KEY TO UGANDA\'S ECONOMIC DEVELOPMENT.  MUSEVENI
SAID HIS GOVERNMENT WILL WELCOME FOREIGN ASSISTANCE IN
DEVELOPING PRODUCTIVE ENTERPRISES.  OUR AMBASSADOR IS
ANXIOUS TO RESUME THE AID PROGRAM AND ENGAGE MUSEVENI
IN DIALOGUE ON UGANDA\'S ECONOMIC AND POLITICAL
EVOLUTION. END TEXT.

4.  KAMPALA MINIMIZE CONSIDERED.
UNQUOTE

SHULTZ
'''),
    # 86ALEXANDRIA1240
    (u'HAMBLEY', u'''HAS TAKEN ITS TOLL IN THIS REGARD.  ON THE OTHER HAND,
HE IS PLEASANT, NOT PUSHY, AND HAS GONE OUT OF HIS
WAY TO UNDERSTAND EGYPTIAN VIEWPOINTS AND PUT DOMESTIC
EVENTS IN EGYPT INTO A BROADER CONTEXT.  IT IS
APPARENT THAT HE IS NEITHER HELPED NOR ENCOURAGED BY
HIS EMBASSY IN CAIRO IN HIS VARIOUS UNDERTAKINGS.
HE CONSULTS REGULARLY, BUT DOES NOT SEEM TO BE KEPT
IN THE INFORMATION LOOP.  WITHOUT HIS AMBASSADOR\'S
FULL UNDERSTANDING AND SUPPORT, IT IS HARD TO IMAGINE
HOW HE CAN BE EXPECTED TO DO MUCH BETTER AS A
WELL-INFORMED AND EFFECTIVE PROPONENT OF IMPROVED
EGYPTIAN-ISRAELI TIES.  TUVAL IS ASSISTED IN HIS


HAMBLEY
'''),
    # 00THEHAGUE1810
    (u'SCHNEIDER', u'''DRAFT.


¶2.  VON DER ASSEN SAID HE WANTS TO WORK CLOSELY WITH THE US
DELEGATION DURING THE MEETING OF THE CORE GROUP OF LIKE-
MINDED COUNTRIES IN AUCKLAND EARLY NEXT WEEK, AND THE IWC
ANNUAL MEETING IN ADELAIDE, JULY 3-6.


¶4.  PLEASE NOTE A CHANGE IN VON DER ASSEN'S PHONE NUMBER.
IT NOW IS 31-70-378 4921.
SCHNEIDER'''),
    # 04CARACAS1540
    (u'SHAPIRO', u'''through political propaganda or through its number of social
projects to convert the poor and middle classes to his
revolution.  Though some of the GOV's propaganda promotes the
image of a beautiful and peaceful revolution, other messages
are foul-mouthed and aggressive.  And, while some of his
social programs appear to have drawn support from segments of
the lower social strata, and some hit a responsive
anti-American cord among traditional leftists, some (not all)
of this support will last only as long as the cash flows.
(Drafted: PAS: Victoria Alvarado.)
SHAPIRO


NNNN

      2004CARACA01540 - UNCLASSIFIED'''),
    # 00HANOI2480
    (u'PETERSON', u'''CONTINUE TO LOOM LARGE -- AS COMPETITOR BUT ALSO AS
MODEL.  IN ONE SENSE, HANOI HAS LITTLE CHOICE.  SINCE
THE FALL OF THE SOVIET UNION, THE BOAT THAT THE
WORLD'S FIVE REMAINING COMMUNIST COUNTRIES FIND
THEMSELVES IN HAS GOTTEN SMALLER AND MORE RICKETY.

WHETHER OUT OF DESPERATION OR INSPIRATION, VIETNAM
FINDS LITTLE RECOURSE BUT TO LOOK TO CHINA -- THE
LARGEST, MOST IMPORTANT AND MOST PROSPEROUS OF THE
FIVE -- FOR IDEAS ON ECONOMIC AND POLITICAL REFORM.
END COMMENT.
PETERSON

NOTE: NOT PASSED TO ABOVE ADDRESSEE(S)

                       CONFIDENTIAL'''),
    # 00HANOI2605
    (u'PETERSON', u'''THE U.S. GOVERNMENT CONDEMNS THE RECENT ACTIONS IN SOUTHEAST
ASIA BY INDIVIDUAL U.S. CITIZENS AND RESIDENTS WHO HAVE
VIOLATED THE LAW BY COMMITTING TERRORIST ACTS AGAINST
EXISTING GOVERNMENTS IN THAT AREA.  THESE ACTS VIOLATE
INTERNATIONAL NORMS OF BEHAVIOR AND ENDANGER LIVES AND
SHOULD BE PUNISHED UNDER INTERNATIONAL AND LOCAL LAWS.
(U. S. LAW ENFORCEMENT AGENCIES HAVE BEEN ALERTED TO
INVESTIGATE WHETHER ANY U.S. LAWS WERE VIOLATED LEADING UP
TO OR IN THE CARRYING OUT OF THESE ILLEGAL ACTIVITIES.)  END
                       UNCLASSIFIED

PAGE 04        HANOI  02605  300858Z
TEXT.

PETERSON

                       UNCLASSIFIED'''),
    # 07LAGOS97
    (u'BROWNE', u'''¶20.  (U)  The new fiscal regime is intended to be
automatically responsive to varying project costs and price

LAGOS 00000097  005.2 OF 005


conditions; progressive so that the government take increases
proportionately with project profitability; and simple, so as
to avoid multiple taxes and complex allowances that either
create loopholes or provide too much incentive.  The regime
is focused on profit, not revenue or costs.

¶21.  (U)  Kupolokun also said that a gas development
agreement for Production Sharing Contracts will be drafted.
Because the PSCs are for oil exploration and development, gas
discoveries are incidental to oil operations.  A separate
agreement is being developed to establish terms for the
commercial development of the gas, taking into account that
exploration costs are recovered from oil revenue, and
unsuccessful oil exploration is considered a sunk cost.  The
NNPC retains ownership of PSC gas.
BROWNE'''),
    # 08KINSHASA329
    ((), u'''
KINSHASA 00000329  008 OF 008


¶56. (U) At a meeting in Matadi, the GDRC decided that at the end of
the month they will auction containers that are piling up at
ONATRA's port.  This should ease congestion and allow normal
operations to resume.

Monthly Inflation and Exchange Rates
------------------------------------

¶57. (U) The monthly inflation rate for March was 5.6 percent. The'''),
    # 01HANOI3209
    (u'PORTER', u'''5.  (U)  COMMENT:  WHILE THIS FOREIGN MINISTERIAL VISIT
FOLLOWED LARGELY PREDICTABLE LINES, THE DISCUSSIONS RELATED
TO COMBATING TERRORISM ARE SIGNIFICANT.  CONSIDERATION BY
ASEAN, OR AT LEAST SEVERAL ASEAN MEMBERS, OF INTELLIGENCE
SHARING IN THE GLOBAL WAR AGAINST TERRORISM SHOULD BE VIEWED
IN A POSITIVE LIGHT, AND FOLLOWS ON THE HEELS OF THE STRONG
STATEMENTS AGAINST TERRORISM AT THE ASEAN SUMMIT IN BRUNEI
AND THE RECENT MANILA MEETING OF ASEAN DEFENSE CHIEFS.
PLANNED MEETINGS IN EARLY 2002 OF THE ASEAN FOREIGN AND
DEFENSE MINISTERS ARE LIKELY FURTHER TO DISCUSS SUCH
EXPANDED ANTI-TERRORISM COOPERATION.
PORTER

                       UNCLASSIFIED'''),
    # 88DHAKA2166
    (u'DE PREE', u'''INTERNATIONAL FORA, BANGLADESH HAS CONDEMNED AS CRIMINAL
ALL ACTS, METHODS, AND PRACTICES OF TERRORISM WHEREVER
AND BY WHOMEVER COMMITTED.  TO POST'S KNOWLEDGE, THE
BDG HAS ENDORSED INTERNATIONAL ANTI-TERRORISM
CONVENTIONS.  BANGLADESH HAS SUPPORTED EFFORTS WITHIN
THE SOUTH ASIAN ASSOCIATION FOR REGIONAL COOPERATION
(SAARC) TO ADDRESS THE PROBLEM OF INTERNATIONAL
TERRORISM.  BANGLADESH'S UNGA VOTING RECORD ON TERRORISM
IS UNAVAILABLE AT POST.


DE PREE
'''),
    # 88STATE271057
    (u'WHITEHEAD', u'''(END TALKING POINTS)

¶4.  FYI ONLY:  THE SIZE AND STRUCTURE OF OUR AUGMENTED
NAVAL FORCES WILL REMAIN COMMENSURATE WITH THE THREAT.
AS THAT THREAT DIMINISHES, WE WILL REDUCE THE FORCE AS
APPROPRIATE.  THE DEPARTMENT WILL CONTINUE TO ADVISE WHEN
FORCE LEVEL CHANGES ARE ANTICIPATED IN ORDER TO ALLOW THE
EMBASSIES TO CONSULT WITH THE STATES OF THE REGION AND
OUR ALLIES.  END FYI. YYY


WHITEHEAD'''),
    # 88BEIJING25961
    (u'LORD', u'''IN HIS SPARE TIME) AS THE AIR MONGOLIA REPRESENTATIVE
IN BEIJING, BUT WAS NOT AVAILABLE FOR COMMENT ON THE
AIR SERVICE. THE MONGOLIAN DIPLOMAT SAID THAT HE WAS
NOT FAMILIAR WITH THE EXISTENCE OF A CIVIL AIR TREATY
BETWEEN MONGOLIA AND THE PRC, BUT WOULD BE HAPPY TO
INVESTIGATE AND ADVISE FURTHER. HE FINALLY REFERRED
ALL OF ECONOFF'S QUESTIONS CONCERNING THE AIR SERVICE
TO THE MAIN OFFICE OF THE CIVIL AVIATION
ADMINISTRATION OF CHINA (CAAC) WHICH SERVES AS AIR
MONGOLIA'S AGENT IN CHINA.

LORD
LIMITED OFFICIAL USE
NNNN'''),
    # 89BANGKOK3838
    (u"O'DONOHUE", u'''OPEN ENDED
----------

¶15.  PM CHATCHAI AND HUN SEN CONTINUED THEIR TALKS AT A
WORKING BREAKFAST TODAY AT HUN SEN'S HOTEL BEFORE
CHATCHAI DEPARTED FOR THE PHILIPPINES.  ACCORDING TO ONE
REPORT, THE PM'S ADVISORS MAY HAVE PERSUADED HUN SEN TO
EXTEND HIS VISIT AN ADDITIONAL DAY AND TO LEAVE FOR PHNOM
PENH TOMORROW, AND ALL ACCOUNTS AGREE THAT HE COULD SO
EXTEND HIS VISIT IF HE WISHED.


O'DONOHUE''')

)

_TEST_CABLES = (
    # Expected, Cable ID, c14n
    (u'MURPHY', u'09BERLIN1167', True),
    (u'Murphy', u'09BERLIN1167', False),
    (u'WHITAKER', u'10NIAMEY72', True),
    (u'WHITAKER', u'10NIAMEY72', False),
    (u'GALBRAITH', u'95ZAGREB4339', True),
    (u'GALBRAITH', u'95ZAGREB4339', False),
    (u'KEEGANPAAL', u'04TAIPEI3991', False),
    ((u'KEEGAN', u'PAAL'), u'04TAIPEI3991', True),
    (u'JOHNSONKEANE', u'05ASUNCION807', False),
    ((u'JOHNSON', u'KEANE'), u'05ASUNCION807', True),
    (u'STEWARTBALTIMORE', u'06MUSCAT396', False),
    ((u'STEWART', u'BALTIMORE'), u'06MUSCAT396', True),
    (u'BIGUSBELL', u'06KIRKUK112', False),
    ((u'BIGUS', u'BELL'), u'06KIRKUK112', True),
    (u'PAAL', u'06TAIPEI189', False),
    (u'HELMS', u'73TEHRAN7005', False),
    (u'HELMS', u'75TEHRAN2069', False),
    ((), u'08KINSHASA332', False),
    ((), u'08KINSHASA329', False),
    ((), u'05BOGOTA9232', False),
    (u"ODONOHUE", u'09KUWAIT266', False),
    (u"O'DONOHUE", u'09KUWAIT266', True),
)


def test_data():
    def check(expected, content, c14n):
        if not isinstance(expected, tuple):
            expected = (expected,)
        eq_(expected, tuple(parse_signers(content, c14n)))
    for testcase in _TEST_DATA:
        if len(testcase) == 2:
            expected, data = testcase
            c14n = False
        else:
            expected, data, c14n = testcase
        yield check, expected, data, c14n

def test_cables():
    def check(expected, cable_id, c14n):
        cable = cable_by_id(cable_id)
        if not isinstance(expected, tuple):
            expected = (expected,)
        eq_(expected, tuple(parse_signers(cable.content, c14n)))
    for expected, cable_id, c14n in _TEST_CABLES:
        yield check, expected, cable_id, c14n


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

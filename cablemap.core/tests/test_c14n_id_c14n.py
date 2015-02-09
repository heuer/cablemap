# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests identifier c14n parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.constants import INVALID_CABLE_IDS, MALFORMED_CABLE_IDS
from cablemap.core.c14n import canonicalize_id

_TEST_DATA = (
    # input reference, expected id c14n
    (u'05RIO123', u'05RIODEJANEIRO123'),
    (u'05RIODEJAN123', u'05RIODEJANEIRO123'),
    (u'05PARISFR1', u'05UNESCOPARISFR1'),
    (u'05USUNESCOPARISFR1', u'05UNESCOPARISFR1'),
    (u'05UNVIE1', u'05UNVIEVIENNA1'),
    (u'05EMBASSYVIENNA1', u'05VIENNA1'),
    (u'05EMBASSYBLABLA1', u'05BLABLA1'),
    (u'06SECSTATE123', u'06STATE123'),
    (u'06SECDEF123', u'06SECDEF123'),
    (u'06PORT-OF-SPAIN123', u'06PORTOFSPAIN123'),
    (u'07PORT-AU-PRINCE12', u'07PORTAUPRINCE12'),
    (u'07PAUP12', u'07PORTAUPRINCE12'),
    (u'07PAP12', u'07PORTAUPRINCE12'),
    (u'07SANJSE12', u'07SANJOSE12'),
    (u'07USEU2', u'07USEUBRUSSELS2'),
    (u'07USUN2', u'07USUNNEWYORK2'),
    (u'08HALIF1234', u'08HALIFAX1234'),
    (u'08KUALALUMP1234', u'08KUALALUMPUR1234'),
    (u'08RIODEJANIERO1234', u'08RIODEJANEIRO1234'),
    (u'08BKK23', u'08BANGKOK23'),
    (u'01PANANA12', u'01PANAMA12'),
    (u'01WELLINGOTN12', u'01WELLINGTON12'),
    (u'66USUNNY12', u'66USUNNEWYORK12'),
    (u'05PANAM12', u'05PANAMA12'),
    (u'03MADRIDSP1234', u'03MADRID1234'),
    (u'03KINSTON1234', u'03KINGSTON1234'),
    (u'03BISHTEK1234', u'03BISHKEK1234'),
    (u'04VAT123', u'04VATICAN123'),
    (u'04SAOPAUO123', u'04SAOPAULO123'),
    (u'03SAOPAUL12', u'03SAOPAULO12'),
    (u'03SECTSTATE12', u'03STATE12'),
    (u'03HAGUE12', u'03THEHAGUE12'),
    (u'09PHNOMPEN12', u'09PHNOMPENH12'),
    (u'09TRIPOLII12', u'09TRIPOLI12'),
    (u'09BRASILA12', u'09BRASILIA12'),
    (u'09MEXICOCITY12', u'09MEXICO12'),
    (u'09USUNNEYORK234', u'09USUNNEWYORK234'),
    (u'09BRAZIL234', u'09BRASILIA234'),
    (u'09BA123', u'09BUENOSAIRES123'),
    (u'02USEUBRUSSELS12', u'02USEUBRUSSELS12'),
    (u'02BRUSSELS12', u'02BRUSSELS12'),
    (u'02USDA12', u'02USDAFAS12'),
    ('10CDCATLANTA12', u'10CDCATLANTAGA12'),
    ('10BRASIIA12', '10BRASILIA12'),
    ('10WELLLINGTON12', '10WELLINGTON12'),
    (u'10USCUSTOMSA12', u'10USCBP12'),
    (u'10USDOCWASHDC12', u'10USDOC12'),
    (u'10RIODEJANERIO12', u'10RIODEJANEIRO12'),
    (u'03SECTATE12', u'03STATE12'),
    (u'03SECDEFWASH12', u'03SECDEF12'),
    (u'09BEIJINJG12', u'09BEIJING12'),
    (u'09BRAZILIA12', u'09BRASILIA12'),
    (u'02SCOPAULO12', u'02SAOPAULO12'),
    (u'02TAIPEI12', u'02AITTAIPEI12'),
    (u'09USEUBRUSEELS1292', u'09USEUBRUSSELS1292'),
)

def test_c14n():
    def check(reference_id, canonical_id):
        eq_(canonical_id, canonicalize_id(reference_id))
    for r, c in _TEST_DATA:
        yield check, r, c

def test_c14n_malformed_ids():
    def check(incorrect_id, correct_id):
        eq_(canonicalize_id(correct_id), canonicalize_id(incorrect_id))
    for incorrect_id, correct_id in MALFORMED_CABLE_IDS.iteritems():
        yield check, incorrect_id, correct_id

def test_c14n_illegal_ids():
    def check(incorrect_id, correct_id):
        eq_(canonicalize_id(correct_id), canonicalize_id(incorrect_id))
    for incorrect_id, correct_id in INVALID_CABLE_IDS.iteritems():
        yield check, incorrect_id, correct_id


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

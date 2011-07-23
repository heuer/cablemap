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
Tests identifier c14n parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.constants import INVALID_CABLE_IDS, MALFORMED_CABLE_IDS
from cablemap.core.reader import canonicalize_id

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
    (u'07USEU2', u'07BRUSSELS2'),
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
)

def test_c14n():
    def check(reference_id, canonical_id):
        eq_(canonical_id, canonicalize_id(reference_id))
    for r, c in _TEST_DATA:
        yield check, r, c

def test_c14n_malformed_ids():
    def check(reference_id, canonical_id):
        eq_(canonical_id, canonicalize_id(reference_id))
    for r, c in MALFORMED_CABLE_IDS.iteritems():
        yield check, r, c

def test_c14n_illegal_ids():
    def check(reference_id, canonical_id):
        eq_(canonical_id, canonicalize_id(reference_id))
    for r, c in INVALID_CABLE_IDS.iteritems():
        yield check, r, c


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

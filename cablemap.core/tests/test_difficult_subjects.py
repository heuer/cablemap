# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Subject parsing for cables which contain some oddities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id


_TEST_DATA = (
    (u'02HANOI2686', u'VIETNAM - WHERE DISASTER PREPAREDNESS IS SERIOUS BUSINESS'),
    (u'09TRIPOLI63', u'RISKY BUSINESS? AMERICAN CONSTRUCTION FIRM ENTERS JOINT VENTURE WITH GOL'),
    (u'07YEREVAN202', u'CUSTOMS GIANT FALLS AMID RUMORS OF SMUGGLING AND CORRUPTION'),
    (u'09OSLO399', u"NORWAY'S RUSSIA POLICY: WISHFUL THINKING"),
    (u'06LIMA1452', u"APRA CONFIDENT OF MAKING SECOND-ROUND RUN-OFF, SEEKS EMBASSY'S ASSISTANCE IN CEMENTING DEMOCRATIC COALITION AGAINST HUMALA"),
    (u'06ISLAMABAD5723', u'DEMARCHE DELIVERED: NEVADA TEST SITE'),
    (u'05DHAKA4483', u'Media Reaction: Iraq Constitution Bangladesh-U.S. Bilateral 9/11 anniversary; Dhaka'),
    (u'05DHAKA4410', u'Media Reaction: Aftermath of Katrina; Dhaka'),
    (u'05DHAKA4392', u'Media Reaction: Aftermath of Katrina; Dhaka'),
    (u'05VANCOUVER1524', u'MARIJUANA FLOURISHES IN B.C. AS METHAMPHETAMINE CRISIS HEIGHTENS'),
    (u'07DAKAR258', u'SENEGAL: SCENESETTER FOR GENERAL WARD'),
)


def test_parse_subject():
    def check(expected, cable):
        eq_(expected, cable.subject)
    for ref_id, subject in _TEST_DATA:
        yield check, subject, cable_by_id(ref_id)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests if the media IRIs are detected.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

_TEST_DATA = (
    (u'07BUENOSAIRES1776', [u'http://www.lanacion.com.ar/1360470-cuatro-paises-denunciaron-corrupcion-en-el-gobierno']),
    (u'06MEXICO680', [u'http://wikileaks.jornada.com.mx/notas/eu-no-veia-mal-la-llegada-de-lopez-obrador-a-los-pinos']),
    (u'06WARSAW1592', [u'http://www.mcclatchydc.com/2011/05/16/114269/wikileaks-cables-show-oil-a-major.html']),
    (u'09BERLIN1162', [u'http://www.spiegel.de']),
    (u'05ROME1593', []),
    (u'10UNESCOPARISFR187', [u'http://www.haitiliberte.com',
                             u'http://www.haiti-liberte.com/archives/volume4-48/Le%20d%C3%A9ploiement%20des%20militaires.asp',
                             u'http://www.haiti-liberte.com/archives/volume4-48/Une%20ru%C3%A9e%20vers%20l%E2%80%99or.asp',
                             u'http://www.haiti-liberte.com/archives/volume4-48/U.S.%20Worried%20about%20International.asp',
                             u'http://www.haiti-liberte.com/archives/volume4-48/After%20Quake.asp']),
    (u'06TELAVIV2787', []), # Appears in these articles: http://not http://yet http://set
    # Next contains: http://WL: http://This http://URL?
    (u'08BERLIN1467', [u'http://www.spiegel.de', u'http://www.spiegel.de/international/world/0,1518,732127,00.html']),
    )

def test_media_urls():
    def check(cable, media_urls):
        eq_(sorted(cable.media_uris), sorted(media_urls))
    for cable_id, media_urls in _TEST_DATA:
        yield check, cable_by_id(cable_id), media_urls


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

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
    )

def test_media_urls():
    def check(cable, media_urls):
        eq_(sorted(cable.media_uris), sorted(media_urls))
    for cable_id, media_urls in _TEST_DATA:
        yield check, cable_by_id(cable_id), media_urls


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

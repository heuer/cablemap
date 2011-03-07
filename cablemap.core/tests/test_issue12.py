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
Test against issue #12.
<https://github.com/heuer/cablemap/issues/#issue/12>

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id

def test_issue12_manama():
    cable = cable_by_id('08MANAMA492')
    eq_(u'VZCZCXRO5008', cable.transmission_id)
    eq_(u'08MANAMA492', cable.reference_id)
    cable = cable_by_id('08ECTION01OF02MANAMA492')
    eq_(u'VZCZCXRO4772', cable.transmission_id)
    eq_(u'08MANAMA492', cable.reference_id)

def test_issue12_saopaulo():
    cable = cable_by_id('08SAOPAULO335')
    eq_(u'VZCZCXRO3989', cable.transmission_id)
    eq_(u'08SAOPAULO335', cable.reference_id)
    cable = cable_by_id('08SCTION02OF02SAOPAULO335')
    eq_(u'VZCZCXRO3727', cable.transmission_id)
    eq_(u'08SAOPAULO335', cable.reference_id)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

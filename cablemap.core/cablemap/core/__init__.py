# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Provides access to commonly used functions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
import logging
from cablemap.core.models import cable_from_file, cable_from_html, cable_from_row
from cablemap.core.handler import handle_source
from cablemap.core.utils import cables_from_source, cables_from_directory, cables_from_csv, cable_by_id, cable_by_url
try:
    from logging import NullHandler # Python >= 2.7
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

__all__ = ['cable_from_file', 'cable_from_html', 'cable_from_row',
           'cables_from_source', 'cables_from_directory', 'cables_from_csv',
           'cable_by_id', 'cable_by_url', 'handle_source'
           ]

_nh = NullHandler()

logger = logging.getLogger('cablemap')
logger.addHandler(_nh)



# -*- coding: utf-8 -*-
"""\
DEPRECATED

This module defines an event handler to process cables.
"""
import warnings
warnings.warn('Deprecated, use "cablemap.tm.handler"', DeprecationWarning)
try:
    from cablemap.tm.handler import *
except ImportError:
    raise ImportError('Cannot find "cablemap.tm", install cablemap.tm')

# -*- coding: utf-8 -*-
'''
Send events covering process status
'''

# Import Python Libs
from __future__ import absolute_import, unicode_literals
import logging

# Import third party libs
# pylint: disable=import-error
try:
    import salt.utils.psutil_compat as psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

__virtualname__ = 'allproc'


def __virtual__():
    if not HAS_PSUTIL:
        return (False, 'cannot load ps beacon: psutil not available')
    return __virtualname__


def validate(config):
    return True, 'No configuration yet required'


def beacon(config):
    '''
    Scan for processes and fire events with all process data

    Example Config

    .. code-block:: yaml

        beacons:
          allproc: []
    '''
    ret = []
    procs = set()
    for proc in psutil.process_iter():
        _name = proc.name()
        if _name.startswith('[') and _name.endswith(']'):
            continue
        procs.add(_name)
    for name in procs:
        ret.append({'name': name})
    return ret


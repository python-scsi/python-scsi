# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from .converter import *
from .enum import *


def init_device(dev, read_write=False):
    if dev[:5] == '/dev/':
        from pyscsi.pyscsi.scsi_device import SCSIDevice
        device = SCSIDevice(dev, read_write)
    elif dev[:8] == 'iscsi://':
        from pyscsi.pyiscsi.iscsi_device import ISCSIDevice
        device = ISCSIDevice(dev)
    else:
        raise NotImplementedError('No backend implemented for %s' % dev)
    return device

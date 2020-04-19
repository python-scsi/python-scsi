#!/usr/bin/env python

# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

import sys

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_device import SCSIDevice
from pyscsi.pyscsi.scsi_enum_getlbastatus import P_STATUS
from pyscsi.utils import init_device


def usage():
    print('Usage: getlbastatus.py [--help] [-l <lba>] <device>')


def main():
    i = 1
    lba = 0
    while i < len(sys.argv):
        if sys.argv[i] == '--help':
            return usage()
        if sys.argv[i] == '-l':
            del sys.argv[i]
            lba = int(sys.argv[i], 10)
            del sys.argv[i]
            continue
        i += 1

    if len(sys.argv) < 2:
        return usage()

    device = sys.argv[1]

    sd = init_device(device)
    s = SCSI(sd)

    r = s.readcapacity16().result
    if not r['lbpme']:
        print('LUN is fully provisioned.')
        return

    r = s.getlbastatus(lba).result
    for i in range(len(r['lbas'])):
        print('LBA:%d-%d %s' % (
            r['lbas'][i]['lba'],
            r['lbas'][i]['lba'] + r['lbas'][i]['num_blocks'] - 1,
            P_STATUS[r['lbas'][i]['p_status']]
        ))


if __name__ == "__main__":
    main()

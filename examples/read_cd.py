#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

import sys

#from pyscsi.pyscsi import scsi_enum_readcd as READCD
from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_sense import SCSICheckCondition
from pyscsi.utils import init_device


def usage():
    print('Usage: read_cd.py [-lba <lba>] [-tl <transfer-length>] [-est <expected-sector-type>] [-dap <dap>] [-mcsb <main-channel-selection-bits>] [-c2ei <c2-error-information>] [-scsb <sub-channel-selection-bits>] <device>')

def atoi(s):
    if s[:2] == '0x':
        return int(s, 16)
    else:
        return int(s, 10)
    
def main():
    i = 1
    lba = 0
    tl = 1
    est = 0
    dap = 0
    mcsb = 0x02
    c2ei = 0
    scsb = 0
    while i < len(sys.argv):
        if sys.argv[i] == '--help':
            return usage()
        if sys.argv[i] == '-lba':
            del sys.argv[i]
            lba = atoi(sys.argv[i])
            del sys.argv[i]
            continue
        if sys.argv[i] == '-tl':
            del sys.argv[i]
            tl = atoi(sys.argv[i])
            del sys.argv[i]
            continue
        if sys.argv[i] == '-est':
            del sys.argv[i]
            est = atoi(sys.argv[i])
            del sys.argv[i]
            continue
        if sys.argv[i] == '-dap':
            del sys.argv[i]
            dap = atoi(sys.argv[i])
            del sys.argv[i]
            continue
        if sys.argv[i] == '-mcsb':
            del sys.argv[i]
            mcsb = atoi(sys.argv[i])
            del sys.argv[i]
            continue
        if sys.argv[i] == '-c2ei':
            del sys.argv[i]
            c2ei = atoi(sys.argv[i])
            del sys.argv[i]
            continue
        if sys.argv[i] == '-scsb':
            del sys.argv[i]
            scsb = atoi(sys.argv[i])
            del sys.argv[i]
            continue
        i += 1

    if len(sys.argv) < 2:
        return usage()

    device = init_device(sys.argv[1])

    s = SCSI(device)

    cmd = s.readcd(lba=lba, tl=tl, est=est, dap=dap, mcsb=mcsb, c2ei=c2ei, scsb=scsb)
    print(cmd.result)


if __name__ == "__main__":
    main()

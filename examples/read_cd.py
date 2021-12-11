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
    print('Usage: read_cd.py <device>')


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
            if sys.argv[i][:2] == '0x':
                lba = int(sys.argv[i], 16)
            else:
                lba = int(sys.argv[i], 10)
            del sys.argv[i]
            continue
        if sys.argv[i] == '-tl':
            del sys.argv[i]
            if sys.argv[i][:2] == '0x':
                tl = int(sys.argv[i], 16)
            else:
                tl = int(sys.argv[i], 10)
            del sys.argv[i]
            continue
        if sys.argv[i] == '-est':
            del sys.argv[i]
            est = int(sys.argv[i], 16)
            del sys.argv[i]
            continue
        if sys.argv[i] == '-dap':
            del sys.argv[i]
            dap = int(sys.argv[i])
            del sys.argv[i]
            continue
        if sys.argv[i] == '-mcsb':
            del sys.argv[i]
            mcsb = int(sys.argv[i], 16)
            del sys.argv[i]
            continue
        if sys.argv[i] == '-c2ei':
            del sys.argv[i]
            c2ei = int(sys.argv[i], 16)
            del sys.argv[i]
            continue
        if sys.argv[i] == '-scsb':
            del sys.argv[i]
            scsb = int(sys.argv[i], 16)
            del sys.argv[i]
            continue
        i += 1

    if len(sys.argv) < 2:
        return usage()

    device = init_device(sys.argv[1])

    with SCSI(device) as s:

        try:
            s.testunitready()

            cmd = s.readcd(lba, tl, est=est, dap=dap, mcsb=mcsb, c2ei=c2ei, scsb=scsb)
            di = cmd.datain
            for i in range(tl):
                print('LBA 0x%08x' % (lba + i), '/', lba + i)
                if mcsb & 0x10:
                    print('SYNC', di[:12].hex())
                    di = di[12:]
                if mcsb & 0x04:
                    print('SECTOR HEADER', di[:4].hex())
                    di = di[4:]
                if mcsb & 0x08:
                    if est != 4 and est != 5:
                        raise RuntimeError('Subheader data can only be requested from Mode 2 Form 1/2 sectors')

                    print('SECTOR SUB-HEADER', di[:8].hex())
                    di = di[8:]
                if mcsb & 0x02:
                    ds = 0
                    if est == 2: # Mode 1
                        ds = 2048
                    if est == 3: # Mode 2 formless
                        ds = 2336
                    if est == 4: # Mode 2 form 1
                        ds = 2048
                    if est == 5: # Mode 2 form 2
                        ds = 2324
                    if ds == 0:
                        raise NotImplementedError('USER DATA requested but we can not determine the size of the data area')

                    print('USER DATA', di[:ds].hex())
                    di = di[ds:]
                if mcsb & 0x01:
                        raise NotImplementedError('EDC&ECC')

                if c2ei == 1: # C2 Errors Codes
                    print('C2 ERROR CODES', di[:294].hex())
                    di = di[294:]
                if c2ei == 2: # C2 Errors Codes
                    print('C2 ERROR CODES', di[:296].hex())
                    di = di[296:]
                if scsb == 2: # Formatted Q sub-channel data
                    print('SUB-CHANNEL', di[:16].hex())
                    di = di[16:]
                if scsb == 4: # Corrected and de-interleaved R-W sub-channel data
                    print('SUB-CHANNEL', di[:96].hex())
                    di = di[96:]

        except SCSICheckCondition as ex:
            # if you want a print out of the sense data dict uncomment the next line
            #ex.show_data = True
            print(ex)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# coding: utf-8

import sys
from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_device import SCSIDevice


def main(device):
    s = SCSI(SCSIDevice(device))
    r = s.readcapacity10().result

    s.blocksize = r['block_length']
    print 'Block size:', s.blocksize

    print 'Read10'
    print '==========================================\n'
    r = s.read10(0, 1).datain
    for i in range(len(r)):
        print "%03x : %02x" % (i, r[i])

if __name__ == "__main__":
    main(sys.argv[1])

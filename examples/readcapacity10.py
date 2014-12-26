#!/usr/bin/env python
# coding: utf-8

import sys
from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_device import SCSIDevice


def main(device):
    try:
        sd = SCSIDevice(device)
        s = SCSI(sd)
        print 'ReadCapacity10'
        print '==========================================\n'
        r = s.readcapacity10().result
        for k, v in r.iteritems():
            print '%s - %s' % (k, v)
    except Exception as e:
        print (e)

if __name__ == "__main__":
    main(sys.argv[1])

#!/usr/bin/env python
# coding: utf-8

import sys
from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_device import SCSIDevice


def main(device):
    sd = SCSIDevice(device)
    s = SCSI(sd)

    print 'ReadCapacity16'
    print '==========================================\n'
    r = s.readcapacity16().result
    for k, v in r.iteritems():
        print '%s - %s' % (k, v)

 
if __name__ == "__main__":
    main(sys.argv[1])


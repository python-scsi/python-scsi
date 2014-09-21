#!/usr/bin/env python
# coding: utf-8

import sys
from sgio.pyscsi.scsi import SCSI


def main(device):
    s = SCSI(device)

    print 'ReadCapacity16'
    print '==========================================\n'
    r = s.readcapacity16().result
    for k, v in r.iteritems():
        print '%s - %s' % (k, v)

 
if __name__ == "__main__":
    main(sys.argv[1])


#!/usr/bin/env python
# coding: utf-8

import sys
from pyscsi.pyscsi.scsi import SCSI
from pyscsi.utils import init_device


def main(device):
    with SCSI(device) as s:
        print 'ReadCapacity10'
        print '==========================================\n'
        r = s.readcapacity10().result
        for k, v in r.iteritems():
            print '%s - %s' % (k, v)


if __name__ == "__main__":
    main(init_device(sys.argv[1]))

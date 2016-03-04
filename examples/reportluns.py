#!/usr/bin/env python
# coding: utf-8

#
# A simple example to get a dict with reported luns
#
import sys

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_device import SCSIDevice


def main(device):
    with SCSI(device) as s:
        print 'ReportLuns'
        print '==========================================\n'
        r = s.reportluns().result
        for k, v in r.iteritems():
            print('%s - %s' % (k, v))


if __name__ == "__main__":
    main(sys.argv[1])

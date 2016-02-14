#!/usr/bin/env python
# coding: utf-8

#
# A simple example to get a dict with reported luns
#
import sys

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_device import SCSIDevice


def main(device):
    try:
        sd = SCSIDevice(device)
        s = SCSI(sd)
        s.testunitready()
    except Exception as e:
        print (e)
    else:
        print ('ReportPriority')
        print ('==========================================\n')
        try:
            r = s.reportpriority().result
            for k, v in r.iteritems():
                print('%s - %s' % (k, v))
        except Exception as e:
                print (e)


if __name__ == "__main__":
    main(sys.argv[1])

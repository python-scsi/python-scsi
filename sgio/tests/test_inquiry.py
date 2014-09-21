#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi import scsi_cdb_inquiry as INQUIRY


def main(device):
    s = SCSI(device)

    print 'inquiry without enabled vital product data'
    print '==========================================\n'
    i = s.inquiry().result
    for k, v in i.iteritems():
        print '%s - %s' % (k, v)
    print '\ninquiry with enabled vital product data\nand proper page_code'
    print '==========================================\n'
    i = s.inquiry(evpd = 1, page_code = INQUIRY.VPD.SUPPORTED_VPD_PAGES).result
    for k, v in i.iteritems():
        print '%s - %s' % (k, v)

if __name__ == "__main__":
    main(sys.argv[1])


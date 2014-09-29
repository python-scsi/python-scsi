#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi import scsi_cdb_inquiry as INQUIRY


def main(device):
    s = SCSI(device)

    print 'Inquiry: Standard Page'
    print '==========================================\n'
    i = s.inquiry().result
    for k, v in i.iteritems():
        print '%s - %s' % (k, v)
    print
    print 'Device is a', INQUIRY.DEVICE_TYPE[i['peripheral_device_type']]

    print
    print 'Inquiry: Supported VPD Pages VPD Page'
    print '==========================================\n'
    i = s.inquiry(evpd=1, page_code=INQUIRY.VPD.SUPPORTED_VPD_PAGES).result
    for k, v in i.iteritems():
        print '%s - %s' % (k, v)
    print
    print 'Supported VPD Pages:'
    vpd_pages = i['vpd_pages']
    for pg in vpd_pages:
        print '%02x: %s' % (pg, INQUIRY.VPD[pg])


if __name__ == "__main__":
    main(sys.argv[1])


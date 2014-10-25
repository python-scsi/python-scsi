#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_device import SCSIDevice
from sgio.pyscsi import scsi_cdb_inquiry as INQUIRY

def usage():
    print 'Usage: inquiry.py [-p <page-code>] [--help] <device>'

def inquiry_standard(s):
    i = s.inquiry().result
    print 'Standard INQUIRY'
    print '================'
    print 'PQual=%d  Device_type=%d  RMB=%d  version=0x%02x  %s' % (
        i['peripheral_qualifier'],
        i['peripheral_device_type'],
        i['rmb'],
        i['version'],
        '[SPC3]' if i['version'] == 5 else '')
    print 'NormACA=%d  HiSUP=%d  Resp_data_format=%d' % (
        i['normaca'],
        i['hisup'],
        i['response_data_format'])
    print 'SCCS=%d  ACC=%d  TPGS=%d  3PC=%d  Protect=%d' % (
        i['sccs'],
        i['acc'],
        i['tpgs'],
        i['3pc'],
        i['protect'])
    print 'EncServ=%d  MultiP=%d  Addr16=%d' % (
        i['encserv'],
        i['multip'],
        i['addr16'])
    print 'WBus16=%d  Sync=%d  CmdQue=%d' % (
        i['wbus16'],
        i['sync'],
        i['cmdque'])
    print 'Clocking=%d  QAS=%d  IUS=%d' % (
        i['clocking'],
        i['qas'],
        i['ius'])
    print '  length=%d  Peripheral device type: %s' % (
        i['additional_length'] + 5,
        INQUIRY.DEVICE_TYPE[i['peripheral_device_type']])
    print 'Vendor identification:', i['t10_vendor_identification'][:32]
    print 'Product identification:', i['product_identification'][:32]
    print 'Product revision level:', i['product_revision_level']

def inquiry_supported_vpd_pages(s):
    i = s.inquiry(evpd=1, page_code=INQUIRY.VPD.SUPPORTED_VPD_PAGES).result
    print 'Supported VPD Pages, page_code=0x00'
    print '==================================='
    print 'PQual=%d  Peripheral device type: %s' % (
        i['peripheral_qualifier'],
        INQUIRY.DEVICE_TYPE[i['peripheral_device_type']])
    print '  Supported VPD pages:'
    for pg in i['vpd_pages']:
        print '    0x%02x: %s' % (pg, INQUIRY.VPD[pg])

def main():
    i = 1
    page_code = 0
    evpd = 0
    while i < len(sys.argv):
       if sys.argv[i] == '--help':
           return usage()
       if sys.argv[i] == '-p':
          del sys.argv[i]
          page_code = int(sys.argv[i])
          evpd = 1
          del sys.argv[i]
          continue
       i += 1

    if len(sys.argv) < 2:
        return usage()

    device = sys.argv[1]

    sd = SCSIDevice(device)
    s = SCSI(sd)

    i = s.testunitready()

    if not evpd:
        inquiry_standard(s)
        return

    if page_code == INQUIRY.VPD.SUPPORTED_VPD_PAGES:
        inquiry_supported_vpd_pages(s)
        return


    print 'No pretty print for this page, page_code=0x%02x' % (page_code)
    print '=============================================\n'
    i = s.inquiry(evpd=1, page_code=page_code).result
    for k, v in i.iteritems():
        print '%s - %s' % (k, v)


if __name__ == "__main__":
    main()


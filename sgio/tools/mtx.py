#!/usr/bin/env python
# coding: utf-8

# A reimplementation of the MTX tool in pyton
# incomplete so far but we can build on it

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_device import SCSIDevice
from sgio.pyscsi import scsi_enum_inquiry as INQUIRY
from sgio.pyscsi import scsi_enum_modesense6 as MODESENSE6
from sgio.pyscsi import scsi_enum_readelementstatus as READELEMENTSTATUS


def status(scsi, eaa):
    if eaa['num_data_transfer_elements'] > 0:
        res = scsi.readelementstatus(start=eaa['first_data_transfer_element_address'],
                                     num=eaa['num_data_transfer_elements'],
                                     element_type=READELEMENTSTATUS.ELEMENT_TYPE.DATA_TRANSFER,
                                     voltag=1, curdata=1, dvcid=1, alloclen=16384).result
        elements = res['data_transfer_elements']
        if elements:
            for element in elements['element_descriptors']:
                if element['full']:
                    print 'Data Transfer Element: %d:Full VolumeTag:%s' % (
                        element['element_address'],
                        element['primary_volume_tag'][0:32])
                else:
                    print 'Data Transfer Element: %d:Empty' % (
                        element['element_address'])

    if eaa['num_storage_elements'] > 0:
        res = scsi.readelementstatus(start=eaa['first_storage_element_address'],
                                     num=eaa['num_storage_elements'],
                                     element_type=READELEMENTSTATUS.ELEMENT_TYPE.STORAGE,
                                     voltag=1, curdata=1, dvcid=1, alloclen=16384).result
        ses = res['storage_elements']
        if ses:
            _first = res['first_element_address']
            for se in ses['element_descriptors']:
                if se['full']:
                    print '      Storage Element: %d:Full VolumeTag:%s' % (
                        se['element_address'] - _first + 1,
                        se['primary_volume_tag'][0:32])
                else:
                    print '      Storage Element: %d:Empty' % (
                        se['element_address'] - _first + 1)

def main():
    device = '/dev/changer'
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-f':
            del sys.argv[i]
            device = sys.argv[i]
            del sys.argv[i]
            break

    scsi = SCSI(SCSIDevice(device))
    i = scsi.inquiry().result
    if i['peripheral_device_type'] != INQUIRY.DEVICE_TYPE.MEDIA_CHANGER_DEVICE:
        print '%s is not a MediaChanger device' % device
        return

    eaa = scsi.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result

    if sys.argv[1] == 'status':
        return status(scsi, eaa)


if __name__ == "__main__":
    main()


#!/usr/bin/env python

# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

# A reimplementation of the MTX tool in pyton
# incomplete so far but we can build on it

import sys

from pyscsi.pyscsi import scsi_enum_inquiry as INQUIRY
from pyscsi.pyscsi import scsi_enum_modesense as MODESENSE6
from pyscsi.pyscsi import scsi_enum_readelementstatus as READELEMENTSTATUS
from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_device import SCSIDevice
from pyscsi.utils import init_device


def status(scsi, dte, se):
    # For ease of use we renumber the element addresses to start at
    # 0 for data transfer elements and to start at num_data_transfer_elements
    # for the storage elements.
    _fdte = 99999999
    for element in dte:
        if element['element_address'] < _fdte:
            _fdte = element['element_address']
    _fse = 99999999
    for element in se:
        if element['element_address'] < _fse:
            _fse = element['element_address']

    for element in dte:
        if element['full']:
            print('Data Transfer Element: %d:Full VolumeTag:%s' % (
                element['element_address'] - _fdte,
                element['primary_volume_tag'][0:32]))
        else:
            print('Data Transfer Element: %d:Empty' % (
                element['element_address'] - _fdte))
    for element in se:
        if element['full']:
            print('      Storage Element: %d:Full VolumeTag:%s' % (
                element['element_address'] - _fse + len(dte),
                element['primary_volume_tag'][0:32]))
        else:
            print('      Storage Element: %d:Empty' % (
                element['element_address'] - _fse + len(dte)))


def load(scsi, mte, dte, se, storage_element, data_transfer_element):
    _fmte = 99999999
    for element in mte:
        if element['element_address'] < _fmte:
            _fmte = element['element_address']
    _fdte = 99999999
    for element in dte:
        if element['element_address'] < _fdte:
            _fdte = element['element_address']
    _fse = 99999999
    for element in se:
        if element['element_address'] < _fse:
            _fse = element['element_address']

    res = scsi.movemedium(_fmte,
                          storage_element + _fse - _fdte,
                          data_transfer_element + _fdte).result
    print('Loaded Storage Element %d into Data Transfer drive %d' % (storage_element, data_transfer_element))


def unload(scsi, mte, dte, se, storage_element, data_transfer_element):
    _fmte = 99999999
    for element in mte:
        if element['element_address'] < _fmte:
            _fmte = element['element_address']
    _fdte = 99999999
    for element in dte:
        if element['element_address'] < _fdte:
            _fdte = element['element_address']
    _fse = 99999999
    for element in se:
        if element['element_address'] < _fse:
            _fse = element['element_address']

    res = scsi.movemedium(_fmte,
                          data_transfer_element + _fdte,
                          storage_element + _fse - _fdte).result
    print('Unloaded Data Transfer drive %d into Storage Element %d ' % (data_transfer_element, storage_element))


def usage():
    print('Usage:')
    print('mtx.py -f <device> status')
    print('mtx.py -f <device> load <src> <dst>')
    print('mtx.py -f <device> unload <dst> <src>')


def main():
    device = ''
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-f':
            del sys.argv[i]
            device = sys.argv[i]
            del sys.argv[i]
            break

    if not device:
        usage()
        exit(1)

    scsi = SCSI(init_device(device))
    i = scsi.inquiry().result
    if i['peripheral_device_type'] != INQUIRY.DEVICE_TYPE.MEDIA_CHANGER_DEVICE:
        print('%s is not a MediaChanger device' % device)
        exit(1)

    eaa = scsi.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result['mode_pages'][0]

    # get the data transfer elements
    dte = scsi.readelementstatus(
        start=eaa['first_data_transfer_element_address'],
        num=eaa['num_data_transfer_elements'],
        element_type=READELEMENTSTATUS.ELEMENT_TYPE.DATA_TRANSFER,
        voltag=1, curdata=1, dvcid=1,
        alloclen=16384).result['element_status_pages'][0]['element_descriptors']

    # get all the storage elements
    se = scsi.readelementstatus(
        start=eaa['first_storage_element_address'],
        num=eaa['num_storage_elements'],
        element_type=READELEMENTSTATUS.ELEMENT_TYPE.STORAGE,
        voltag=1, curdata=1, dvcid=1,
        alloclen=16384).result['element_status_pages'][0]['element_descriptors']

    # get all the medium transport elements
    mte = scsi.readelementstatus(
        start=eaa['first_medium_transport_element_address'],
        num=eaa['num_medium_transport_elements'],
        element_type=READELEMENTSTATUS.ELEMENT_TYPE.MEDIUM_TRANSPORT,
        voltag=1, curdata=1, dvcid=1,
        alloclen=16384).result['element_status_pages'][0]['element_descriptors']

    if sys.argv[1] == 'status':
        return status(scsi, dte, se)

    if sys.argv[1] == 'load':
        return load(scsi, mte, dte, se, int(sys.argv[2]), int(sys.argv[3]))

    if sys.argv[1] == 'unload':
        return unload(scsi, mte, dte, se, int(sys.argv[2]), int(sys.argv[3]))

    usage()
    exit(1)


if __name__ == "__main__":
    main()

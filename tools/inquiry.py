#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

import sys

from pyscsi.pyscsi import scsi_enum_inquiry as INQUIRY
from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_sense import SCSICheckCondition
from pyscsi.utils import init_device


def usage():
    print('Usage: inquiry.py [-p <page-code>] [--help] <device>')


def inquiry_standard(s):
    cmd = s.inquiry()
    i = cmd.result
    print('Standard INQUIRY')
    print('================')
    print('PQual=%d  Device_type=%d  RMB=%d  version=0x%02x  %s' % (
        i['peripheral_qualifier'],
        i['peripheral_device_type'],
        i['rmb'],
        i['version'],
        '[SPC3]' if i['version'] == 5 else ''))
    print('NormACA=%d  HiSUP=%d  Resp_data_format=%d' % (
        i['normaca'],
        i['hisup'],
        i['response_data_format']))
    print('SCCS=%d  ACC=%d  TPGS=%d  3PC=%d  Protect=%d' % (
        i['sccs'],
        i['acc'],
        i['tpgs'],
        i['3pc'],
        i['protect']))
    print('EncServ=%d  MultiP=%d  Addr16=%d' % (
        i['encserv'],
        i['multip'],
        i['addr16']))
    print('WBus16=%d  Sync=%d  CmdQue=%d' % (
        i['wbus16'],
        i['sync'],
        i['cmdque']))
    print('Clocking=%d  QAS=%d  IUS=%d' % (
        i['clocking'],
        i['qas'],
        i['ius']))
    print('  length=%d  Peripheral device type: %s' % (i['additional_length'] + 5,
                                                       cmd.DEVICE_TYPE[i['peripheral_device_type']]))
    print('Vendor identification:', i['t10_vendor_identification'][:32].decode(encoding="utf-8",
                                                                               errors="strict"))
    print('Product identification:', i['product_identification'][:32].decode(encoding="utf-8",
                                                                             errors="strict"))
    print('Product revision level:', i['product_revision_level'].decode(encoding="utf-8",
                                                                        errors="strict"))


def inquiry_supported_vpd_pages(s):
    cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.SUPPORTED_VPD_PAGES)
    i = cmd.result
    print('Supported VPD Pages, page_code=0x00')
    print('===================================')
    print('PQual=%d  Peripheral device type: %s' % (i['peripheral_qualifier'],
                                                    cmd.DEVICE_TYPE[i['peripheral_device_type']]))
    print('  Supported VPD pages:')
    for pg in i['vpd_pages']:
        print('    0x%02x: %s' % (pg, cmd.VPD[pg]))


def inquiry_block_limits(s):
    cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.BLOCK_LIMITS)
    i = cmd.result
    print('Block Limits, page_code=0xb0 (SBC)')
    print('==================================')
    print('  Maximum compare and write length:', i['max_caw_len'])
    print('  Optimal transfer length granularity:', i['opt_xfer_len_gran'])
    print('  Maximum transfer length:', i['max_xfer_len'])
    print('  Optimal transfer length:', i['opt_xfer_len'])
    print('  Maximum prefetch, xdread, xdwrite transfer length:', i['max_pfetch_len'])
    print('  Maximum unmap LBA count:', i['max_unmap_lba_count'])
    print('  Maximum unmap block descriptor count:', i['max_unmap_bd_count'])
    print('  Optimal unmap granularity:', i['opt_unmap_gran'])
    print('  Unmap granularity alignment valid:', i['ugavalid'])
    print('  Unmap granularity alignment:', i['unmap_gran_alignment'])


def inquiry_block_dev_char(s):
    cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.BLOCK_DEVICE_CHARACTERISTICS)
    i = cmd.result
    print('Block Device Characteristics, page_code=0xb1 (SBC)')
    print('==================================================')
    print('  Nominal rotation rate: %d rpm' % (i['medium_rotation_rate']))
    print('  Product type=%d' % (i['product_type']))
    print('  WABEREQ=%d' % (i['wabereq']))
    print('  WACEREQ=%d' % (i['wacereq']))
    print('  Nominal form factor %s inches' % (
        cmd.NOMINAL_FORM_FACTOR[i['nominal_form_factor']]))
    print('  VBULS=%d' % (i['vbuls']))


def inquiry_logical_block_prov(s):
    cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.LOGICAL_BLOCK_PROVISIONING)
    i = cmd.result
    print('Logical Block Provisioning, page_code=0xb2 (SBC)')
    print('================================================')
    print('  Threshold=%d blocks  [%s]' % (1 << i['threshold_exponent'],
                                           'NO LOGICAL BLOCK PROVISIONING SUPPORT' if not
                                           i['threshold_exponent'] else 'exponent=%d' % (
                                           i['threshold_exponent'])))
    print('  LBPU=%d  LBPWS=%d  LBPWS10=%d  LBPRZ=%d  ANC_SUP=%d  DP=%d' % (i['lbpu'],
                                                                            i['lpbws'],
                                                                            i['lbpws10'],
                                                                            i['lbprz'],
                                                                            i['anc_sup'],
                                                                            i['dp']))
    print('  Provisioning Type=%d  [%s]' % (i['provisioning_type'],
                                            cmd.PROVISIONING_TYPE[i['provisioning_type']]))


def inquiry_unit_serial_number(s):
    cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.UNIT_SERIAL_NUMBER)
    i = cmd.result
    print('Unit Serial Number, page_code=0x80')
    print('==================================')
    print('  Unit serial number: %s' % (i['unit_serial_number']))


def inquiry_device_identification(s):
    cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.DEVICE_IDENTIFICATION, alloclen=16383)
    i = cmd.result
    print('Device Identification, page_code=0x83')
    print('=====================================')
    _d = i['designator_descriptors']
    for idx in range(len(_d)):
        print('  Designation descriptor, descriptor length: %d' %
              (_d[idx]['designator_length'] + 4))
        print('    designator type:%d [%s]  code set:%d [%s]' %
              (_d[idx]['designator_type'],
               cmd.DESIGNATOR[_d[idx]['designator_type']],
               _d[idx]['code_set'],
               cmd.CODE_SET[_d[idx]['code_set']]))
        print('    association:%d [%s]' % (_d[idx]['association'],
                                           cmd.ASSOCIATION[_d[idx]['association']]))
        for k, v in _d[idx]['designator'].items():
            print('      %s: %s' % (k, v))


def inquiry_ata_information(s):
    specific_config = {
        14280: 'Device requires SET FEATURES subcommand to spin-up after power-up\n'
               'and IDENTIFY DEVICE data is incomplete',
        29640: 'Device requires SET FEATURES subcommand to spin-up after power-up\n'
               'and DEVICE data is complete',
        35955: 'Device does not require SET FEATURES subcommand to spin-up after power-up\n'
               'and IDENTIFY DEVICE data is incomplete',
        51255: 'Device does not require SET FEATURES subcommand to spin-up after power-up\n'
               'and IDENTIFY DEVICE data is complete',
    }
    print('ATA Information, page_code=0x89')
    print('=============================================\n')
    cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.ATA_INFORMATION)
    i = cmd.result
    print('SAT Vendor Identification:', i['sat_vendor_identification'].decode(encoding="utf-8",
                                                                              errors="strict"))
    print('SAT Product Identification:', i['sat_product_identification'].decode(encoding="utf-8",
                                                                                errors="strict"))
    print('SAT Product Revisions Level:', i['sat_product_rev_lvl'].decode(encoding="utf-8",
                                                                          errors="strict"))
    if 'signature' in i.keys():
        sig = i['signature']
        print('Signature Information:')
        print('    Sector Count:', sig['sector_count'])
        print('    LBA low:', sig['lba_low'])
        print('    LBA mid/Byte Count low:', sig['lba_mid'])
        print('    LBA high/Byte Count high:', sig['lba_high'])
        print('    Device:', sig['device'])
    if 'identify' in i.keys():
        ident = i['identify']
        print('Identify Device or Identify Package Device Data:')
        print('    General Configuration:')
        print('        ATA Device:',
              'yes' if ident['general_config']['ata_device'] == 0 else 'no')
        print('        Response incomplete:',
              'yes' if ident['general_config']['ata_device'] == 2 else 'no')
        print('    Specific Configuration:')
        print('       ', (specific_config[ident['specific_config']]
                          if ident['specific_config'] in specific_config.keys() else 'reserved'))
        print('    Device Serial number: %s' % ident['serial_number'].decode(encoding="utf-8",
                                                                             errors="replace"))
        print('    Firmware Revision:', ident['firmware_rev'].decode(encoding="utf-8",
                                                                     errors="replace"))
        print('    Model Number:', ident['model_number'].decode(encoding="utf-8",
                                                                errors="replace"))


def main():
    i = 1
    page_code = 0
    evpd = 0
    while i < len(sys.argv):
        if sys.argv[i] == '--help':
            return usage()
        if sys.argv[i] == '-p':
            del sys.argv[i]
            page_code = int(sys.argv[i], 16)
            evpd = 1
            del sys.argv[i]
            continue
        i += 1

    if len(sys.argv) < 2:
        return usage()

    device = init_device(sys.argv[1])

    with SCSI(device) as s:

        try:
            s.testunitready()

            if not evpd:
                inquiry_standard(s)
                return

            if page_code == INQUIRY.VPD.SUPPORTED_VPD_PAGES:
                inquiry_supported_vpd_pages(s)
                return

            if page_code == INQUIRY.VPD.BLOCK_LIMITS:
                inquiry_block_limits(s)
                return

            if page_code == INQUIRY.VPD.BLOCK_DEVICE_CHARACTERISTICS:
                inquiry_block_dev_char(s)
                return

            if page_code == INQUIRY.VPD.LOGICAL_BLOCK_PROVISIONING:
                inquiry_logical_block_prov(s)
                return

            if page_code == INQUIRY.VPD.UNIT_SERIAL_NUMBER:
                inquiry_unit_serial_number(s)
                return

            if page_code == INQUIRY.VPD.DEVICE_IDENTIFICATION:
                inquiry_device_identification(s)
                return

            if page_code == INQUIRY.VPD.ATA_INFORMATION:
                inquiry_ata_information(s)
                return

            print('No pretty print( for this page, page_code=0x%02x' % page_code)
            print('=============================================\n')
            cmd = s.inquiry(evpd=1, page_code=page_code)
            i = cmd.result
            for k, v in i.items():
                print('%s - %s' % (k, v))
        except SCSICheckCondition as ex:
            # if you want a print out of the sense data dict uncomment the next line
            #ex.show_data = True
            print(ex)


if __name__ == "__main__":
    main()

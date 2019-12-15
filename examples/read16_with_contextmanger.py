#!/usr/bin/env python
# coding: utf-8
import sys
from pyscsi.pyscsi.scsi_cdb_read16 import Read16
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils import init_device


def ba_to_int(ba):
    return sum(b for b in ba)


def ba_to_hex(ba):
    result = ''
    for b in ba:
        result += hex(b)[2:]
    return result


def main(device):
    """
    simple use case for a scsi device without the scsi helper. SCSIDevice has also a contextmanager so we can
    use the with statement but we need to take care of the initialization of a SCSICommand and the execution of the
    command with the device.
    """
    with device as d:
        cmd = Read16(sbc.READ_16, blocksize=512, lba=1, tl=1)
        d.execute(cmd)
        r = cmd.datain
        print('Read16 - GPT Header')
        print('==========================================\n')
        print('signature: %s' % r[:8])
        print('revision: %.1f' % float(ba_to_int(r[8:12])))
        print('header size: %s byte' % ba_to_int(r[12:16]))
        print('crc32 of header: %s' % ba_to_hex(r[16:20]))
        print('reserved: %s' % ba_to_int(r[20:24]))
        print('current LBA: %s' % ba_to_int(r[24:32]))
        print('backup LBA: %s' % ba_to_int(r[32:40]))
        print('first usable LBA for partitions: %s' % ba_to_int(r[40:48]))
        print('last usable LBA: %s' % ba_to_int(r[48:56]))
        print('Disk GUID: %s' % ba_to_hex(r[56:72]))
        print('Starting LBA of array of partition entries: %s' % ba_to_int(r[72:80]))
        print('number of partition entries in array: %s' % ba_to_int(r[80:84]))
        print('size of a single partition entry: %s' % ba_to_int(r[84:88]))
        print('crc32 of header: %s' % ba_to_hex(r[88:92]))


if __name__ == "__main__":
    main(init_device(sys.argv[1]))

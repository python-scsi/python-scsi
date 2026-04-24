# coding: utf-8

# Copyright (C) 2026 by Brian Meagher<brian.meagher@truenas.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import scsi_int_to_ba

#
# SCSI UNMAP command and definitions
#
# See SBC-4 5.35 UNMAP command
#


class Unmap(SCSICommand):
    """
    A class to send an UNMAP command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
        "anchor": [0x01, 1],
        "group": [0x3F, 6],
        "parameter_list_length": [0xFFFF, 7],
    }

    @classmethod
    def marshall_dataout(cls, lbas):
        """
        Build the UNMAP parameter list (SBC-4 5.35.1).

        :param lbas: a list of dicts, each with 'lba' and 'num_blocks' keys
        :return: a bytearray
        """
        descriptors = bytearray()
        for entry in lbas:
            d = bytearray(16)
            d[0:8] = scsi_int_to_ba(entry["lba"], 8)
            d[8:12] = scsi_int_to_ba(entry["num_blocks"], 4)
            # bytes 12-15: reserved
            descriptors += d

        desc_len = len(descriptors)
        header = bytearray(8)
        # UNMAP DATA LENGTH: length of remaining bytes (total - 2)
        header[0:2] = scsi_int_to_ba(6 + desc_len, 2)
        # UNMAP BLOCK DESCRIPTOR DATA LENGTH
        header[2:4] = scsi_int_to_ba(desc_len, 2)
        # bytes 4-7: reserved

        return header + descriptors

    def __init__(self, opcode, lbas, anchor=0, group=0):
        """
        initialize a new instance

        :param opcode: an OpCode instance
        :param lbas: a list of dicts, each with 'lba' and 'num_blocks' keys,
                     specifying the LBA ranges to unmap
        :param anchor: Anchor flag, 0 or 1
        :param group: Group Number
        """
        _data = Unmap.marshall_dataout(lbas)
        SCSICommand.__init__(self, opcode, 0, 0)
        self.dataout = _data
        self.cdb = self.build_cdb(
            opcode=self.opcode.value,
            anchor=anchor,
            parameter_list_length=len(_data),
            group=group,
        )

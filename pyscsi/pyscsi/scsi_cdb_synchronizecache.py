# coding: utf-8

# Copyright (C) 2024 by Folkert van Heusden <mail@vanheusden.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI SYNCHRONIZE_CACHE command
#


class SynchronizeCache(SCSICommand):
    """
    A class to hold information from a synchronizecache command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
    }

    def __init__(self, opcode):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        """
        SCSICommand.__init__(self, opcode, 0, 0)

        self.cdb = self.build_cdb(opcode=self.opcode.value)

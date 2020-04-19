# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI TestUnitReady command
#


class TestUnitReady(SCSICommand):
    """
    A class to hold information from a testunitready command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0], }

    def __init__(self,
                 opcode):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value)

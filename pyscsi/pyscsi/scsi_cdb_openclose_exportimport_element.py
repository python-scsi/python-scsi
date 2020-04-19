# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI OpenCloseImportExportElement command and definitions
#


class OpenCloseImportExportElement(SCSICommand):
    """
    A class to hold information from a OpenCloseImportExportElement
    command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'element_address': [0xffff, 2],
                 'action_code': [0x1f, 4], }

    def __init__(self,
                 opcode,
                 xfer,
                 acode,
                 **kwargs):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param xfer: element address
        :param acode: action code
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  element_address=xfer,
                                  action_code=acode, )

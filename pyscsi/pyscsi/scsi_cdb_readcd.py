# coding: utf-8

# Copyright (C) 2021 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import decode_bits, encode_dict

#
# SCSI ReadCd command and definitions
#


class ReadCd(SCSICommand):
    """
    A class to hold information from a ReadCd command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'est': [0x1c, 1],
                 'dap': [0x02, 1],
                 'lba': [0xffffffff, 2],
                 'tl': [0xffff, 6],
                 'mcsb': [0xf8, 9],
                 'c2ei': [0x06, 9],
                 'scsb': [0x07, 10],
                 }

    def __init__(self,
                 opcode,
                 lba,
                 tl,
                 est=0,
                 dap=0,
                 mcsb=0,
                 c2ei=0,
                 scsb=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param lba: Logical Block Address
        :param tl: transfer length
        :param est=0: Expected Sector Type
        :param dap=0: Digital Audio Play
        :param mcsb=0: Main Channel Selection Bits
        :param c2e1=0: C2 Error Information
        :param scsb=0: Sub-Channel Selection Bits
        """

        # dont bother to compute the exact allocation length needed, just use
        # 3kb per lba
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             tl * 3072)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  lba=lba,
                                  tl=tl,
                                  est=est,
                                  dap=dap,
                                  mcsb=mcsb,
                                  c2ei=c2ei,
                                  scsb=scsb)

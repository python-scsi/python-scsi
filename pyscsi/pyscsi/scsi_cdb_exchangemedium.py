# coding: utf-8

# Copyright:
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import encode_dict, decode_bits

#
# SCSI ExchangeMedium command and definitions
#


class ExchangeMedium(SCSICommand):
    """
    A class to hold information from a ExchangeMedium command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'medium_transport_address': [0xffff, 2],
                 'source_address': [0xffff, 4],
                 'first_destination_address': [0xffff, 6],
                 'second_destination_address': [0xffff, 8],
                 'inv2': [0x01, 10],
                 'inv1': [0x02, 10], }

    def __init__(self, opcode, xfer, source, dest1, dest2, inv1=0, inv2=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param xfer: medium transfer address
        :param source: source address
        :param dest1: first destination address
        :param dest2: second destination address
        :param inv1: value indicating if first destination should be inverted
        :param inv2: value indicating if scond destination should be inverted
        """
        SCSICommand.__init__(self, opcode, 0, 0)
        self.cdb = self.build_cdb(xfer, source, dest1, dest2, inv1, inv2)

    def build_cdb(self, xfer, source, dest1, dest2, inv1, inv2):
        """
        Build a ExchangeMedium CDB

        :param xfer: medium transfer address
        :param source: source address
        :param dest1: first destination address
        :param dest2: second destination address
        :param inv1: value indicating if first destination should be inverted
        :param inv2: value indicating if scond destination should be inverted
        :return: a byte array representing a code descriptor block
        """
        cdb = {
            'opcode': self.opcode.value,
            'medium_transport_address': xfer,
            'source_address': source,
            'first_destination_address': dest1,
            'second_destination_address': dest2,
            'inv1': inv1,
            'inv2': inv2, }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ExchangeMedium cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, ExchangeMedium._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ExchangeMedium cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(12)
        encode_dict(cdb, ExchangeMedium._cdb_bits, result)
        return result


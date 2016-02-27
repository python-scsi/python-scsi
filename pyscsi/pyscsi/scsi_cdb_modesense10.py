# coding: utf-8

# Copyright:
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# Copyright (C) 2015 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
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
from pyscsi.utils.converter import scsi_int_to_ba, encode_dict, decode_bits, scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_modesense import PAGE_CODE, MODESENSE10, MODESELECT10

#
# SCSI ModeSense10 command and definitions
#


class ModeSense10(SCSICommand):
    """
    A class to hold information from a modesense10 command
    """

    def __init__(self,
                 opcode,
                 page_code,
                 sub_page_code=0,
                 llbaa=0,
                 dbd=0,
                 pc=0,
                 alloclen=96):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param page_code: the page code for the vpd page
        :param sub_page_code: a integer representing a sub page code
        :param llbaa: long LBA accepted can be 0 or 1
        :param dbd: disable block descriptor can be 0 or 1. If set to 1 server shall not return any block descriptor
        :param pc: page control field, a value between 0 and 3
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)
        self.cdb = self.build_cdb(page_code,
                                  sub_page_code,
                                  llbaa,
                                  dbd,
                                  pc,
                                  alloclen)

    def build_cdb(self,
                  page_code,
                  sub_page_code,
                  llbaa,
                  dbd,
                  pc,
                  alloclen):
        """

        :param page_code: the page code for the vpd page
        :param sub_page_code: a integer representing a sub page code
        :param llbaa: long LBA accepted can be 0 or 1
        :param dbd: disable block descriptor can be 0 or 1. If set to 1 server shall not return any block descriptor
        :param pc: page control field, a value between 0 and 3
        :param alloclen: the max number of bytes allocated for the data_in buffer
        :return: a byte array representing a code descriptor block
        """
        cdb = {'opcode': self.opcode.value,
               'llbaa': llbaa,
               'dbd': dbd,
               'page_code': page_code,
               'pc': pc,
               'sub_page_code': sub_page_code,
               'alloc_len': alloclen, }

        return self.marshall_cdb(cdb)

    def unmarshall(self):
        """
        wrapper method for unmarshall_datain method.
        """
        self.result = self.unmarshall_datain(self.datain)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ModeSense10 datain.

        :param data: a byte array
        :return result: a dict
        """
        result = {}
        _mps = []
        decode_bits(data[0:8],
                    MODESENSE10.mode_parameter_header_bits,
                    result)

        _bdl = scsi_ba_to_int(data[6:8])
        block_descriptor = data[8:_bdl]  # no one really use this variable in here ?

        data = data[8 + _bdl:]

        _r = {}
        if not data[0] & 0x40:
            decode_bits(data,
                        MODESENSE10.page_zero_bits,
                        _r)
            data = data[2:]
        else:
            decode_bits(data,
                        MODESENSE10.sub_page_bits,
                        _r)
            data = data[4:]

        if _r['page_code'] == PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
            decode_bits(data,
                        MODESENSE10.element_address_bits,
                        _r)
        if _r['page_code'] == PAGE_CODE.CONTROL:
            if not 'sub_page_code' in _r:
                decode_bits(data,
                            MODESENSE10.control_bits,
                            _r)
            elif _r['sub_page_code'] == 1:
                decode_bits(data,
                            MODESENSE10.control_extension_1_bits,
                            _r)
        if _r['page_code'] == PAGE_CODE.DISCONNECT_RECONNECT:
            if not 'sub_page_code' in _r:
                decode_bits(data,
                            MODESENSE10.disconnect_reconnect_bits,
                            _r)

        _mps.append(_r)

        result.update({'mode_pages': _mps})
        return result

    @staticmethod
    def marshall_datain(data):
        """
        Marshall the ModeSense10 datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(8)
        encode_dict(data,
                    MODESENSE10.mode_parameter_header_bits,
                    result)

        # mode page header
        for mp in data['mode_pages']:
            if not mp['spf']:
                _d = bytearray(2)
                encode_dict(mp,
                            MODESENSE10.page_zero_bits,
                            _d)
            else:
                _d = bytearray(4)
                encode_dict(mp,
                            MODESENSE10.sub_page_bits,
                            _d)

            if mp['page_code'] == PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
                _mpd = bytearray(18)
                encode_dict(mp,
                            MODESENSE10.element_address_bits,
                            _mpd)
            if mp['page_code'] == PAGE_CODE.CONTROL:
                if not mp['spf']:
                    _mpd = bytearray(10)
                    encode_dict(mp,
                                MODESENSE10.control_bits,
                                _mpd)
                elif mp['sub_page_code'] == 1:
                    _mpd = bytearray(28)
                    encode_dict(mp,
                                MODESENSE10.control_extension_1_bits,
                                _mpd)
            if mp['page_code'] == PAGE_CODE.DISCONNECT_RECONNECT:
                if not mp['spf']:
                    _mpd = bytearray(14)
                    encode_dict(mp,
                                MODESENSE10.disconnect_reconnect_bits,
                                _mpd)

            if not mp['spf']:
                _d[1] = len(_mpd)
            else:
                _d[2:4] = scsi_int_to_ba(len(_mpd), 2)

            result += _d
            result += _mpd

        result[0] = len(result) - 1
        return result

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ModeSense10 cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    MODESENSE10.cdb_bits,
                    result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ModeSense10 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(10)
        encode_dict(cdb,
                    MODESENSE10.cdb_bits,
                    result)
        return result


class ModeSelect10(SCSICommand):
    """
    A class to hold information from a ModeSelect10 command
    """
    def __init__(self,
                 opcode,
                 data,
                 pf=1,
                 sp=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param data: a dict holding mode page to set
        :param pf: page format value can be 0 or 1
        :param sp: save pages value can be 0 or 1
        """
        _d = ModeSense10.marshall_datain(data)

        SCSICommand.__init__(self,
                             opcode,
                             len(_d),
                             0)
        self.dataout = _d
        self.cdb = self.build_cdb(pf,
                                  sp,
                                  len(_d))

    def build_cdb(self,
                  pf,
                  sp,
                  alloclen):
        """
        method to create a byte array for a Command Descriptor Block with a proper length

        :param pf: page format value can be 0 or 1
        :param sp: save pages value can be 0 or 1
        :param alloclen: length of the parameter list
        """
        cdb = {'opcode': self.opcode.value,
               'pf': pf,
               'sp': sp,
               'parameter_list_length': alloclen, }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_datain(data):
        """
        wrapper method for unmarshall_datain method.

        :param data: a byte array
        :return result: a dict
        """
        return ModeSense10.unmarshall_dataout(data)

    @staticmethod
    def marshall_dataout(data):
        """
        Marshall the ModeSelect6 dataout.

        :param data: a dict
        :return result: a byte array
        """
        return ModeSense10.marshall_datain(data)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ModeSelect10 cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    MODESELECT10.modeselect10_cdb_bits,
                    result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ModeSelect10 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(10)
        encode_dict(cdb,
                    MODESELECT10.modeselect10_cdb_bits,
                    result)
        return result

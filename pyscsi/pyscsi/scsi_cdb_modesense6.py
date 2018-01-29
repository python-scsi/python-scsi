# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
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
from pyscsi.utils.converter import scsi_int_to_ba, encode_dict, decode_bits
import pyscsi.pyscsi.scsi_enum_modesense as modesense_enums

#
# SCSI ModeSense6 command and definitions
#

# we get a generator for all modeselect10 enums, so we can add them to the class
_enums = ((key, modesense_enums.__dict__[key]) for key in modesense_enums.__dict__.keys()
          if key in modesense_enums.__all__ and key not in ['MODESENSE10'])


class ModeSense6(SCSICommand):
    """
    A class to hold information from a modesense6 command
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'dbd': [0x08, 1],
                 'pc': [0xc0, 2],
                 'page_code': [0x3f, 2],
                 'sub_page_code': [0xff, 3],
                 'alloc_len': [0xff, 4], }

    for enum in _enums:
        setattr(SCSICommand, enum[0], enum[1])

    def __init__(self,
                 opcode,
                 page_code,
                 sub_page_code=0,
                 dbd=0,
                 pc=0,
                 alloclen=96):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param page_code: the page code for the vpd page
        :param sub_page_code: a integer representing a sub page code
        :param dbd: disable block descriptor can be 0 or 1. If set to 1 server shall not
                    return any block descriptor
        :param pc: page control field, a value between 0 and 3
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)
        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  page_code=page_code,
                                  sub_page_code=sub_page_code,
                                  dbd=dbd,
                                  pc=pc,
                                  alloc_len=alloclen)

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the ModeSense6 datain.

        :param data: a byte array with data
        :return result: a dict
        """
        result = {}
        _mps = []
        decode_bits(data[0:4],
                    cls.MODESENSE6.mode_parameter_header_bits,
                    result)

        _bdl = data[3]
        block_descriptor = data[4:_bdl]  # no one really use this variable in here ?

        data = data[4 + _bdl:]

        _r = {}
        if not data[0] & 0x40:
            decode_bits(data,
                        cls.MODESENSE6.page_zero_bits,
                        _r)
            data = data[2:]
        else:
            decode_bits(data,
                        cls.MODESENSE6.sub_page_bits,
                        _r)
            data = data[4:]

        if _r['page_code'] == cls.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
            decode_bits(data,
                        cls.MODESENSE6.element_address_bits,
                        _r)
        if _r['page_code'] == cls.PAGE_CODE.CONTROL:
            if 'sub_page_code' not in _r:
                decode_bits(data,
                            cls.MODESENSE6.control_bits,
                            _r)
            elif _r['sub_page_code'] == 1:
                decode_bits(data,
                            cls.MODESENSE6.control_extension_1_bits,
                            _r)
        if _r['page_code'] == cls.PAGE_CODE.DISCONNECT_RECONNECT:
            if 'sub_page_code' not in _r:
                decode_bits(data,
                            cls.MODESENSE6.disconnect_reconnect_bits,
                            _r)

        _mps.append(_r)

        result.update({'mode_pages': _mps})
        return result

    @classmethod
    def marshall_datain(cls, data):
        """
        Marshall the ModeSense6 datain.

        :param data: a dict with data
        :return result: a byte array
        """
        result = bytearray(4)
        encode_dict(data,
                    cls.MODESENSE6.mode_parameter_header_bits,
                    result)

        # mode page header
        for mp in data['mode_pages']:
            if not mp['spf']:
                _d = bytearray(2)
                encode_dict(mp,
                            cls.MODESENSE6.page_zero_bits,
                            _d)
            else:
                _d = bytearray(4)
                encode_dict(mp,
                            cls.MODESENSE6.sub_page_bits,
                            _d)

            if mp['page_code'] == cls.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
                _mpd = bytearray(18)
                encode_dict(mp,
                            cls.MODESENSE6.element_address_bits,
                            _mpd)
            if mp['page_code'] == cls.PAGE_CODE.CONTROL:
                if not mp['spf']:
                    _mpd = bytearray(10)
                    encode_dict(mp,
                                cls.MODESENSE6.control_bits,
                                _mpd)
                elif mp['sub_page_code'] == 1:
                    _mpd = bytearray(28)
                    encode_dict(mp,
                                cls.MODESENSE6.control_extension_1_bits,
                                _mpd)
            if mp['page_code'] == cls.PAGE_CODE.DISCONNECT_RECONNECT:
                if not mp['spf']:
                    _mpd = bytearray(14)
                    encode_dict(mp,
                                cls.MODESENSE6.disconnect_reconnect_bits,
                                _mpd)

            if not mp['spf']:
                _d[1] = len(_mpd)
            else:
                _d[2:4] = scsi_int_to_ba(len(_mpd), 2)

            result += _d
            result += _mpd

        result[0] = len(result) - 1
        return result


class ModeSelect6(SCSICommand):
    """
    A class to hold information from a modeselect6 command
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'pf': [0x10, 1],
                 'sp': [0x01, 1],
                 'parameter_list_length': [0xff, 4], }

    def __init__(self,
                 opcode,
                 data,
                 pf=1,
                 sp=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param data: a dict holding mode page to set
        :param pf: page format can be 0 or 1
        :param sp: save pages can be 0 or 1
        """
        _d = ModeSense6.marshall_datain(data)

        SCSICommand.__init__(self,
                             opcode,
                             len(_d),
                             0)
        self.dataout = _d
        self.cdb = self.build_cdb(pf=pf,
                                  opcode=self.opcode.value,
                                  sp=sp,
                                  parameter_list_length=len(_d))

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ModeSelect6 dataout.

        :param data: a byte array with data
        """
        return ModeSense6.unmarshall_dataout(data)

    @staticmethod
    def marshall_dataout(data):
        """
        Marshall the ModeSelect6 dataout.

        :param data: a dict with data
        :return result: a byte array
        """
        return ModeSense6.marshall_datain(data)

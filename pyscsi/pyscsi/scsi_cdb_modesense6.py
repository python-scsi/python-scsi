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
from pyscsi.pyscsi.scsi_enum_modesense import PAGE_CODE, MODESENSE6, MODESELECT6

#
# SCSI ModeSense6 command and definitions
#


class ModeSense6(SCSICommand):
    """
    A class to hold information from a modesense6 command
    """

    def __init__(self, scsi, page_code, sub_page_code=0, dbd=0, pc=0,
                 alloclen=96):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param page_code: the page code for the vpd page
        :param sub_page_code:
        :param dbd:
        :param pc:
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self.cdb = self.build_cdb(page_code, sub_page_code, dbd, pc,
                                  alloclen)
        self.execute()

    def build_cdb(self, page_code, sub_page_code, dbd, pc, alloclen):
        """
        """
        cdb = {'opcode': self.scsi.device.opcodes.MODE_SENSE_6.value,
               'dbd': dbd,
               'pc': pc,
               'page_code': page_code,
               'sub_page_code': sub_page_code,
               'alloc_len': alloclen, }

        return self.marshall_cdb(cdb)

    def unmarshall(self):
        """
        Unmarshall the ModeSense6 data.
        """
        self.result = self.unmarshall_datain(self.datain)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ModeSense6 datain.
        """
        result = {}
        _mps = []
        decode_bits(data[0:4], MODESENSE6.mode_parameter_header_bits, result)

        _bdl = data[3]
        block_descriptor = data[4:_bdl]

        data = data[4 + _bdl:]

        _r = {}
        if not data[0] & 0x40:
            decode_bits(data, MODESENSE6.page_zero_bits, _r)
            data = data[2:]
        else:
            decode_bits(data, MODESENSE6.sub_page_bits, _r)
            data = data[4:]

        if _r['page_code'] == PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
            decode_bits(data, MODESENSE6.element_address_bits, _r)
        if _r['page_code'] == PAGE_CODE.CONTROL:
            if not 'sub_page_code' in _r:
                decode_bits(data, MODESENSE6.control_bits, _r)
            elif _r['sub_page_code'] == 1:
                decode_bits(data, MODESENSE6.control_extension_1_bits, _r)
        if _r['page_code'] == PAGE_CODE.DISCONNECT_RECONNECT:
            if not 'sub_page_code' in _r:
                decode_bits(data, MODESENSE6.disconnect_reconnect_bits, _r)

        _mps.append(_r)

        result.update({'mode_pages': _mps})
        return result

    @staticmethod
    def marshall_datain(data):
        """
        Marshall the ModeSense6 datain.
        """
        result = bytearray(4)
        encode_dict(data, MODESENSE6.mode_parameter_header_bits, result)

        # mode page header
        for mp in data['mode_pages']:
            if not mp['spf']:
                _d = bytearray(2)
                encode_dict(mp, MODESENSE6.page_zero_bits, _d)
            else:
                _d = bytearray(4)
                encode_dict(mp, MODESENSE6.sub_page_bits, _d)

            if mp['page_code'] == PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
                _mpd = bytearray(18)
                encode_dict(mp, MODESENSE6.element_address_bits, _mpd)
            if mp['page_code'] == PAGE_CODE.CONTROL:
                if not mp['spf']:
                    _mpd = bytearray(10)
                    encode_dict(mp, MODESENSE6.control_bits, _mpd)
                elif mp['sub_page_code'] == 1:
                    _mpd = bytearray(28)
                    encode_dict(mp, MODESENSE6.control_extension_1_bits, _mpd)
            if mp['page_code'] == PAGE_CODE.DISCONNECT_RECONNECT:
                if not mp['spf']:
                    _mpd = bytearray(14)
                    encode_dict(mp, MODESENSE6.disconnect_reconnect_bits, _mpd)

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
        Unmarshall a ModeSense6 cdb
        """
        result = {}
        decode_bits(cdb, MODESENSE6.cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ModeSense6 cdb
        """
        result = bytearray(6)
        encode_dict(cdb, MODESENSE6.cdb_bits, result)
        return result


class ModeSelect6(SCSICommand):
    """
    A class to hold information from a modeselect6 command
    """
    def __init__(self, scsi, data, pf=1, sp=0):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param data: a dict holding mode page to set
        :param pf:
        :param sp:
        """
        _d = ModeSense6.marshall_datain(data)

        SCSICommand.__init__(self, scsi, len(_d), 0)
        self.dataout = _d
        self.cdb = self.build_cdb(pf, sp, len(_d))
        self.execute()

    def build_cdb(self, pf, sp, alloclen):
        """
        """
        cdb = {'opcode': self.scsi.device.opcodes.MODE_SELECT_6.value,
               'pf': pf,
               'sp': sp,
               'parameter_list_length': alloclen, }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ModeSelect6 dataout.
        """
        return ModeSense6.unmarshall_dataout(data)

    @staticmethod
    def marshall_dataout(data):
        """
        Marshall the ModeSelect6 dataout.
        """
        return ModeSense6.marshall_datain(data)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ModeSelect6 cdb
        """
        result = {}
        decode_bits(cdb, MODESELECT6.modeselect6_cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ModeSelect6 cdb
        """
        result = bytearray(6)
        encode_dict(cdb, MODESELECT6.modeselect6_cdb_bits, result)
        return result

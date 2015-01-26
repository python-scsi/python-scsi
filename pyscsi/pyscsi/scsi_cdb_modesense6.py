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

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, encode_dict, decode_bits
import scsi_enum_modesense6 as modesensense_enums

#
# SCSI ModeSense6 command and definitions
#


class ModeSense6(SCSICommand):
    """
    A class to hold information from a modesense6 command
    """
    _cdb_bits = {
        'opcode': [0xff, 0],
        'dbd': [0x08, 1],
        'pc': [0xc0, 2],
        'page_code': [0x3f, 2],
        'sub_page_code': [0xff, 3],
        'alloc_len': [0xff, 4]
    }
    _mode_parameter_header_bits = {
        'medium_type': [0xff, 1],
        'device_specific_parameter': [0xff, 2],
    }
    _page_zero_bits = {
        'ps': [0x80, 0],
        'spf': [0x40, 0],
        'page_code': [0x3f, 0],
    }
    _sub_page_bits = {
        'ps': [0x80, 0],
        'spf': [0x40, 0],
        'page_code': [0x3f, 0],
        'sub_page_code': [0xff, 1],
    }
    _element_address_bits = {
        'first_medium_transport_element_address': [0xffff, 0],
        'num_medium_transport_elements': [0xffff, 2],
        'first_storage_element_address': [0xffff, 4],
        'num_storage_elements': [0xffff, 6],
        'first_import_element_address': [0xffff, 8],
        'num_import_elements': [0xffff, 10],
        'first_data_transfer_element_address': [0xffff, 12],
        'num_data_transfer_elements': [0xffff, 14],
    }
    _control_bits = {
        'tst': [0xe0, 0],
        'tmf_only': [0x10, 0],
        'dpicz': [0x08, 0],
        'd_sense': [0x04, 0],
        'gltsd': [0x02, 0],
        'rlec': [0x01, 0],
        'queue_algorithm_modifier': [0xf0, 1],
        'nuar': [0x08, 1],
        'qerr': [0x06, 1],
        'vs': [0x80, 2],
        'rac': [0x40, 2],
        'ua_intlck_ctrl': [0x30, 2],
        'swp': [0x08, 2],
        'ato': [0x80, 3],
        'tas': [0x40, 3],
        'atmpe': [0x20, 3],
        'rwwp': [0x10, 3],
        'autoload_mode': [0x07, 3],
        'busy_timeout_period': [0xffff, 6],
        'extended_self_test_completion_time': [0xffff, 8],
    }

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
               'alloc_len': alloclen
        }
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
        decode_bits(data[0:4], ModeSense6._mode_parameter_header_bits, result)

        _bdl = data[3]
        block_descriptor = data[4:_bdl]

        data = data[4 + _bdl:]

        _r = {}
        if not data[0] & 0x40:
            decode_bits(data, ModeSense6._page_zero_bits, _r)
            data = data[2:]
        else:
            decode_bits(data, ModeSense6._sub_page_bits, _r)
            data = data[4:]

        if _r['page_code'] == modesensense_enums.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
            decode_bits(data, ModeSense6._element_address_bits, _r)
        if _r['page_code'] == modesensense_enums.PAGE_CODE.CONTROL:
            decode_bits(data, ModeSense6._control_bits, _r)
        _mps.append(_r)

        result.update({'mode_pages': _mps})
        return result

    @staticmethod
    def marshall_datain(data):
        """
        Marshall the ModeSense6 datain.
        """
        result = bytearray(4)
        encode_dict(data, ModeSense6._mode_parameter_header_bits, result)

        # mode page header
        for mp in data['mode_pages']:
            if mp['page_code'] == modesensense_enums.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
                _mpd = bytearray(18)
                encode_dict(mp, ModeSense6._element_address_bits, _mpd)
            if mp['page_code'] == modesensense_enums.PAGE_CODE.CONTROL:
                _mpd = bytearray(10)
                encode_dict(mp, ModeSense6._control_bits, _mpd)

            if not mp['spf']:
                _d = bytearray(2)
                encode_dict(mp, ModeSense6._page_zero_bits, _d)
                _d[1] = len(_mpd)
            else:
                _d = bytearray(4)
                encode_dict(mp, ModeSense6._sub_page_bits, _d)
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
        decode_bits(cdb, ModeSense6._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ModeSense6 cdb
        """
        result = bytearray(6)
        encode_dict(cdb, ModeSense6._cdb_bits, result)
        return result

class ModeSelect6(SCSICommand):
    """
    A class to hold information from a modeselect6 command
    """
    _cdb_bits = {
        'opcode': [0xff, 0],
        'pf': [0x10, 1],
        'sp': [0x01, 1],
        'parameter_list_length': [0xff, 4]
    }

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
               'parameter_list_length': alloclen
        }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ModeSelect6 dataout.
        """
        return ModeSense6.unmarshall_datain(data)

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
        decode_bits(cdb, ModeSelect6._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ModeSelect6 cdb
        """
        result = bytearray(6)
        encode_dict(cdb, ModeSelect6._cdb_bits, result)
        return result

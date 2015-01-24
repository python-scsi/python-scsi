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
from pyscsi.utils.converter import scsi_int_to_ba, scsi_ba_to_int, encode_dict, decode_bits
import scsi_enum_readelementstatus as readelementstatus_enums

#
# SCSI ReadElementStatus command and definitions
#


class ReadElementStatus(SCSICommand):
    """
    A class to hold information from a readelementstatus command
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'voltag': [0x10, 1],
                 'element_type': [0x07, 1],
                 'starting_element_address': [0xffff, 2],
                 'num_elements': [0xffff, 4],
                 'curdata': [0x02, 6],
                 'dvcid': [0x01, 6],
                 'alloc_len': [0xffffff, 7]
    }

    def __init__(self, scsi, start, num, element_type=readelementstatus_enums.ELEMENT_TYPE.ALL,
                 voltag=0, curdata=1, dvcid=0, alloclen=16384):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param start: first element to return
        :param num: number of elements to return
        :param element_type: type of element to return data for
        :param voltag
        :param curdata
        :param dvcid
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self.cdb = self.build_cdb(start, num, element_type, voltag, curdata,
                                  dvcid, alloclen)
        self.execute()

    def build_cdb(self, start, num, element_type,
                  voltag, curdata, dvcid, alloclen):
        """
        Build a ReadElementStatus CDB
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.READ_ELEMENT_STATUS.value,
            'voltag': voltag,
            'element_type': element_type,
            'starting_element_address': start,
            'num_elements': num,
            'curdata': curdata,
            'dvcid': dvcid,
            'alloc_len': alloclen
        }
        return self.marshall_cdb(cdb)

    #
    # Unmarshall a SMC Storage Element Descriptor as per SMC 6.11.5
    #
    def unmarshall_element_descriptor(self, element_type, data, pvoltag, avoltag):
        _storage = {}
        _bits = {'element_address': [0xffff, 0],
                 'access': [0x08, 2],
                 'except': [0x04, 2],
                 'full': [0x01, 2],
                 'additional_sense_code': [0xff, 4],
                 'additional_sense_code_qualifier': [0xff, 5],
                 'svalid': [0x80, 9],
                 'invert': [0x40, 9],
                 'ed': [0x08, 9],
                 'medium_type': [0x07, 9],
                 'source_storage_element_address': [0xffff, 10], }
        decode_bits(data, _bits, _storage)

        _data = data[12:]
        if pvoltag:
            _storage.update({'primary_volume_tag': _data[0:36]})
            _data = _data[36:]
        if avoltag:
            _storage.update({'alternate_volume_tag': _data[0:36]})
            _data = _data[36:]
        _bits = {'code_set': [0x0f, 0],
                 'identifier_type': [0x0f, 1],
                 'identifier_length': [0xff, 3], }
        decode_bits(_data, _bits, _storage)
        if _storage['identifier_length']:
            _storage.update({'identifier': _data[4:4 + _storage['identifier_length']]})
        return _storage

    #
    # Unmarshall Element Status Page as per SMC 6.11.3
    #
    def unmarshall_element_status_page(self, data):
        _status = {}
        _type = data[0] & 0x0f
        _status['element_type'] = _type
        _pvoltag = (data[1] >> 7) & 0x01
        _status['pvoltag'] = _pvoltag
        _avoltag = (data[1] >> 6) & 0x01
        _status['avoltag'] = _avoltag
        _edl = scsi_ba_to_int(data[2:4])

        #
        # Element Descriptors
        #
        _data = data[8:]
        _e = []
        while len(_data):
            _e.append(self.unmarshall_element_descriptor(_type, _data[:_edl],
                                                         _pvoltag, _avoltag))

            _data = _data[_edl:]

        if len(_e):
            _status['element_descriptors'] = _e

        return _type, _status

    def unmarshall(self):
        """
        """
        _bits = {'first_element_address': [0xffff, 0],
                 'num_elements': [0xffff, 2],
                 'byte_count': [0xffffff, 5], }
        decode_bits(self.datain, _bits, self.result)

        #
        # Loop over the remaining data until we have consumed all
        # element status pages
        #
        _data = self.datain[8:8 + self.result['byte_count']]
        while len(_data):
            _bytes = scsi_ba_to_int(_data[5:8])

            _type, _descriptors = self.unmarshall_element_status_page(
                _data[:8 + _bytes])

            if _type == readelementstatus_enums.ELEMENT_TYPE.MEDIUM_TRANSPORT:
                self.result.update({'medium_transport_elements': _descriptors})

            if _type == readelementstatus_enums.ELEMENT_TYPE.STORAGE:
                self.result.update({'storage_elements': _descriptors})

            if _type == readelementstatus_enums.ELEMENT_TYPE.IMPORT_EXPORT:
                self.result.update({'import_export_elements': _descriptors})

            if _type == readelementstatus_enums.ELEMENT_TYPE.DATA_TRANSFER:
                self.result.update({'data_transfer_elements': _descriptors})

            _data = _data[8 + _bytes:]

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ReadElementStatus cdb
        """
        result = {}
        decode_bits(cdb, ReadElementStatus._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ReadElementStatus cdb
        """
        result = bytearray(12)
        encode_dict(cdb, ReadElementStatus._cdb_bits, result)
        return result

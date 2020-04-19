# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import pyscsi.pyscsi.scsi_enum_readelementstatus as readelementstatus_enums
from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import (
    decode_bits,
    encode_dict,
    scsi_ba_to_int,
    scsi_int_to_ba,
)

#
# SCSI ReadElementStatus command and definitions
#

# we get a generator for all inquiry enums, so we can add them to the class
_enums = ((key, readelementstatus_enums.__dict__[key])
          for key in readelementstatus_enums.__dict__.keys()
          if key in readelementstatus_enums.__all__)


class ReadElementStatus(SCSICommand):
    """
    A class to hold information from a readelementstatus command
    """
    _cdb_bits =                       {'opcode': [0xff, 0],
                                       'voltag': [0x10, 1],
                                       'element_type': [0x07, 1],
                                       'starting_element_address': [0xffff, 2],
                                       'num_elements': [0xffff, 4],
                                       'curdata': [0x02, 6],
                                       'dvcid': [0x01, 6],
                                       'alloc_len': [0xffffff, 7], }

    _datain_bits =                    {'first_element_address': [0xffff, 0],
                                       'num_elements': [0xffff, 2], }

    _element_status_page_bits =       {'element_type': [0x0f, 0],
                                       'pvoltag': [0x80, 1],
                                       'avoltag': [0x40, 1], }

    _element_status_descriptor_bits = {'element_address': [0xffff, 0],
                                       'except': [0x04, 2],
                                       'full': [0x01, 2],
                                       'additional_sense_code': [0xff, 4],
                                       'additional_sense_code_qualifier': [0xff, 5],
                                       'svalid': [0x80, 9],
                                       'invert': [0x40, 9],
                                       'ed': [0x08, 9],
                                       'medium_type': [0x07, 9],
                                       'source_storage_element_address': [0xffff, 10], }

    _data_transfer_descriptor_bits =  {'access': [0x08, 2], }

    _storage_descriptor_bits =        {'access': [0x08, 2], }

    _import_export_descriptor_bits =  {'oir': [0x80, 2],
                                       'cmc': [0x40, 2],
                                       'inenab': [0x20, 2],
                                       'exenab': [0x10, 2],
                                       'access': [0x08, 2],
                                       'impexp': [0x02, 2], }

    # HACK: we update the baseclass with enums for the subclass, if there is a better way
    #       to add this to the subclass we should use it instead :-)
    for enum in _enums:
        setattr(SCSICommand, enum[0], enum[1])

    def __init__(self,
                 opcode,
                 start,
                 num,
                 element_type=readelementstatus_enums.ELEMENT_TYPE.ALL,
                 voltag=0,
                 curdata=1,
                 dvcid=0,
                 alloclen=16384):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param start: first element to return
        :param num: number of elements to return
        :param element_type: type of element to return data for
        :param voltag: volume tag, can have a value of 0 or 1
        :param curdata: current data, can have a value of 0 or 1
        :param dvcid: device id, can have a value of 0 or 1
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  voltag=voltag,
                                  element_type=element_type,
                                  starting_element_address=start,
                                  num_elements=num,
                                  curdata=curdata,
                                  dvcid=dvcid,
                                  alloc_len=alloclen)

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the ReadElementStatus datain buffer.

        :param data: a byte array
        :return result: a dict
        """
        result = {}
        _esd = []
        decode_bits(data,
                    cls._datain_bits,
                    result)

        #
        # Loop over the remaining data until we have consumed all
        # element status pages
        #
        _bc = scsi_ba_to_int(data[5:8])
        data = data[8:8 + _bc]
        while len(data):
            _r = {}
            _bc = scsi_ba_to_int(data[5:8])
            _edl = scsi_ba_to_int(data[2:4])

            decode_bits(data,
                        cls._element_status_page_bits,
                        _r)
            _d = data[8:8 + _bc]
            _ed = []
            while len(_d):
                _rr = {}

                decode_bits(_d,
                            cls._element_status_descriptor_bits,
                            _rr)
                _dd = _d[12:]
                if _r['pvoltag']:
                    _rr.update({'primary_volume_tag': _dd[0:36]})
                    _dd = _dd[36:]
                if _r['avoltag']:
                    _rr.update({'alternate_volume_tag': _dd[0:36]})
                    _dd = _dd[36:]  # this is not going to used again so we may just delete it?

                if _r['element_type'] == cls.ELEMENT_TYPE.DATA_TRANSFER:
                    decode_bits(_d,
                                cls._data_transfer_descriptor_bits,
                                _rr)
                if _r['element_type'] == cls.ELEMENT_TYPE.STORAGE:
                    decode_bits(_d,
                                cls._storage_descriptor_bits,
                                _rr)
                if _r['element_type'] == cls.ELEMENT_TYPE.IMPORT_EXPORT:
                    decode_bits(_d,
                                cls._import_export_descriptor_bits,
                                _rr)
                _ed.append(_rr)
                _d = _d[_edl:]
            _r.update({'element_descriptors': _ed})
            _esd.append(_r)
            data = data[8 + _bc:]
        result.update({'element_status_pages': _esd})
        return result

    @classmethod
    def marshall_datain(cls, data):
        """
        Marshall the ReadCapacity16 datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(8)
        encode_dict(data,
                    cls._datain_bits,
                    result)

        for _esp in data['element_status_pages']:
            _r = bytearray(8)
            encode_dict(_esp,
                        cls._element_status_page_bits,
                        _r)

            _edl = 12 + 4
            if _esp['pvoltag']:
                _edl += 36
            if _esp['avoltag']:
                _edl += 36

            for _ed in _esp['element_descriptors']:
                _rr = bytearray(12)
                encode_dict(_ed,
                            cls._element_status_descriptor_bits,
                            _rr)
                if _esp['element_type'] == cls.ELEMENT_TYPE.DATA_TRANSFER:
                    encode_dict(_ed,
                                cls._data_transfer_descriptor_bits,
                                _rr)
                if _esp['element_type'] == cls.ELEMENT_TYPE.STORAGE:
                    encode_dict(_ed,
                                cls._storage_descriptor_bits,
                                _rr)
                if _esp['element_type'] == cls.ELEMENT_TYPE.IMPORT_EXPORT:
                    encode_dict(_ed,
                                cls._import_export_descriptor_bits,
                                _rr)
                _r += _rr
                if _esp['pvoltag']:
                    _rr = bytearray(36)
                    _r += _rr
                if _esp['avoltag']:
                    _rr = bytearray(36)
                    _r += _rr
                _rr = bytearray(4)
                _r += _rr

            _r[2:4] = scsi_int_to_ba(_edl, 2)
            _r[5:8] = scsi_int_to_ba(len(_r) - 8, 3)
            result += _r

        result[5:8] = scsi_int_to_ba(len(result) - 8, 3)
        return result

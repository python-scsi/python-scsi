# coding: utf-8

from scsi_command import SCSICommand, OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int
from sgio.utils.enum import Enum

#
# SCSI ReadElementStatus command and definitions
#

#
# qqq
#
header_bits = {'ps': [0x80, 0],
               'spf': [0x40, 0],
               'page_code': [0x3f, 0],
               'parameter_list_length': [0xff, 1], }

#
# Element Type Code
#
element_type = {'ALL': 0x00,
                'MEDIUM_TRANSPORT': 0x01,
                'STORAGE': 0x02,
                'IMPORT_EXPORT': 0x03,
                'DATA_TRANSFER': 0x04, }

ELEMENT_TYPE = Enum(element_type)

class ReadElementStatus(SCSICommand):
    """
    A class to hold information from a readelementstatus command
    """

    def __init__(self, scsi, start, num, element_type=ELEMENT_TYPE.ALL,
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
        """
        cdb = SCSICommand.init_cdb(OPCODE.READ_ELEMENT_STATUS)
        if voltag:
            cdb[1] |= 0x10
        cdb[1] |= element_type & 0x0f
        cdb[2:4] = scsi_int_to_ba(start, 2);
        cdb[4:6] = scsi_int_to_ba(num, 2);
        if curdata:
            cdb[6] |= 0x02
        if dvcid:
            cdb[6] |= 0x01
        cdb[7:10] = scsi_int_to_ba(alloclen, 3);
        return cdb

    #
    # Unmarshall a SMC Storage Element Descriptor as per SMC 6.11.5
    #
    def unmarshall_element_descriptor(self, type, data, pvoltag, avoltag):
        _storage = {}
        _storage['element_address'] = scsi_ba_to_int(data[0:2])
        _storage['access'] = (data[2] >> 3) & 0x01
        _storage['except'] = (data[2] >> 2) & 0x01
        _storage['full'] = (data[2]) & 0x01
        _storage['additional_sense_code'] = data[4]
        _storage['additional_sense_code_qualifier'] = data[5]
        _storage['svalid'] = (data[9] >> 7) & 0x01
        _storage['invert'] = (data[9] >> 6) & 0x01
        _storage['ed'] = (data[9] >> 3) & 0x01
        _storage['medium_type'] = data[9] & 0x07
        _storage['source_storage_element_address'] = scsi_ba_to_int(data[10:12])

        _data = data[12:]
        if pvoltag:
            _storage['primary_volume_tag'] = _data[0:36]
            _data = _data[36:]
        if avoltag:
            _storage['alternate_volume_tag'] = _data[0:36]
            _data = _data[36:]

        _storage['code_set'] = _data[0] & 0x0f
        _storage['identifier_type'] = _data[1] & 0x0f
        _il = data[3]
        _storage['identifier_length'] = _il
        if _il:
            _storage['identifier'] = _data[4:_il]
            
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
        _first = scsi_ba_to_int(self.datain[0:2])
        self.add_result('first_element_address', _first)

        _num = scsi_ba_to_int(self.datain[2:4])
        self.add_result('num_elements', _num)

        _bytes = scsi_ba_to_int(self.datain[5:8])
        self.add_result('byte_count', _bytes)

        #
        # Loop over the remaining data until we have consumed all
        # element status pages
        #
        _data = self.datain[8:8 + _bytes]
        while len(_data):
            _bytes = scsi_ba_to_int(_data[5:8])

            _type, _descriptors = self.unmarshall_element_status_page(
                _data[:8 + _bytes])

            if _type == ELEMENT_TYPE.STORAGE:
                self.add_result('storage_elements', _descriptors)

            if _type == ELEMENT_TYPE.DATA_TRANSFER:
                self.add_result('data_transfer_elements', _descriptors)

            _data = _data[8 + _bytes:]

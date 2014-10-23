# coding: utf-8

from scsi_command import SCSICommand, OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int, decode_bits
from sgio.utils.enum import Enum

#
# SCSI ReadElementStatus command and definitions
#

#
# Element Status Data
#
element_status_data_bits = {
        'first_element_address': [0xffff, 0],
        'num_elements': [0xffff, 2],
        'byte_count': [0xffffff, 5],
}

#
# Element Descriptor bits
#
element_descriptor_bits = {
    'element_address': [0xffff, 0],
    'access': [0x08, 2],
    'except': [0x04, 2],
    'full': [0x01, 2],
    'additional_sense_code': [0xff, 4],
    'additional_sense_code_qualifier': [0xff, 5],
    'svalid': [0x80, 9],
    'invert': [0x40, 9],
    'ed': [0x08, 9],
    'medium_type': [0x07, 9],
    'source_storage_element_address': [0xffff, 10],
}

element_descriptor_trailer_bits = {
    'code_set': [0x0f, 0],
    'identifier_type':  [0x0f, 1],
    'identifier_length': [0xff, 3],
}

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
        decode_bits(data, element_descriptor_bits, _storage)

        _data = data[12:]
        if pvoltag:
            self.add_result_to_dict('primary_volume_tag',
                                    _data[0:36], _storage)
            _data = _data[36:]
        if avoltag:
            self.add_result_to_dict('alternate_volume_tag',
                                    _data[0:36], _storage)
            _data = _data[36:]

        decode_bits(_data, element_descriptor_trailer_bits, _storage)
        if _storage['identifier_length']:
            self.add_result_to_dict('identifier',
                                    _data[4:4 + _storage['identifier_length']],
                                    _storage)
            
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
        decode_bits(self.datain, element_status_data_bits, self.result)

        #
        # Loop over the remaining data until we have consumed all
        # element status pages
        #
        _data = self.datain[8:8 + self.result['byte_count']]
        while len(_data):
            _bytes = scsi_ba_to_int(_data[5:8])

            _type, _descriptors = self.unmarshall_element_status_page(
                _data[:8 + _bytes])

            if _type == ELEMENT_TYPE.MEDIUM_TRANSPORT:
                self.add_result('medium_transport_elements', _descriptors)

            if _type == ELEMENT_TYPE.STORAGE:
                self.add_result('storage_elements', _descriptors)

            if _type == ELEMENT_TYPE.IMPORT_EXPORT:
                self.add_result('import_export_elements', _descriptors)

            if _type == ELEMENT_TYPE.DATA_TRANSFER:
                self.add_result('data_transfer_elements', _descriptors)

            _data = _data[8 + _bytes:]

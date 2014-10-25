# coding: utf-8

from sgio.utils.enum import Enum

#
# CDB
#
cdb_bits = {
    'opcode': [0xff, 0],
    'voltag': [0x10, 1],
    'element_type': [0x07, 1],
    'starting_element_address': [0xffff, 2],
    'num_elements': [0xffff, 4],
    'curdata': [0x02, 6],
    'dvcid': [0x01, 6],
    'alloc_len': [0xffffff, 7],
}

#
# Element Status Data
#
element_status_data_bits = {'first_element_address': [0xffff, 0],
                            'num_elements': [0xffff, 2],
                            'byte_count': [0xffffff, 5], }

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
    'source_storage_element_address': [0xffff, 10], }

element_descriptor_trailer_bits = {
    'code_set': [0x0f, 0],
    'identifier_type': [0x0f, 1],
    'identifier_length': [0xff, 3],
}

#
# Element Type Code
#
_element_type = {
    'ALL': 0x00,
    'MEDIUM_TRANSPORT': 0x01,
    'STORAGE': 0x02,
    'IMPORT_EXPORT': 0x03,
    'DATA_TRANSFER': 0x04,
}

ELEMENT_TYPE = Enum(_element_type)

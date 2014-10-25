# coding: utf-8

from sgio.utils.enum import Enum


#
# CDB
#
cdb_bits = {
    'opcode': [0xff, 0],
    'dbd': [0x08, 1],
    'pc': [0xc0, 2],
    'page_code': [0x3f, 2],
    'sub_page_code': [0xff, 3],
    'alloc_len': [0xff, 4],
}

#
# Mode Header
#
mode_header_bits = {
    'mode_data_length': [0xff, 0],
    'medium_type': [0xff, 1],
    'device_specific_parameter': [0xff, 2],
    'block_descriptor_length': [0xff, 3],
}

#
# Element Address Assignment
#
element_address_assignment_bits = {
    'first_medium_transport_element_address': [0xffff, 2],
    'num_medium_transport_elements': [0xffff, 4],
    'first_storage_element_address': [0xffff, 6],
    'num_storage_elements': [0xffff, 8],
    'first_import_element_address': [0xffff, 10],
    'num_import_elements': [0xffff, 12],
    'first_data_transfer_element_address': [0xffff, 14],
    'num_data_transfer_elements': [0xffff, 16],
}

#
# Page Header
#
page_header_bits = {
    'ps': [0x80, 0],
    'spf': [0x40, 0],
    'page_code': [0x3f, 0],
    'parameter_list_length': [0xff, 1],
}

#
# Page Control
#
_pc = {
    'CURRENT': 0x00,
    'CHANGEABLE': 0x01,
    'DEFAULT': 0x02,
    'SAVED': 0x03,
}

PC = Enum(_pc)

#
# Page Codes
#

_page_code = {'ELEMENT_ADDRESS_ASSIGNMENT': 0x1d, }

PAGE_CODE = Enum(_page_code)

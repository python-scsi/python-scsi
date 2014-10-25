# coding: utf-8

from sgio.utils.enum import Enum

#
# CDB
#
cdb_bits = {
    'opcode': [0xff, 0],
    'service_action': [0x1f, 1],
    'alloc_len': [0xffffffff, 10],
}

readcapacity16_bits = {
    'returned_lba': [0xffffffffffffffff, 0],
    'block_length': [0xffffffff, 8],
    'p_type': [0x0e, 12],
    'prot_en': [0x01, 12],
    'p_i_exponent': [0xf0, 13],
    'lbppbe': [0x0f, 13],
    'lbpme': [0x80, 14],
    'lbprz': [0x40, 14],
    'lowest_aligned_lba': [0x3fff, 14],
}

#
# P_TYPE
#
_p_types = {
    'TYPE_1_PROTECTION': 0x00,
    'TYPE_2_PROTECTION': 0x01,
    'TYPE_3_PROTECTION': 0x02,
}

P_TYPE = Enum(_p_types)
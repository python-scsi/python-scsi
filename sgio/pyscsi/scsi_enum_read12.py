# coding: utf-8

#
# CDB
#
cdb_bits = {
    'opcode': [0xff, 0],
    'rdprotect': [0xe0, 1],
    'dpo': [0x10, 1],
    'fua': [0x08, 1],
    'rarc': [0x04, 1],
    'lba': [0xffffffff, 2],
    'tl': [0xffffffff, 6],
    'group': [0x1f, 10],
}
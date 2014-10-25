# coding: utf-8

#
# CDB
#
cdb_bits = {
    'opcode': [0xff, 0],
}

readcapacity10_bits = {
    'returned_lba': [0xffffffff, 0],
    'block_length': [0xffffffff, 4],
}

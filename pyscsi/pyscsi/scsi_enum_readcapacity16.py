# coding: utf-8

from pyscsi.utils.enum import Enum

#
# P_TYPE
#
_p_types = {
    'TYPE_1_PROTECTION': 0x00,
    'TYPE_2_PROTECTION': 0x01,
    'TYPE_3_PROTECTION': 0x02,
}

P_TYPE = Enum(_p_types)
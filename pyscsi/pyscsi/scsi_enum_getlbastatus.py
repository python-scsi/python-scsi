# coding: utf-8

from pyscsi.utils.enum import Enum

#
# P_STATUS
#
_p_status = {
    'MAPPED': 0x00,
    'DEALLOCATED': 0x01,
    'ANCHORED': 0x02,
}

P_STATUS = Enum(_p_status)

# coding: utf-8

from pyscsi.utils.enum import Enum

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

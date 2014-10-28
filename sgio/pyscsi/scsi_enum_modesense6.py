# coding: utf-8

from sgio.utils.enum import Enum

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

# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

__all__ = ['ELEMENT_TYPE', ]

from pyscsi.utils.enum import Enum

#
# Element Type Code
#
_element_type = {'ALL': 0x00,
                 'MEDIUM_TRANSPORT': 0x01,
                 'STORAGE': 0x02,
                 'IMPORT_EXPORT': 0x03,
                 'DATA_TRANSFER': 0x04, }

ELEMENT_TYPE = Enum(_element_type)

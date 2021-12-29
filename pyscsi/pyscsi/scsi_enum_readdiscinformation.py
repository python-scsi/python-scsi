# coding: utf-8

# Copyright (C) 2021 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2021 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.utils.enum import Enum

__all__ = ['DISC_INFORMATION_DATA_TYPE', 'STATE_OF_LAST_SESSION',
           'DISC_STATUS', 'DISC_TYPE']

disc_information_data_type = {'STANDARD_DISC_INFORMATION': 0x00,
                              'TRACK_RESOURCES_INFORMATION': 0x01,
                              'POW_RESOURCES_DISC_INFORMATION': 0x02,
                              }
state_of_last_session = {'EMPTY_SESSION': 0x00,
                         'INCOMPLETE_SESSION': 0x01,
                         'DAMAGED_SESSION': 0x02,
                         'COMPLETE_SESSION': 0x03
               }

disc_status = {'EMPTY_DISC': 0x00,
               'INCOMPLETE_DISC': 0x01,
               'FINALIZED_DISC': 0x02,
               'OTHERS': 0x03, }

disc_type = {'CD-DA or CD-ROM': 0x00,
             'CD-I': 0x10,
             'CD-ROM XA': 0x20,
             'UNDEFINED': 0xFF,
             }
DISC_INFORMATION_DATA_TYPE = Enum(disc_information_data_type)
STATE_OF_LAST_SESSION = Enum(state_of_last_session)
DISC_STATUS = Enum(disc_status)
DISC_TYPE = Enum(disc_type)

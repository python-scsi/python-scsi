# SPDX-FileCopyrightText: 2022 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8


from pyscsi.utils.enum import Enum

#
# EXPECTED_SECTOR_TYPE
#
_expected_sector_type = {'CDDA': 1,
                         'MODE_1': 2,
                         'MODE_2_FORMLESS': 3,
                         'MODE_2_FORM_1': 4,
                         'MODE_2_FORM_2': 5, }

EXPECTED_SECTOR_TYPE = Enum(_expected_sector_type)

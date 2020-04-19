#!/usr/bin/env python

# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

#
# A simple example to get a dict with reported luns
#
import sys

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.utils import init_device


def main(device):
    with SCSI(device) as s:
        s.testunitready()
        print ('ReportPriority')
        print ('==========================================\n')
        r = s.reportpriority().result
        for k, v in r.items():
            print('%s - %s' % (k, v))


if __name__ == "__main__":
    main(init_device(sys.argv[1]))

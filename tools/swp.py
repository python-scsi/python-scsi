#!/usr/bin/env python

# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

#
# A simple example to show/set/clear the software write protect flag SWP
#
import sys

from pyscsi.pyscsi import scsi_enum_modesense as MODESENSE6
from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_device import SCSIDevice
from pyscsi.utils import init_device


def usage():
    print('Usage: swp.py [--help] [--on|--off] <device>')


def main():
    swp_on = 0
    swp_off = 0
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--help':
            return usage()
        if sys.argv[i] == '--on':
            del sys.argv[i]
            swp_on = 1
            continue
        if sys.argv[i] == '--off':
            del sys.argv[i]
            swp_off = 1
            continue
        i += 1

    if len(sys.argv) < 2:
        return usage()

    device = sys.argv[1]

    sd = init_device(device)
    s = SCSI(sd)
    i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.CONTROL).result

    if swp_on:
        i['mode_pages'][0]['swp'] = 1
        s.modeselect6(i)
        print('Set SWP ON')
        return

    if swp_off:
        i['mode_pages'][0]['swp'] = 0
        s.modeselect6(i)
        print('Set SWP OFF')
        return

    print('SWP is %s' % ("ON" if i['mode_pages'][0]['swp'] else "OFF"))


if __name__ == "__main__":
    main()

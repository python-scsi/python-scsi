#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

import sys

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_sense import SCSICheckCondition
from pyscsi.utils import init_device


def usage():
    print("Usage: read_disc_information.py <device>")


def pe(cmd, res, name):
    e = getattr(cmd, name)
    print(name + ": %s (%d)" % (e[res[name.lower()]], res[name.lower()]))


def pi(res, name):
    print(name + ": %d" % (res[name.lower()]))


def main():
    i = 1
    data_type = 0

    while i < len(sys.argv):
        if sys.argv[i] == "--help":
            return usage()
        if sys.argv[i] == "--data-type":
            del sys.argv[i]
            if sys.argv[i][:2] == "0x":
                data_type = int(sys.argv[i], 16)
            else:
                data_type = int(sys.argv[i], 10)
            del sys.argv[i]
            continue
        i += 1

    if len(sys.argv) < 2:
        return usage()

    device = init_device(sys.argv[1])

    with SCSI(device) as s:
        try:
            s.testunitready()

            cmd = s.readdiscinformation(data_type, alloc_len=512)
            i = cmd.result
            pe(cmd, i, "DISC_INFORMATION_DATA_TYPE")
            if (
                i["disc_information_data_type"]
                == cmd.DISC_INFORMATION_DATA_TYPE.STANDARD_DISC_INFORMATION
            ):
                pi(i, "ERASABLE")
                pe(cmd, i, "STATE_OF_LAST_SESSION")
                pe(cmd, i, "DISC_STATUS")
                pi(i, "NUMBER_OF_FIRST_TRACK_ON_DISC")
                pi(i, "NUMBER_OF_SESSIONS")
                pi(i, "FIRST_TRACK_NUMBER_IN_LAST_SESSION")
                pi(i, "LAST_TRACK_NUMBER_IN_LAST_SESSION")
                pi(i, "DID_V")
                pi(i, "DBC_V")
                pi(i, "URU")
                pi(i, "DAC_V")
                pi(i, "LEGACY")
                pi(i, "BG_FORMAT_STATUS")
                pe(cmd, i, "DISC_TYPE")
                pi(i, "DISC_IDENTIFICATION")
                print(
                    "LAST_SESSION_LEAD_IN_START_ADDRESS",
                    i["last_session_lead_in_start_address"],
                )
                print(
                    "LAST_POSSIBLE_LEAD_OUT_START_ADDRESS",
                    i["last_possible_lead_out_start_address"],
                )
                print("DISC_BAR_CODE", i["disc_bar_code"])
            else:
                for k, v in i.items():
                    print("%s - %s" % (k, v))

        except SCSICheckCondition as ex:
            # if you want a print out of the sense data dict uncomment the next line
            # ex.show_data = True
            print(ex)


if __name__ == "__main__":
    main()

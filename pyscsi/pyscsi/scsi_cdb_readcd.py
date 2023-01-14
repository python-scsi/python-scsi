# coding: utf-8

# Copyright (C) 2021 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import pyscsi.utils.converter as convert
from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.pyscsi.scsi_enum_readcd import EXPECTED_SECTOR_TYPE

#
# SCSI ReadCd command and definitions
#


class ReadCd(SCSICommand):
    """
    A class to hold information from a ReadCd command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
        "est": [0x1C, 1],
        "dap": [0x02, 1],
        "lba": [0xFFFFFFFF, 2],
        "tl": [0xFFFFFF, 6],
        "mcsb": [0xF8, 9],
        "c2ei": [0x06, 9],
        "scsb": [0x07, 10],
    }
    # SubChannel type 2 bits
    _sc2_bits = {
        "c": [0xF0, 0],
        "adr": [0x0F, 0],
        "track-number": [0xFF, 1],
        "index-number": [0xFF, 2],
        "min": [0xFF, 3],
        "sec": [0xFF, 4],
        "frame": [0xFF, 5],
        "zero": [0xFF, 6],
        "amin": [0xFF, 7],
        "asec": [0xFF, 8],
        "aframe": [0xFF, 9],
        "crc": [0xFFFF, 10],
        "p": [0x80, 15],
    }
    # SectorHeader
    _sh_bits = {
        "minute": [0xFF, 0],
        "second": [0xFF, 1],
        "frame": [0xFF, 2],
        "mode": [0xFF, 3],
    }

    def __init__(self, opcode, lba=0, tl=0, est=0, dap=0, mcsb=0, c2ei=0, scsb=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param lba: Logical Block Address
        :param tl: transfer length
        :param est=0: Expected Sector Type
        :param dap=0: Digital Audio Play
        :param mcsb=0: Main Channel Selection Bits
        :param c2e1=0: C2 Error Information
        :param scsb=0: Sub-Channel Selection Bits
        """

        # dont bother to compute the exact allocation length needed, just use
        # 3kb per lba
        SCSICommand.__init__(self, opcode, 0, tl * 3072)

        self.cdb = self.build_cdb(
            opcode=self.opcode.value,
            lba=lba,
            tl=tl,
            est=est,
            dap=dap,
            mcsb=mcsb,
            c2ei=c2ei,
            scsb=scsb,
        )

    @classmethod
    def unmarshall_datain(cls, d, lba=0, tl=0, **kwargs):
        """
        Unmarshall the ReadCD datain.

        :param data: a byte array
        :return result: a dict
        """
        result = {}

        est = kwargs["est"]
        mcsb = kwargs["mcsb"] << 3
        # Need to remap according to MMC:
        # Table 354 — Main Channel Selection and Mapped Values
        if (
            mcsb
            in [0x28, 0x48, 0x68, 0x88, 0x90, 0x98, 0xA8, 0xC0, 0xC8, 0xD0, 0xD8, 0xE8]
            and est != EXPECTED_SECTOR_TYPE.CDDA
        ):
            raise ValueError("Invalid MCSB/EST combination")
        if mcsb in [0x30, 0xB0, 0xB8] and est > EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS:
            raise ValueError("Invalid MCSB/EST combination")
        if est == EXPECTED_SECTOR_TYPE.CDDA:
            mcsb = 0x10
        if mcsb == 0x08 and est == EXPECTED_SECTOR_TYPE.MODE_2_FORM_1:
            mcsb = 0x10
        if mcsb == 0x38 and est == EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS:
            mcsb = 0x30
        if mcsb == 0x58 and est == EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS:
            mcsb = 0x10
        if mcsb == 0xB8 and est == EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS:
            mcsb = 0xB0
        if mcsb == 0xF8 and est == EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS:
            mcsb = 0xB0
        if mcsb == 0x40 and est in [
            EXPECTED_SECTOR_TYPE.MODE_1,
            EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS,
        ]:
            mcsb = 0x00
        if mcsb == 0x50 and est < EXPECTED_SECTOR_TYPE.MODE_2_FORM_1:
            mcsb = 0x10
        if mcsb == 0x58 and est == EXPECTED_SECTOR_TYPE.MODE_1:
            mcsb = 0x18
        if mcsb == 0x60 and est in [
            EXPECTED_SECTOR_TYPE.MODE_1,
            EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS,
        ]:
            mcsb = 0x20
        if mcsb == 0x70 and est in [
            EXPECTED_SECTOR_TYPE.MODE_1,
            EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS,
        ]:
            mcsb = 0x30
        if mcsb == 0x78 and est in [
            EXPECTED_SECTOR_TYPE.MODE_1,
            EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS,
        ]:
            mcsb = 0x38
        if mcsb == 0xE0 and est in [
            EXPECTED_SECTOR_TYPE.MODE_1,
            EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS,
        ]:
            mcsb = 0xA0
        if mcsb == 0xF0 and est in [
            EXPECTED_SECTOR_TYPE.MODE_1,
            EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS,
        ]:
            mcsb = 0xB0
        if mcsb == 0xF8 and est == EXPECTED_SECTOR_TYPE.MODE_1:
            mcsb = 0xB8
        mcsb = mcsb >> 3

        for l in range(lba, lba + tl):
            r = {}
            # SYNC
            if mcsb & 0x10:
                r["sync"] = d[:12]
                d = d[12:]
            # Header Codes: Sector Header
            if mcsb & 0x04:
                r["sector-header"] = {}
                convert.decode_bits(d, cls._sh_bits, r["sector-header"])
                d = d[4:]
            # Header Codes: Sector Subheader
            if mcsb & 0x08:
                r["sector-subheader"] = []
                # sub header first copy
                _b = {}
                _b["file-number"] = d[0]
                _b["channel-number"] = d[1]
                _b["sub-mode"] = d[2]
                _b["data"] = d[:4]
                r["sector-subheader"].append(_b)
                d = d[4:]
                # sub header second copy
                _b = {}
                _b["file-number"] = d[0]
                _b["channel-number"] = d[1]
                _b["sub-mode"] = d[2]
                _b["data"] = d[:4]
                r["sector-subheader"].append(_b)
                d = d[4:]
            # User Data
            if mcsb & 0x02:
                # CD-DA
                if est == EXPECTED_SECTOR_TYPE.CDDA:
                    r["data"] = d[:2352]
                    d = d[2352:]
                # Mode 1
                if est == EXPECTED_SECTOR_TYPE.MODE_1:
                    r["data"] = d[:2048]
                    d = d[2048:]
                # Mode 2 Formless
                if est == EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS:
                    r["data"] = d[:2336]
                    d = d[2336:]
                # Mode 2 Form 1
                if est == EXPECTED_SECTOR_TYPE.MODE_2_FORM_1:
                    r["data"] = d[:2048]
                    d = d[2048:]
                # Mode 2 Form 2
                if est == EXPECTED_SECTOR_TYPE.MODE_2_FORM_2:
                    r["data"] = d[:2324]
                    d = d[2324:]
            if mcsb & 0x01:
                if est == EXPECTED_SECTOR_TYPE.CDDA:
                    # Everything is DATA for CDDA
                    True
                elif est == EXPECTED_SECTOR_TYPE.MODE_1:
                    r["edc"] = d[:4]
                    d = d[4:]
                    # zero fill
                    d = d[8:]
                    r["p-parity"] = d[:172]
                    d = d[172:]
                    r["q-parity"] = d[:104]
                    d = d[104:]
                elif est == EXPECTED_SECTOR_TYPE.MODE_2_FORMLESS:
                    raise ValueError("No EDC/ECC for Mode2Formless")
                elif est == EXPECTED_SECTOR_TYPE.MODE_2_FORM_1:
                    r["edc"] = d[:4]
                    d = d[4:]
                    r["p-parity"] = d[:172]
                    d = d[172:]
                    r["q-parity"] = d[:104]
                    d = d[104:]
                elif est == EXPECTED_SECTOR_TYPE.MODE_2_FORM_2:
                    r["edc"] = d[:4]
                    d = d[4:]
                else:
                    raise NotImplementedError(
                        "EDC/ECC not yet implemented for this MCSB/EST combination"
                    )

            if kwargs["c2ei"] == 1:
                r["c2ei-data"] = d[:294]
                d = d[294:]
            if kwargs["c2ei"] == 2:
                r["c2ei"] = {}
                r["c2ei"]["data"] = d[:296]
                d = d[296:]

            if kwargs["scsb"] == 2:
                r["subchannel"] = {}
                convert.decode_bits(d, cls._sc2_bits, r["subchannel"])
                r["subchannel"]["data"] = d[:16]
                d = d[16:]
            if kwargs["scsb"] == 4:
                r["subchannel"] = {}
                r["subchannel"]["data"] = d[:96]
                d = d[96:]

            result[l] = r

        return result

#!/usr/bin/env python
# coding: utf-8

from pyscsi.utils.enum import Enum
from pyscsi.pyscsi.scsi_enum_command import smc

enum_dict = {'A': 1,
             'B': 2,
             'C': 3, }


def main():
    i = Enum(enum_dict)
    assert i.A == 1
    assert i.B == 2
    assert i.C == 3
    assert i[1] == 'A'
    assert i[2] == 'B'
    assert i[3] == 'C'
    assert i[4] == ''
    a = Enum(A=1, B=2, C=3)
    assert a.A == 1
    assert a.B == 2
    assert a.C == 3
    assert a[1] == 'A'
    assert a[2] == 'B'
    assert a[3] == 'C'
    assert a[4] == ''
    assert smc.WRITE_BUFFER.value == 0x3b
    assert smc.WRITE_BUFFER.name == 'WRITE_BUFFER'


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# coding: utf-8

from sgio.utils.enum import Enum

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


if __name__ == "__main__":
    main()

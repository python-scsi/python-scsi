#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.enum import Enum

enum_dict = {'a': 1,
             'b': 2,
             'c': 3, }


def main():
    i = Enum(enum_dict)
    dir(i)
    print i.a
    print i.c

    i = Enum({'a': 3, 'b': 2, 'c': 1, })
    dir(i)
    print i.a
    print i.c

    i = Enum(a=5, b=6, c=7)
    dir(i)
    print i.a
    print i.c

if __name__ == "__main__":
    main()
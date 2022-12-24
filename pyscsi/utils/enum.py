# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# we disable some pylint errors since we know it will work ..
# pylint: disable=not-an-iterable
# pylint: disable=unsupported-membership-test

from typing import Any, Dict

from pyscsi.utils.exception import NotSupportedArgumentError


class Enum(type):
    """ A class for  pseudo enumerators

        usage:

         >>fubar = Enum(a=1,b=2)
         >>fubar.a
         1
         >>fubar= Enum({'a': 1, 'b': 2})
         >>fubar.a
         1

        for now there is not much of a sanity check here, like if the key already exists
        or if a enum value is already there. It's basically a little helper for the other
        packages in this project and for now the developer has to take care that stuff is
        sane. And we assume  that we pass either a dict or simply keyword arguments!

        TODO:

          - adding check if value exists
    """

    def __new__(cls, *args: Any, **kwargs: Any):
        """
        Building a new Enum object with a dict or keyword arguments
        """
        tmp: Dict[str, Any] = {}
        if len(args) == 1 and type(args[0]).__name__ == 'dict':
            tmp.update(args[0])
        elif kwargs:
            tmp.update(**kwargs)
        else:
            raise NotSupportedArgumentError("use either as dict or provide keyword arguments")
        return super().__new__(cls, cls.__name__, (), tmp)

    def __init__(cls, *args: Any, **kwargs: Any) -> None:
            super().__init__(cls.__name__, args, kwargs)

    def __getitem__(cls, value: str) -> str:
        for key in cls.keys:
            if getattr(cls, key) == value:
                return key
        return ""

    def add(cls, key: str, value: Any) -> None:
        """
        method to add key to the Enum
        """
        if key in cls.keys:
            raise KeyError(f"key {key} already exist")
        setattr(cls, key, value)

    def remove(cls, key: str) -> None:
        """
        method to remove key from the Enum
        """
        try:
            delattr(cls, key)
        except (AttributeError, KeyError) as ex:
            raise KeyError(f"Key {ex} not found") from ex

    @property
    def keys(cls) -> list[str]:
        """
        Property to return a list of Keys in the Enum.
        """
        result: list[str] = [key for key, val in vars(cls).items() if not callable(val)
                and not key.startswith('__')
                or not type(val).__name__ != 'method']
        return result

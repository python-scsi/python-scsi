# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

class Enum(type):
    """ A class for  pseudo enumerators

        usage:

         >>fubar = Enum(a=1,b=2)
         >>fubar.a
         1
         >>fubar= Enum({'a': 1, 'b': 2})
         >>fubar.a
         1

        for now there is not much of a sanity check here, like if the key already exists or if a enum
        value is already there. It's basically a little helper for the other packages in this project
        and for now the developer has to take care that stuff is is sane. And we assume  that we pass either
        a dict or simply keyword arguments!

        TODO:

          - adding check if value exists
    """

    def __new__(cls, *args, **kwargs):
        """
        Building a new Enum object with a dict or keyword arguments
        """
        tmp = {}
        if len(args) == 1 and type(args[0]).__name__ == 'dict':
            tmp.update(args[0])
        else:
            tmp.update(dict(**kwargs))
        tmp['_enums'] = tmp.keys()
        return type.__new__(cls, cls.__name__, (), tmp)

    def __init__(self, *args, **kwargs):
        setattr(self, 'add', classmethod(self.__class__.add))
        setattr(self, 'remove', classmethod(self.__class__.remove))

    def __getitem__(self, value):
        for key in self._enums:
            if self.__getattribute__(self, key) == value:
                return key
        return ""

    def add(self, key, value):
        try:
            getattr(self,
                    key)
            print("key %s already exist" % key)
        except:
            self._enums.append(key)
            setattr(self,
                    key,
                    value)

    def remove(self, key):
        try:
            delattr(self, key)
            self._enums.remove(key)
        except (AttributeError, KeyError) as e:
            print("Key %s not found" % e)

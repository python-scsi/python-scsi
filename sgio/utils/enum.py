# coding: utf-8

#      Copyright (C) 2014 by Markus Rosjat<markus.rosjat@gmail.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU Lesser General Public License as published by
#	   the Free Software Foundation; either version 2.1 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU Lesser General Public License for more details.
#
#	   You should have received a copy of the GNU Lesser General Public License
#	   along with this program; if not, see <http://www.gnu.org/licenses/>.


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
        and for now the developer has to take care that stuff is is sane.

        TODO:

          - adding check if key exists
          - adding check if value exists
    """

    def __new__(cls,*args, **kwargs):
        if len(args) > 0:
            if len(args) == 1:
                if type(args[0]).__name__ == 'dict':
                    tmp = args[0]
                else:
                    tmp ={}
            else:
                tmp = dict()
        elif len(kwargs) > 0:
            if len(kwargs) == 1:
                tmp = kwargs
            else:
                tmp = dict(**kwargs)
        else:
            tmp = dict()
        tmp['_enums'] = tmp.keys()
        return type.__new__(cls, cls.__name__, (), tmp)

    def __init__(self, *args, **kwargs):
        setattr(self, 'add', classmethod(self.__class__.add))
        setattr(self, 'remove', classmethod(self.__class__.remove))

    def add(self, key, value):
        if not key in self._enums:
            self._enums.append(key)
            setattr(self, key, value)

    def remove(self, key):
        if key in self._enums:
            delattr(self, key)
            self._enums.remove(key)

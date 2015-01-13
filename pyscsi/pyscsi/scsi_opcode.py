# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from pyscsi.utils.enum import Enum


class OpCode(object):

    _name = ''
    _code = 0xff
    _serviceaction = None

    def __init__(self, name, code, serviceaction):
        self._name = name
        self._code = code
        self._serviceaction = Enum(serviceaction)

    def __str__(self):
        return '%s - %x' % (self.name, self.value)

    def __repr__(self):
        return '%s - %x' % (self.name, self.value)

    @property
    def name(self):
        """
        getter method of the name property

        :return: a  string
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        setter method of the name property

        :param value: a string
        """
        self._name = value

    @property
    def value(self):
        """
        getter method of the value property

        :return: a hex value
        """
        return self._code

    @value.setter
    def value(self, value):
        """
        setter method of the value property

        :param value: a hex value
        """
        self._code = value

    @property
    def serviceaction(self):
        """
        getter method of the serviceaction property

        :return: a Enum object
        """
        return self._serviceaction

    @serviceaction.setter
    def serviceaction(self, value):
        """
        setter method of the serviceaction property

        :param value: a Enum object
        """
        self._serviceaction = value

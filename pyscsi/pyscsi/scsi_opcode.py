# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.utils.enum import Enum


class OpCode(object):
    """
    A class to hold information about a scsi operation code
    """
    _name = ''
    _code = 0xff
    _serviceaction = None

    def __init__(self,
                 name,
                 code,
                 serviceaction):
        """
        initialize a new instance

        :param name: a string representing the name of the operation code
        :param code: a hexadecimal value representing the value associated with the operation code
        :param serviceaction: a Enum with service actions supported by the command associtaed with the operation code
        """
        self._name = name
        self._code = code
        self._serviceaction = Enum(serviceaction)

    def __str__(self):
        return '%s - %x' % (self.name,
                            self.value)

    def __repr__(self):
        return '%s - %x' % (self.name,
                            self.value)

    @property
    def name(self):
        """
        getter method of the name property

        :return: a  string
        """
        return self._name

    @name.setter
    def name(self,
             value):
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
    def value(self,
              value):
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
    def serviceaction(self,
                      value):
        """
        setter method of the serviceaction property

        :param value: a Enum object
        """
        self._serviceaction = value

# coding: utf-8

from pyscsi.utils.enum import Enum


class OpCodeMapper(object):

    def __init__(self, opcodes, serviceaction):
        self._opcode = Enum(opcodes)
        self._serviceaction = Enum(serviceaction)

    @property
    def opcode(self):
        """
        getter method of the opcode property

        :return: a Enum object
        """
        return self._opcode

    @opcode.setter
    def opcode(self, value):
        """
        setter method of the result property

        :param value: a Enum object
        """
        self._opcode = value

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

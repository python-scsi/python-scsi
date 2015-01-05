# coding: utf-8


class MockDevice(object):

    @property
    def opcodeMapper(self):
        return self._opcode

    @opcodeMapper.setter
    def opcodeMapper(self, value):
        self._opcode = value

    def execute(self, cdb, dataout, datain, sense):
        pass

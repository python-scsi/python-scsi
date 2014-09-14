class SCSICommand:
    def __init__(self, dev, dataout_alloclen, datain_alloclen):
        self.dev = dev
        self.sense = bytearray(32)
        self.dataout = bytearray(dataout_alloclen)
        self.datain = bytearray(datain_alloclen)
        self._result = {}

    def execute(self):
        self.dev.execute(self.cdb, self.dataout,
                         self.datain, self.sense)
        self.unmarshall()

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    def add_result(self, key, value):
        self.result.update({key:value})

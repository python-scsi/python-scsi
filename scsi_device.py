import scsi
import scsi_sense
import sgio

class SCSIDevice:
    def __init__(self, device):
        self._fd = sgio.open(device)

    def execute(self, cdb, dataout, datain, sense):
        status = sgio.execute(self._fd, cdb, dataout, datain, sense)
        if status == scsi.SCSI_STATUS_CHECK_CONDITION:
            raise scsi_sense.SCSICheckCondition(sense)
        if status == scsi.SCSI_STATUS_SGIO_ERROR:
            raise scsi_sense.SCSISGIOError()


from scsi_device import SCSIDevice
from scsi_command import SCSICommand
from scsi_cdb_inquiry import Inquiry

SCSI_STATUS_GOOD                 = 0x00
SCSI_STATUS_CHECK_CONDITION      = 0x02
SCSI_STATUS_CONDITIONS_MET       = 0x04
SCSI_STATUS_BUSY                 = 0x08
SCSI_STATUS_RESERVATION_CONFLICT = 0x18
SCSI_STATUS_TASK_SET_FULL        = 0x28
SCSI_STATUS_ACA_ACTIVE           = 0x30
SCSI_STATUS_TASK_ABORTED         = 0x40
SCSI_STATUS_SGIO_ERROR           = 0xff

class SCSI(SCSIDevice):
    def Inquiry(self, evpd = 0, page_code = 0, alloc_len = 96):
        return Inquiry(self, evpd, page_code, alloc_len)


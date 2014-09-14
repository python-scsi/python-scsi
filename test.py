#!/usr/bin/env python
import sys
from scsi import SCSI
import scsi_cdb_inquiry as INQUIRY

if __name__ == "__main__":
    s = SCSI(sys.argv[1])

    i = s.Inquiry().result
    print i

    i = s.Inquiry(evpd = 1, page_code = INQUIRY.SUPPORTED_VPD_PAGES).result
    print i


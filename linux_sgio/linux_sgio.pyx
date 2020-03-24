# ========================================================================== **
#                                sgiomodule.c
# 
# Copyright:
#  Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
#  Copyright (C) 2014 by Christopher R. Hertel <crh@ubiqx.org>
#  Copyright (C) 2016-2020 by Diego Elio Pettenò <flameeyes@flameeyes.com>
# 
# Description: A Python binding for the Linux SCSI Generic (sg) Driver.
# 
# -------------------------------------------------------------------------- **
# License:
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
# 
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
# 
# -------------------------------------------------------------------------- **
# References:
#  + Linux SCSI Generic (sg) Driver: http://sg.danny.cz/sg/
#  + Tour the Linux generic SCSI driver:
#      http://www.ibm.com/developerworks/library/l-scsi-api/
#  + Extending Python with C or C++:
#      https://docs.python.org/2/extending/extending.html
#  + Python Extension Programming with C:
#      http://www.tutorialspoint.com/python/python_further_extensions.htm
# 
# See Also:
#  + The Linux SCSI Generic (sg) HOWTO:
#      (Though out of date, this Linux 2.4 doc provides useful info.)
#      http://www.tldp.org/HOWTO/SCSI-Generic-HOWTO/index.html
# 
# 
# ========================================================================== **
#

from cpython.bytearray cimport PyByteArray_FromStringAndSize

from libc.errno cimport errno
from libc.stdlib cimport calloc
from posix.ioctl cimport ioctl

cdef extern from "scsi/sg.h":
    cdef enum:
        SG_IO

    cdef enum:
        SCSI_STATUS_CHECK_CONDITION

    cdef enum:
        SG_DXFER_NONE
        SG_DXFER_TO_DEV
        SG_DXFER_FROM_DEV
        SG_DXFER_TO_FROM_DEV

    cdef enum:
        SG_INFO_OK_MASK
        SG_INFO_OK

    ctypedef struct sg_io_hdr_t:
        int interface_id
        int dxfer_direction
        unsigned char cmd_len
        unsigned char mx_sb_len
        unsigned short int iovec_count
        unsigned int dxfer_len
        void * dxferp
        unsigned char * cmdp
        unsigned char * sbp
        unsigned int timeout
        unsigned int flags
        int pack_id
        void * usr_ptr
        unsigned char status
        unsigned char masked_status
        unsigned char msg_status
        unsigned char sb_len_wr
        unsigned short int host_status
        unsigned short int driver_status
        int resid
        unsigned int duration
        unsigned int info


class CheckConditionError(Exception):
    """The target is reporting an error.
    
    Send a Request Sense command to retrieve error information.

    See https://en.wikipedia.org/wiki/SCSI_check_condition for details.
    """

    def __init__(self, sense):
        super(CheckConditionError, self).__init__()
        self.sense = sense


class UnspecifiedError(Exception):
    """Something went wrong."""


def execute(
        fid,
        bytearray cdb,
        bytearray data_out,
        bytearray data_in,
):
    cdef sg_io_hdr_t io_hdr
    cdef unsigned char *sense = <unsigned char *> calloc(
        32, sizeof(unsigned char))
    cdef unsigned char *input = <unsigned char *> calloc(
        len(data_in) + 1, sizeof(unsigned char))

    if not sense or not input:
        raise MemoryError()

    # Prepare the sg device I/O header structure.
    io_hdr.interface_id = 'S'
    io_hdr.cmd_len = len(cdb)
    io_hdr.iovec_count = 0
    io_hdr.cmdp = cdb
    io_hdr.sbp = sense
    io_hdr.timeout = 1800000
    io_hdr.flags = 0
    io_hdr.mx_sb_len = len(sense)

    if len(data_out) and len(data_in):
        raise NotImplemented('Indirect IO is not supported.')
    elif len(data_out):
        io_hdr.dxfer_direction = SG_DXFER_TO_DEV
        io_hdr.dxfer_len = len(data_out)
        io_hdr.dxferp = <void*>data_out
    elif len(data_in):
        io_hdr.dxfer_direction = SG_DXFER_FROM_DEV
        io_hdr.dxfer_len = len(data_in)
        io_hdr.dxferp = input
    else:
        io_hdr.dxfer_len = 0
        io_hdr.dxferp = NULL
        io_hdr.dxfer_direction = SG_DXFER_NONE

    result = ioctl(fid.fileno(), SG_IO, &io_hdr)
    if result < 0:
        raise OSError(errno)

    if io_hdr.info & SG_INFO_OK_MASK != SG_INFO_OK:
        if io_hdr.sb_len_wr > 0:
            raise CheckConditionError(sense)
        else:
            raise UnspecifiedError()

    input_array = PyByteArray_FromStringAndSize(
        <char*>input, io_hdr.resid)
    for idx in range(len(input_array)):
        data_in[idx] = input_array[idx]

    # Return the actual transfer written.
    return io_hdr.resid

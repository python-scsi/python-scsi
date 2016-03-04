from pyscsi.pyscsi.scsi_exception import SCSIDeviceCommandExceptionMeta as ExMETA
import pyscsi.pyscsi.scsi_enum_command as scsi_enum_command

try:
    import libiscsi
    _has_libiscsi = True
except ImportError as e:
    _has_libiscsi = False

# make a new base class with the metaclass this should solve the problem with the
# python 2 and python 3 metaclass definitions
_new_base_class = ExMETA('SCSIDeviceCommandExceptionMeta', (object,), {})


class ISCSIDevice(_new_base_class):
    """
    The iscsi device class

    By default it gets the SPC opcodes assigned so it's always possible to issue
    a inquiry command to the device. This is important since the the Command will
    figure out the opcode from the SCSIDevice first to use it for building the cdb.
    This means after the that it's possible to use the proper OpCodes for the device.
    A basic workflow for using a device would be:
        - try to open the device passed by the device arg
        - create a  Inquiry instance, with the default opcodes of the device
        - execute the inquiry with the device
        - unmarshall the datain from the inquiry command to figure out the device type
        - assign the proper Opcode for the device type (it would also work just to use the
          opcodes without assigning them to the device since the command builds the cdb
          and the device just executes)

    Note: The workflow above is already implemented in the SCSI class
    """

    def __init__(self,
                 device):
        """
        initialize a  new instance of a ISCSIDevice

        :param device: the file descriptor
        """
        self._opcodes = scsi_enum_command.spc
        self._file_name = device
        self._iscsi = None
        self._iscsi_url = None
        if _has_libiscsi and device[:8] == 'iscsi://':
            self.open()
        else:
            raise NotImplementedError('No backend implemented for %s' % device)

    def __enter__(self):
        return self

    def __exit__(self,
                 exc_type,
                 exc_val,
                 exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        # we may need to do more teardown here ?
        self.close()

    def open(self):
        """

        """
        self._iscsi = libiscsi.iscsi_create_context('iqn.2007-10.com.github:python-scsi')
        self._iscsi_url = libiscsi.iscsi_parse_full_url(self._iscsi,
                                                        self._file_name)
        libiscsi.iscsi_set_targetname(self._iscsi,
                                      self._iscsi_url.target)
        libiscsi.iscsi_set_session_type(self._iscsi,
                                        libiscsi.ISCSI_SESSION_NORMAL)
        libiscsi.iscsi_set_header_digest(self._iscsi,
                                         libiscsi.ISCSI_HEADER_DIGEST_NONE_CRC32C)
        libiscsi.iscsi_full_connect_sync(self._iscsi,
                                         self._iscsi_url.portal,
                                         self._iscsi_url.lun)

    def close(self):
        # we may need to do more teardown here ?
        libiscsi.iscsi_destroy_context(self._iscsi)

    def execute(self,
                cdb,
                dataout,
                datain,
                sense):
        """
        execute a scsi command
        :param cdb: a byte array representing a command descriptor block
        :param dataout: a byte array to hold received data from the ioctl call
        :param datain: a byte array to hold data passed to the ioctl call
        :param sense: a byte array to hold sense data
        """
        _dir = libiscsi.SCSI_XFER_NONE
        _xferlen = 0
        if len(datain):
            _dir = libiscsi.SCSI_XFER_READ
            _xferlen = len(datain)
        if len(dataout):
            _dir = libiscsi.SCSI_XFER_WRITE
            _xferlen = len(dataout)
        _task = libiscsi.scsi_create_task(cdb,
                                          _dir,
                                          _xferlen)
        if len(datain):
            libiscsi.scsi_task_add_data_in_buffer(_task,
                                                  datain)
        if len(dataout):
            libiscsi.scsi_task_add_data_out_buffer(_task,
                                                   dataout)

        libiscsi.iscsi_scsi_command_sync(self._iscsi,
                                         self._iscsi_url.lun,
                                         _task,
                                         None)
        _status = libiscsi.scsi_task_get_status(_task,
                                                None)
        if _status == libiscsi.SCSI_STATUS_CHECK_CONDITION:
            raise self.CheckCondition(sense)
        if _status == libiscsi.SCSI_STATUS_GOOD:
            return
        raise self.SCSISGIOError

    @property
    def opcodes(self):
        return self._opcodes

    @opcodes.setter
    def opcodes(self,
                value):
        self._opcodes = value

    @property
    def devicetype(self):
        return self._devicetype

    @devicetype.setter
    def devicetype(self,
                   value):
        self._devicetype = value
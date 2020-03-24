import unittest

import libiscsi

class LibISCSITest(unittest.TestCase):

    def test_url_parse(self):
        context = libiscsi.Context("foobar")

        url = libiscsi.URL(context, "iscsi://localhost/my-target/0")
        self.assertEqual(url.portal, "localhost")

    def test_set_context_params(self):
        context = libiscsi.Context("foobar")
        context.set_targetname("my-target")
        context.set_header_digest(libiscsi.ISCSI_HEADER_DIGEST_NONE)

    def test_task(self):
        task = libiscsi.Task(
            b"\x12\x00\x00\x00\x60\x00",
            libiscsi.SCSI_XFER_READ,
            96)

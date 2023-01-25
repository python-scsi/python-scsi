# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# Copyright (C) 2023 by Brian Meagher<brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.utils.enum import Enum

__all__ = ["PR_TYPE", "PR_SCOPE", "PROTOCOL_ID"]

# ------------------------------------------------------------------------------
# Persistent reservation TYPE
# ------------------------------------------------------------------------------

pr_type = {
    "WRITE_EXCLUSIVE": 0x01,
    "EXCLUSIVE_ACCESS": 0x03,
    "WRITE_EXCLUSIVE_REGISTRANTS_ONLY": 0x05,
    "EXCLUSIVE_ACCESS_REGISTRANTS_ONLY": 0x06,
    "WRITE_EXCLUSIVE_ALL_REGISTRANTS": 0x07,
    "EXCLUSIVE_ACCESS_ALL_REGISTRANTS": 0x08,
}

# ------------------------------------------------------------------------------
# Persistent reservations scope
# ------------------------------------------------------------------------------

pr_scope = {
    "LU_SCOPE": 0x00,
}

# ------------------------------------------------------------------------------
# Protocol Identifier
# ------------------------------------------------------------------------------

protocol_id = {
    "FIBRE_CHANNEL": 0x00,
    "IEEE_1394": 0x03,
    "RDMA": 0x04,
    "ISCSI": 0x05,
    "SAS": 0x06,
    "SOP": 0x0A,
}

# ------------------------------------------------------------------------------
# Instantiate the Enum Objects
# ------------------------------------------------------------------------------

PR_TYPE = Enum(pr_type)
PR_SCOPE = Enum(pr_scope)
PROTOCOL_ID = Enum(protocol_id)

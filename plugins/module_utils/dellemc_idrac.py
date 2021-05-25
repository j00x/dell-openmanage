# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.1
# Copyright (C) 2018-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from omsdk.sdkinfra import sdkinfra
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare, file_share_manager
    from omsdk.sdkprotopref import ProtoPreference, ProtocolEnum
    from omsdk.http.sdkwsmanbase import WsManOptions
    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False


class iDRACConnection:

    def __init__(self, module_params):
        if not HAS_OMSDK:
            raise ImportError("Dell EMC OMSDK library is required for this module")
        self.idrac_ip = module_params['idrac_ip']
        self.idrac_user = module_params['idrac_user']
        self.idrac_pwd = module_params['idrac_password']
        self.idrac_port = module_params['idrac_port']
        if not all((self.idrac_ip, self.idrac_user, self.idrac_pwd)):
            raise ValueError("hostname, username and password required")
        self.handle = None
        self.creds = UserCredentials(self.idrac_user, self.idrac_pwd)
        self.pOp = WsManOptions(port=self.idrac_port)
        self.sdk = sdkinfra()
        if self.sdk is None:
            msg = "Could not initialize iDRAC drivers."
            raise RuntimeError(msg)

    def __enter__(self):
        self.sdk.importPath()
        self.handle = self.sdk.get_driver(self.sdk.driver_enum.iDRAC, self.idrac_ip, self.creds, pOptions=self.pOp)
        if self.handle is None:
            msg = "Unable to communicate with iDRAC {0}. This most often indicates one of the following:\n\n" \
                  "1. A bad username/password\n" \
                  "2. The iDRAC IP address is unreachable\n" \
                  "3. A failure in a TLS/SSL handshake (proxies/firewalls are a common cause of this problem)\n".format(self.idrac_ip)
            raise RuntimeError(msg)
        return self.handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle.disconnect()
        return False

#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         keystone.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

from tools.pycurl.drivers.driver_base import DriverPycurl


class Keystone(DriverPycurl):
    def __init__(self, region):
        super(Keystone, self).__init__()
        self.header_list = ["Accept: application/json",
                            "Content-Type: application/json"]
        self._keystone_url = self._conffile.get(region, "KeystoneEndpoint")

    #def postpycurl(self, header_list=False, bodydata_json=False, timeout=False):
    def postpycurl(self, kwdarg):
        if "header_list" not in kwdarg:
            header_list = self.header_list

        return self._postpycurl_returnstr(self._keystone_url, kwdarg["bodydata_json"],
                                          header_list, kwdarg["timeout"])



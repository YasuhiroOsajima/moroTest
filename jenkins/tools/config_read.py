#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         config_read.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

import os

from ConfigParser import SafeConfigParser

configfile_path = "../jobenv.ini"


class ConfigReade(object):
    def __init__(self):
        self._conffile = SafeConfigParser()
        self._conffile.read(configfile_path)

        self._tenantid = self._conffile.get(region, "TenantId")
        self._tenantuser = self._conffile.get(region, "TenantUser")
        self._tenantpassword = self._conffile.get(region, "TenantPassword")
        self._keystone_url = self._conffile.get(region, "KeystoneEndpoint")
        self._vmid = self._conffile.get(region, "VMUuid")
        self._volumeid = self._conffile.get(region, "VolumeUuid")



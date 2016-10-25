#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         default.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

from tools.pycurl.drivers.driver_base import DriverPycurl


class Default(DriverPycurl):
    def __init__(self, region):
        super(Default, self).__init__()



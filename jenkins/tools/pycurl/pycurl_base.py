#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         pycurl_base.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

import inspect
import re
import os


class PyCurl(object):
    def __init__(self):
        self.driver = False

    def getpycurl(self, **kwdarg):
        return self.driver.getpycurl(kwdarg)

    def postpycurl(self, **kwdarg):
        return self.driver.postpycurl(kwdarg)

    def postpycurl_file(self, **kwdarg):
        return self.driver.postpycurl_file(kwdarg)

    def putpycurl(self, **kwdarg):
        return self.driver.putpycurl(kwdarg) 

    def patchpycurl(self, **kwdarg):
        return self.driver.patchpycurl(kwdarg)

    def deletepycurl(self, **kwdarg):
        return self.driver.deletepycurl(kwdarg)

    def set_compornent(self, compornent, region):
        curentdir = os.path.abspath(os.path.dirname(__file__))
          #/opt/zcom_autobackup/tools/restapi
        modulebase = "tools.pycurl.drivers"
        modulepath = "%s.%s" % (modulebase, compornent)
        importstr = "import %s" % modulepath
        exec importstr

        exec "classestuple = inspect.getmembers(%s, inspect.isclass)" % modulepath
          #get class names list by module file. like this.
          #[('TEST1', <class test2.TEST1 at 0x7f34fbcae870>), ('TEST2', <class test2.TEST2 at 0x7f34fbcae808>)]

        searcher = re.compile(compornent, re.IGNORECASE)
        classname = [classtuple[0] for classtuple in classestuple
                      if searcher.match(classtuple[0])
                      and len(compornent)==len(classtuple[0])][0]

        exec ("self.driver = %s.%s(region)" % (modulepath, classname))

          ### Use this module like this.
          #driver = PyCurl()
          #driver.set_compornen('nova')
          #result = driver.getpycurl(lasturl, timeout)
          #result = driver.postpycurl(lasturl, bodydata_json, timeout)
          #result = driver.deletepycurl(lasturl, timeout)
          #
          #You can following drivers
          #  tools/restapi/drivers
          #    cinder
          #    driver_base
          #    glance
          #    keystone
          #    nexenta
          #    nova
          #    storagevolume


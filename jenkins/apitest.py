#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         apitest.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

import sys
import os

from ConfigParser import SafeConfigParser

from csvapi import CSVAPI
from exception_classes import InvalidArgument
from exception_classes import FunctionResultFail

configfile_path = "jobenv.ini"


class APITest(object):
    def __init__(self, region, jobname):
        self.__validate_option(region, jobname)
        self.testlogic = CSVAPI(region, jobname)

    def __validate_option(self, region, jobname):
        conffile = SafeConfigParser()
        conffile.read(configfile_path)
        if region not in conffile.sections():
            raise InvalidArgument(region)

        scriptsdir = os.path.abspath(os.path.dirname(__file__))
        if "%s.csv" % jobname not in os.listdir("%s/apilist/" % scriptsdir):
            raise InvalidArgument(jobname)

    #def set_testlogic(self, logictype):
    #    curentdir = os.path.abspath(os.path.dirname(__file__))
    #    modulebase = "tools.pycurl.drivers"
    #    modulepath = "%s.%s" % (modulebase, logictype)
    #    importstr = "import %s" % modulepath
    #    exec importstr

    #    exec "classestuple = inspect.getmembers(%s, inspect.isclass)" % modulepath
    #      #get class names list by module file. like this.
    #      #[('TEST1', <class test2.TEST1 at 0x7f34fbcae870>), ('TEST2', <class test2.TEST2 at 0x7f34fbcae808>)]

    #    searcher = re.compile(logictype, re.IGNORECASE)
    #    classname = [classtuple[0] for classtuple in classestuple
    #                  if searcher.match(classtuple[0])
    #                  and len(logictype)==len(classtuple[0])][0]

    #    exec ("self.driver = %s.%s(region)" % (modulepath, classname))

    def pre_method(self):
        return self.testlogic.pre_method()

    def run_api(self):
        return self.testlogic.run_api()

    def post_method(self):
        return self.testlogic.post_method()

    def main(self):

        if not self.pre_method():
            raise FunctionResultFail("provision")

        if not self.run_api():
            raise FunctionResultFail("api test")

        if not self.post_method():
            raise FunctionResultFail("clean up")

        return True


if __name__ == "__main__":
    region = sys.argv[1]
    jobname = sys.argv[2]
    APITest(region, jobname).main()



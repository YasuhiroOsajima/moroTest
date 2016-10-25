#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         exception_classes.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================


class InvalidArgument(Exception):
    def __init__(self, arg):
        self.__message = "Invalid argument: %s" % arg
        print(self.__message)

    def __str__(self):
        return repr(self.__message)


class FunctionResultFail(Exception):
    def __init__(self, func):
        self.__message = "Failed result: %s" % func
        print(self.__message)

    def __str__(self):
        return repr(self.__message)


class APIResultCheckFail(Exception):
    def __init__(self, check, apiresult):
        self.__message = ("API result check failed. CHECK: %s , API:%s"
                          % (check, apiresult))
        print(self.__message)

    def __str__(self):
        return repr(self.__message)



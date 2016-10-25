#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         ssh.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

import paramiko

from ConfigParser import SafeConfigParser

configfile_path = "jobenv.ini"


class SSH(object):
    def __init__(self):
        self._conffile = SafeConfigParser()
        self._conffile.read(configfile_path)
        self._user = self._conffile.get(region, "SSHUser")
        self._passwd = self._conffile.get(region, "SSHPassword")
        self._port = 22

    def ssh_exec_command(self, command, server):
        connector = paramiko.Transport((server, self._port))
        try:
            connector.connect(username=self._user, password=self._passwd, hostkey=None)
            channel = connector.open_channel(kind="session")
            channel.exec_command(command)
            stdout = channel.recv(10240)
            stderr = channel.recv_stderr(10240)
            return (stdout, stderr)
        except Exception as errormessage:
            raise Exception("SSH connection error. Server:%s Port:%s User:%s error:%s"
                            %(server, self._port, self._user, errormessage.message))
        finally:
            connector.close()



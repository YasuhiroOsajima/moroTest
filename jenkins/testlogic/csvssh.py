#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         csvssh.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

import os
import csv
import json
import time

from ConfigParser import SafeConfigParser

from tools.pycurl.pycurl_base import PyCurl
from exception_classes import APIResultCheckFail

configfile_path = "jobenv.ini"


class CSVSSH(object):
    def __init__(self, region, jobname):
        self._scriptsdir = os.path.abspath(os.path.dirname(__file__))

        self._conffile = SafeConfigParser()
        self._conffile.read(configfile_path)

        self._tenantid = self._conffile.get(region, "TenantId")
        self._tenantuser = self._conffile.get(region, "TenantUser")
        self._tenantpassword = self._conffile.get(region, "TenantPassword")
        self._keystone_url = self._conffile.get(region, "KeystoneEndpoint")
        self._vmid = self._conffile.get(region, "VMUuid")
        self._volumeid = self._conffile.get(region, "VolumeUuid")

        self.pycurl = PyCurl()

        self._region = region
        self._jobname = jobname

        with open("./apilist/%s.csv" % jobname, 'r') as f:
            self._api_list = list(csv.reader(f))

        self._replace_csv_uuid()
        self._set_token_and_endpoints()

    def _replace_csv_uuid(self):

        def __do_replace(cell):
            repldict = {"/VMID/": self._vmid,
                        "/VOLUMEID/": self._volumeid,
                        "/TENANTID/": self._tenantid}

            for idstring in repldict.keys():
                if idstring in cell:
                    cell = __do_replace(cell.replace(idstring, "/%s/" % repldict[idstring]))

            return cell

        for idx, csvline in enumerate(self._api_list):
            for cell in csvline:
                csvline[csvline.index(cell)] = __do_replace(cell)

            self._api_list[idx] = csvline

        return True

    def _set_token_and_endpoints(self):
        print "------------------------------------------<get token>------------------------------------------"
        bodyjson = ('{"auth":{"passwordCredentials":{"username":"%s","password":"%s"},"tenantId":"%s"}}'
                    % (self._tenantuser, self._tenantpassword, self._tenantid))

        self.pycurl.set_compornent("keystone", self._region)
        apiresult = self.pycurl.postpycurl(bodydata_json=bodyjson, timeout=False)
        resdict = json.loads(apiresult["body"])
        self._tokenid = resdict["access"]["token"]["id"]

        #catalog = resdict["access"]["serviceCatalog"]
        #for endpoint in catalog:
        #    if endpoint["type"]=="compute": self._nova_url = endpoint["endpoints"][0]["publicURL"]
        #    elif endpoint["type"]=="image": self._glance_url = endpoint["endpoints"][0]["publicURL"]
        #    elif endpoint["type"]=="volumev2": self._cinder_url = endpoint["endpoints"][0]["publicURL"]
        #    elif endpoint["type"]=="network": self._neytron_url = endpoint["endpoints"][0]["publicURL"]

        print ""
        return True

    def _exec_restapi(self):
        self.pycurl.set_compornent("default", self._region)

        for apiline in  self._api_list:
            if not apiline or apiline[0].startswith('#'):
                continue

            if apiline[0].startswith('sleep'):
                time.sleep(int(apiline[0].replace('sleep', '')))
                continue

            method, urlstr, header_list, bodydata_json, checkresult = self._parse_apiline(apiline)
            header_list.append("X-Auth-Token: %s" % self._tokenid.encode("UTF-8"))

            curlcmd = ("apiresult = self.pycurl.%spycurl(apiurl=urlstr, header=header_list, body=bodydata_json)"
                       % method.lower())
            exec curlcmd

            #apiresult["header"]["statucode"]
            if checkresult and checkresult not in json.dumps(apiresult["body"]):
                raise APIResultCheckFail(checkresult, apiresult["body"])

            #print apiresult
            print ''
            print "++++++ API Result OK ++++++"
            print ''

    def _parse_apiline(self, apiline):
        idx = 0
        returnlist = [[]]
        for cell in apiline:
            if not cell:
                idx += 1
                returnlist.append([])
                continue

            returnlist[idx].append(cell)

        method = returnlist[0][0] if returnlist[0] else ''
        urlstr = returnlist[1][0] if returnlist[1] else ''
        header_list = returnlist[2]
        bodydata_json = returnlist[3][0] if returnlist[3] else ''
        checkresult = returnlist[4][0] if returnlist[4] else ''

        return method, urlstr, header_list, bodydata_json, checkresult

    def pre_method(self):
        return True

    def run_api(self):
        self._exec_restapi()
        return True

    def post_method(self):
        return True



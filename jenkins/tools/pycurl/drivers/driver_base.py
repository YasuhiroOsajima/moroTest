#! /usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#  FILE:         driver_base.py
#  USAGE: 
#  DESCRIPTION:
#  OPTIONS:
#  REQUIREMENTS:
#===============================================================================

import sys
import pycurl
import json
from io import BytesIO

from ConfigParser import SafeConfigParser

configfile_path = "jobenv.ini"


class DriverPycurl(object):
    def __init__(self):
        self._conffile = SafeConfigParser()
        self._conffile.read(configfile_path)

    def _printcurl(self, method, urlstr, header_list, body_json=False, timeout=False,
                   filepath=False):
        curlcmd = ("curl -X %s %s" % (method, urlstr))
        header_str = " -H '" + "' -H '".join(header_list) if header_list else ''
        body_str = "' -d '%s'" % body_json if body_json else ''
        timeout_str = " --connect-timeout %s" % str(timeout) if timeout else ''
        file_str = " -F xmlBatch=@%s" % str(filepath) if filepath else ''

        curlcmd_total = curlcmd + header_str + body_str + timeout_str + file_str
        print("APIcommand: ")
        print(curlcmd_total)

    def _printresult(self, apiresult_header_body):
        apiresult_header = apiresult_header_body["header"]
        apiresult_body = apiresult_header_body["body"]
        print("APIresult: ")
        print(apiresult_header)
        print(apiresult_body)

    def _responce_generate(self, respheader):
        headersplit = respheader.splitlines()
          #headersplit -> ['HTTP/1.1 200 OK', 'X-Compute-Request-Id: req-53ded28a-65c7-4bd5-9027-7b9c68a979d5', 'Content-Type: application/json', 'Content-Length: 752', 'X-Openstack-Request-Id: req-53ded28a-65c7-4bd5-9027-7b9c68a979d5', 'Date: Tue, 07 Jun 2016 04:24:08 GMT', '']

        statuscode = [codeline for codeline in headersplit if codeline.startswith("HTTP")][0]
        header_list = [tuple(headerline.split(':')) for headerline in headersplit
                       if not headerline.startswith("HTTP") and headerline]
        return {"statucode":statuscode, "header_list":header_list}

    def _get_curl_object(self, urlstr, header_list, timeout, method, bodydata_json=False):
        curlobj = pycurl.Curl()
        responseheader = BytesIO()
        jsoninsdata = BytesIO()

        curlobj.setopt(curlobj.URL, urlstr.encode("UTF-8"))
        curlobj.setopt(curlobj.HTTPHEADER, header_list)
        curlobj.setopt(curlobj.HEADERFUNCTION, responseheader.write)
        curlobj.setopt(curlobj.WRITEFUNCTION, jsoninsdata.write)
        if timeout:
            curlobj.setopt(curlobj.CONNECTTIMEOUT, int(timeout))
            curlobj.setopt(curlobj.TIMEOUT, int(timeout))

        if method=="POST" and bodydata_json:
            curlobj.setopt(curlobj.POST, 1)
            curlobj.setopt(curlobj.POSTFIELDS, bodydata_json)

        if method=="PATCH" and bodydata_json:
            curlobj.setopt(curlobj.CUSTOMREQUEST, "PATCH")

        if method=="DELETE":
            curlobj.setopt(curlobj.CUSTOMREQUEST, "DELETE")

        curlobj.perform()
        curlobj.close()

        header = responseheader.getvalue()
        status_header_dict = self._responce_generate(header)

        result_value = jsoninsdata.getvalue()
        result = result_value if result_value  else ''

        return {"header": status_header_dict, "body": result}

    def _getpycurl_returndict(self, urlstr, header_list=False, timeout=False):
        self._printcurl("GET", urlstr, header_list, timeout)
        header_body_dict = self._get_curl_object(urlstr, header_list, timeout, "GET")
        response_str = header_body_dict["body"]
        try:
            header_body_dict["body"] = json.loads(response_str)
        except:
            pass

        self._printresult(header_body_dict)
        return header_body_dict

    def _postpycurl_returnstr(self, urlstr, bodydata_json, header_list, timeout=False):
        self._printcurl("POST", urlstr, header_list, bodydata_json, timeout)
        apiresult = self._get_curl_object(urlstr, header_list, timeout, "POST", bodydata_json)
        self._printresult(apiresult)
        return apiresult

    def _patchpycurl_returnstr(self, urlstr, header_list, bodydata_json, timeout=False):
        self._printcurl("PATCH", urlstr, header_list, timeout)
        apiresult = self._get_curl_object(urlstr, header_list, timeout, "PATCH", bodydata_json)
        self._printresult(apiresult)
        return apiresult

    def _putpycurl_returnstr(self, urlstr, header_list, bodydata_json, timeout=False):
        self._printcurl("PUT", urlstr, header_list, timeout)
        apiresult = self._get_curl_object(urlstr, header_list, timeout, "PUT", bodydata_json)
        self._printresult(apiresult)
        return apiresult

    def _deletepycurl_returnstr(self, urlstr, header_list, timeout=False):
        self._printcurl("DELETE", urlstr, header_list, timeout)
        apiresult = self._get_curl_object(urlstr, header_list, timeout, "DELETE")
        self._printresult(apiresult)
        return apiresult

    def _parse_arg(func):
        def inner(self, kwdarg):
            print "-----------------------------------------<execute api>-----------------------------------------"
            urlstr = kwdarg["apiurl"]
            bodydata_json = kwdarg["body"]
            header_list = kwdarg["header"]
            timeout = kwdarg["timeout"] if "timeout" in kwdarg else False
            apiresult = func(self, urlstr, bodydata_json, header_list, timeout)
            print ""
            return apiresult
        return inner

    #Please override following methods.
    @_parse_arg
    def getpycurl(self, urlstr, bodydata_json, header_list, timeout):
        apiresult = self._getpycurl_returndict(urlstr, header_list, timeout)
        return apiresult

    @_parse_arg
    def postpycurl(self, urlstr, bodydata_json, header_list, timeout):
        apiresult = self._postpycurl_returnstr(urlstr, bodydata_json, header_list, timeout)
        return apiresult

    @_parse_arg
    def deletepycurl(self, urlstr, bodydata_json, header_list, timeout):
        apiresult = self._deletepycurl_returnstr(urlstr, header_list, timeout)
        return apiresult



#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, socket
if sys.version_info.major == 3:
  from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, Request, build_opener
  from urllib.parse import urlencode
else:
  from urllib2 import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, Request, build_opener
  from urllib import urlencode

import json


socket.setdefaulttimeout(10)
VALIDATE_URL ="http://devzik.ru/db_scripts/validate.php"
#VALIDATE_URL ="http://devzik.ru/db_scripts/check.php"
#don't forget replace in syncdb.py too

def curl(url, params=None, auth=None, req_type="GET", data=None, headers=None):
  post_req = ["POST", "PUT"]
  get_req = ["GET", "DELETE"]

  if params is not None:
    url += "?" + urlencode(params)

  if req_type not in post_req + get_req:
    raise IOError("Wrong request type \"%s\" passed" % req_type)

  _headers = {}
  handler_chain = []

  if auth is not None:
    manager = HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, url, auth["user"], auth["pass"])
    handler_chain.append(HTTPBasicAuthHandler(manager))

  if req_type in post_req and data is not None:
    _headers["Content-Length"] = len(data)

  if headers is not None:
    _headers.update(headers)

  director = build_opener(*handler_chain)

  if req_type in post_req:
    if sys.version_info.major == 3:
      _data = bytes(data, encoding='utf8')
    else:
      _data = bytes(data)

    req = Request(url, headers=_headers, data=_data)
  else:
    req = Request(url, headers=_headers)

  req.get_method = lambda: req_type
  result = director.open(req)

  return {
    "httpcode": result.code,
    "headers": result.info(),
    "content": result.read()
  }


"""
Usage example:
"""

#Post data:
#try:
#ans = curl("http://devzik.ru/", req_type="POST", data='cascac')
#except:
#    print("can't get data")
#print ans['content']
#Pass arguments (http://127.0.0.1/?q=show):
#  curl("http://127.0.0.1/", params={'q': 'show'}, req_type="POST", data='cascac')

#HTTP Authorization:
#  curl("http://127.0.0.1/secure_data.txt", auth={"user": "username", "pass": "password"})


def onlinecheck(code):
    #if(checkCODE(code) == False):
    #    return(False,True)
    try:
        result = curl(VALIDATE_URL,params={"checkcode":str(code) },req_type="GET" )
        print(str(result["content"]))
        jsonstr=json.loads(str(result["content"]),"utf-8")
        print(jsonstr["valid"])
        if(jsonstr["valid"] == True):
            #print("online valid")
            valid = True
            online = True
        else:
            #print("online no valid")
            valid = False
            online = True
    except:
        valid = True
        online = False
    return (valid,online)



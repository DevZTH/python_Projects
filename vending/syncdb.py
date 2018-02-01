#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#this script update main database and must run periodicaly via crontab fo example =)
#
#######
import sys, socket
if sys.version_info.major == 3:
  from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, Request, build_opener
  from urllib.parse import urlencode
else:
  from urllib2 import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, Request, build_opener
  from urllib import urlencode

import sqlite3, time

socket.setdefaulttimeout(10)
VALIDATE_URL ="http://devzik.ru/test/validate.php"
#don't forget replace in online_Check.py too



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

def validate(code):
    try:
        result = curl(VALIDATE_URL,params={"checkcode":str(code) },req_type="GET" )
        return True
    except:
        return False

db = sqlite3.connect('usedkeys.db')
cursor = db.cursor()
cursor.execute("SELECT * FROM `ukeys` WHERE sync = 0")
rows=cursor.fetchall()
for row in rows:
    code,remain,timestamp,sync = row
    if(validate(code)):
        cursor.execute("UPDATE `ukeys` SET sync = 1 WHERE code = "+str(code) )
        db.commit()
    db.close()
        #print("UPDATE `ukeys` SET sync = 1 WHERE code = "+str(code))
    print(row)



#            cursor.execute("insert into ukeys values  (?,?,?,?);",
#            ( code,"0", int(time.time()),"0" ) )
#            db.commit()
#            db.close()

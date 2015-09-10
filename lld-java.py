#!/usr/bin/python

import sys
import json
import struct
import socket

port = sys.argv[1]
keys = sys.argv[2]

JavaGateway = ('172.17.42.1', 10052)

common  = {
  "request":  "java gateway jmx",
  "conn":     "192.168.1.83",
  "username": None,
  "password": None,
}

jmxs = {
    "uptime"  : "jmx[java.lang:type=Runtime,Uptime]",
    "maxfd"   : "jmx[java.lang:type=OperatingSystem,MaxFileDescriptorCount]",
    "openfd"  : "jmx[java.lang:type=OperatingSystem,OpenFileDescriptorCount]",
    "version" : "jmx[java.lang:type=Runtime,VmVersion]",
    "ThreadCount"       : "jmx[java.lang:type=Threading,ThreadCount]",
    "PeakThreadCount"   : "jmx[java.lang:type=Threading,PeakThreadCount]",
    "DaemonThreadCount" : "jmx[java.lang:type=Threading,DaemonThreadCount]",
    }

common["keys"] = [ jmxs[keys] ]
common["port"] = port

queries = json.dumps(common)

header = 'ZBXD\1'
length = struct.pack('<8B', len(queries),0,0,0,0,0,0,0)

s = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(JavaGateway)

if s is None:
    print 'could not open socket'
    sys.exit(1)

s.send(header)
s.send(length)
s.send(queries)

data = s.recv(5)
data = s.recv(8)
data = s.recv(1024)
s.close()

value = json.loads(data)
print repr(value)
value = value["data"][0]

print value.get("value")

#!/usr/bin/python

import sys  
import json
import struct
import socket  
  
HOST = "172.17.42.1"
PORT = "10052"

s=None  
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    s = socket.socket(af, socktype, proto)
    s.connect(sa)
    break

if s is None:  
    print 'could not open socket'  
    sys.exit(1)  

header = 'ZBXD\1'
data   = '{"request": "java gateway internal", "keys":[\"zabbix[java,,version]\"]}'

send   = json.loads(data)
send2  = json.dumps(send)

length = struct.pack('<8B', len(send2),0,0,0,0,0,0,0)

s.send(header)
s.send(length)
s.send(send2)

data = s.recv(5)
data = s.recv(8)
data = s.recv(1024)
s.close()  
print repr(data)

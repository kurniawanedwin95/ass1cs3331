#!usr/bin/python

#socket implementation
import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '' #local
receiver_port = sys.arg[1]

s.bind((host, port))
print 'server is waiting for UDP connection'
while 1:
  message, client = s.recvfrom(2048)
  ACK = #something
  s.sendto(ACK, client)
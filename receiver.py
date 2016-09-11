#!usr/bin/python

#socket implementation
import socket
import struct
import sys


head = struct.Struct('? ? I I')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '' #local
receiver_port = int(sys.argv[1])

s.bind((host, receiver_port))
print 'server is waiting for UDP connection'
while 1:
  message, client = s.recvfrom(1024) #buffer size 1kb
  #connection received
  header = head.unpack(message)
  print header
  #might need an if statement here
  if(header[0] == True and header[1] == False):
    SYN = True
    ACK = True
    seq_num = header[2]+1
    ack_num = 1
    header = head.pack(SYN, ACK, seq_num, ack_num)
    s.sendto(header, client)
    print 'SYN+ACK packet sent'
  message, client = s.recvfrom(1024)
  header = head.unpack(message)
  if(header[0] == False and header[1] == True):
    print 'ACK Received'
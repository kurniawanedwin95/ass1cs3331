#!usr/bin/python

import socket
import struct
import sys
import time

#Main Function
#might comment them first, then add as more are implemented
receiver_host_ip = sys.argv[1]
receiver_port = int(sys.argv[2])
# f = sys.arg[3]
# MSS = sys.arg[4]
# timeout = sys.arg[5]
# pdrop = sys.arg[6]
# seed = sys.arg[7]
head = struct.Struct('? ? I I')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
  #first we will simulate a TCP header and make it available in all our UDP packets
  SYN = True
  ACK = False
  seq_num = 1#some randomly generated value
  ack_num = 0
  message = 'testin dis crap'
  header = head.pack(SYN,ACK,seq_num,ack_num)
  s.sendto(header,(receiver_host_ip, receiver_port)) #sends SYN
  print 'SYN packet sent'
  message, client = s.recvfrom(1024) #reads reply
  print 'SYN+ACK received'
  header = head.unpack(message)
  print header
  if(header[0] == True and header[1] == True):
    SYN = False
    ACK = True
    seq_num = header[2]+1
    ack_num = header[3]
    header = head.pack(SYN, ACK, seq_num, ack_num)
    s.sendto(header,(receiver_host_ip, receiver_port)) #sends ACK
    print 'ACK packet sent'
#handshakes
except socket.error:
  print 'Could not connect to server, terminating program.\n'
    
    

    

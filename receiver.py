#!usr/bin/python

#socket implementation
import socket
import pickle
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '' #local
receiver_port = int(sys.argv[1])

s.bind((host, receiver_port))
print 'server is waiting for UDP connection'
while 1:
  message, client = s.recvfrom(1024) #buffer size 1kb
  #connection received
  message = pickle.loads(message)
  print message
  #might need an if statement here
  if(message['SYN'] == True and message['ACK'] == False):
    value = {'SYN':True,'ACK':True,'seq_num':message['seq_num']+1,'ack_num':1}
    message = pickle.dumps(value)
    s.sendto(message, client)
    print 'SYN+ACK packet sent'
    
  message, client = s.recvfrom(1024)
  message = pickle.loads(message)
  if(message['SYN'] == False and message['ACK'] == True):
    print 'ACK Received'
    exit
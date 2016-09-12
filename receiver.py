#!usr/bin/python

#socket implementation
import socket
import pickle
import sys

def readAndResponse(message,client):
  if(message['SYN'] == True and message['ACK'] == False):
    print 'SYN received'
    print message
    value = {'SYN':True,'ACK':True,'seq_num':message['seq_num']+1,'ack_num':1}
    message = pickle.dumps(value)
    s.sendto(message, client)
    print 'SYN+ACK packet sent'
  
  elif(message['SYN'] == False and message['ACK'] == True):
    print 'ACK Received'
    print message
    
  else:
    print 'Something wrong somewhere'


if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  host = '' #local
  receiver_port = int(sys.argv[1])
  s.bind((host, receiver_port))
  print 'server is waiting for UDP connection'
  
  while 1:
    message, client = s.recvfrom(1024) #buffer size 1kb
    message = pickle.loads(message)
    readAndResponse(message,client)

  
#!usr/bin/python

import socket
import pickle
import random
import sys
import time
#implement connection termination and timeout next


if __name__ == '__main__':#might comment them first, then add as more are implemented
  receiver_host_ip = sys.argv[1]
  receiver_port = int(sys.argv[2])
  f = open(sys.argv[3],'r') #use read() to read, argument is number of chars
  MSS = int(sys.argv[4])
  # timeout = int(sys.argv[5])
  # pdrop = int(sys.argv[6])
  # seed = int(sys.argv[7])
  cwnd = 1
  # ssthresh = MSS #initial ssthresh value
  
  
  #UDP packet structure SYN, ACK, FIN, seq_num, ack_num, data, mss
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    #3 Way Handshake
    value = {'SYN':True,'ACK':False,'FIN':False,'seq_num':1,'ack_num':0,'data':'','mss':MSS}
    message = pickle.dumps(value)
    s.sendto(message,(receiver_host_ip, receiver_port)) #sends SYN
    print 'SYN packet sent'
    message, client = s.recvfrom(1024) #reads SYN+ACK
    message = pickle.loads(message)
    print 'SYN+ACK received'
    print message
    if(message['SYN'] == True and message['ACK'] == True):
      value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':message['seq_num'],'data':'','mss':MSS}
      message = pickle.dumps(value)
      s.sendto(message,(receiver_host_ip, receiver_port)) #sends ACK
      print 'ACK packet sent'
      message = pickle.loads(message)
      
    #send message here
    while 1:
      chunk = f.read(MSS)
      if chunk == '':
        print 'EOF reached'
        break
      value = {'SYN':True,'ACK':False,'FIN':False,'seq_num':message['ack_num'],'ack_num':message['seq_num'],'data':chunk,'mss':MSS}
      message = pickle.dumps(value)
      s.sendto(message,(receiver_host_ip,receiver_port))
      print 'SYN+Data packet sent'
      message,client = s.recvfrom(1024)
      message = pickle.loads(message)
      if(message['SYN'] == False and message['ack_num'] == value['seq_num']+1):
        print 'Packet successfully ACKed'
    ###
  
    #3 Way FIN
    value = {'SYN':False,'ACK':False,'FIN':True,'seq_num':message['seq_num']+1,'ack_num':message['ack_num']+1, 'data':'','mss':MSS}
    message = pickle.dumps(value)
    s.sendto(message,(receiver_host_ip,receiver_port))
    print 'FIN packet sent'
    message, client = s.recvfrom(1024) #reads SYN+ACK
    message = pickle.loads(message)
    if(message['FIN'] == True and message['ACK'] == True):
      print 'FIN+ACK received'
      print 'Terminating connection'
      s.close()
      f.close()
      print 'Connection terminated'
    
  except socket.error:
    print 'Could not connect to server, terminating program.\n'
      
      
  
      

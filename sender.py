#!usr/bin/python

import socket
import pickle
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
cwnd = 1
# ssthresh = MSS #initial ssthresh value

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
  #first we will simulate a TCP header and make it available in all our UDP packets
  value = {'SYN':True, 'ACK':False, 'seq_num':1, 'ack_num':0, 'data':''} #seq shud be RNG
  message = pickle.dumps(value)
  s.sendto(message,(receiver_host_ip, receiver_port)) #sends SYN
  print 'SYN packet sent'
  
  message, client = s.recvfrom(1024) #reads SYN+ACK
  message = pickle.loads(message)
  print 'SYN+ACK received'
  print message
  if(message['SYN'] == True and message['ACK'] == True):
    value = {'SYN':False, 'ACK':True, 'seq_num':message['seq_num']+1, 'ack_num':message['ack_num']}
    message = pickle.dumps(value)
    s.sendto(message,(receiver_host_ip, receiver_port)) #sends ACK
    print 'ACK packet sent'

except socket.error:
  print 'Could not connect to server, terminating program.\n'
    
    

    

#!usr/bin/python

import socket
import pickle
import random
import sys
import time
#implement retransmit

def beginConnection(s,receiver_host_ip,receiver_port):
  
  #3 Way Handshake
  value = {'SYN':True,'ACK':False,'FIN':False,'seq_num':random.randint(0,10000),'ack_num':0,'data':'','mss':MSS}
  message = pickle.dumps(value)
  s.sendto(message,(receiver_host_ip, receiver_port)) #sends SYN
  print 'SYN packet sent'
  message, client = s.recvfrom(1024) #reads SYN+ACK
  message = pickle.loads(message)
  print 'SYN+ACK received'
  print message
  if(message['SYN'] == True and message['ACK'] == True):
    value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':message['seq_num']+1,'data':''}
    message = pickle.dumps(value)
    s.sendto(message,(receiver_host_ip, receiver_port)) #sends ACK
    print 'ACK packet sent'
    message = pickle.loads(message)
    return message

def endConnection(s,message,receiver_host_ip,receiver_port):
  #3 Way FIN
  value = {'SYN':False,'ACK':False,'FIN':True,'seq_num':message['seq_num'],'ack_num':message['ack_num']+1, 'data':''}
  message = pickle.dumps(value)
  s.sendto(message,(receiver_host_ip,receiver_port))
  print 'FIN packet sent'
  message, client = s.recvfrom(1024) #reads SYN+ACK
  message = pickle.loads(message)
  if(message['FIN'] == True and message['ACK'] == True):
    print 'FIN+ACK received'
    value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':message['seq_num']+1}
    message = pickle.dumps(value)
    s.sendto(message,(receiver_host_ip,receiver_port))
    print 'ACK packet sent, terminating connection'
    s.close()
    f.close()
    print 'Connection terminated'


if __name__ == '__main__':#might comment them first, then add as more are implemented
  receiver_host_ip = sys.argv[1]
  receiver_port = int(sys.argv[2])
  f = open(sys.argv[3],'r') #use read() to read, argument is number of chars
  MSS = int(sys.argv[4])
  MWS = MSS
  timeout = int(sys.argv[5])
  pdrop = float(sys.argv[6])
  seed = int(sys.argv[7])

  cwnd = 1
  # ssthresh = MSS #initial ssthresh value
  message = '' #initialise message
  EOFFlag = False
  finalACK = False
  random.seed(seed)
  #UDP packet structure SYN, ACK, FIN, seq_num, ack_num, data
  
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    #3way handshake
    message = beginConnection(s,receiver_host_ip,receiver_port)
    
    message['seq_num'] -= MSS #initiate correct seq_num
    print message['seq_num']
    #use deque, first in first out for MWS implementation(perhaps)
    #send message here
    while 1:
      sent = 0
      ##data reading module---------------------------------------------
      for i in range(0,MWS):
        if EOFFlag == False:
          chunk = f.read(MSS)
          
          if chunk == '':
            #reached EOF
            print 'EOF reached'
            EOFFlag = True
            break
          ##-------------------------------------------------------------
          
          ##data sending module------------------------------------------
          value = {'SYN':True,'ACK':False,'FIN':False,'seq_num':message['seq_num']+MSS,'ack_num':message['seq_num'],'data':chunk}
          print value['seq_num']
          message = pickle.dumps(value)
          
          if random.random() > pdrop:
            s.sendto(message,(receiver_host_ip,receiver_port))
            sent += 1
            print 'SYN+Data packet sent'
          else:
            print 'packet dropped'
          message = pickle.loads(message)
          ##--------------------------------------------------------------
          
        else:
          break
      
      if (EOFFlag == True and finalACK == True):
        break
      
      for k in range(0,sent):
        #checks acks with the same amount of undropped packets
        rec_message,client = s.recvfrom(1024)
        rec_message = pickle.loads(rec_message)
      
      #final data handling
      diff = sent-len(value['data'])
      sent = sent-diff
      
      if(rec_message['ACK'] == True and rec_message['ack_num'] == value['seq_num']+sent):
        print 'Packet successfully ACKed'
        if EOFFlag == True:
          message['seq_num'] = rec_message['ack_num']
          finalACK = True

    ###
    #3way fin
    endConnection(s,message,receiver_host_ip,receiver_port)

    
  except socket.error:
    print 'Could not connect to server, terminating program.\n'
      
      
  
      

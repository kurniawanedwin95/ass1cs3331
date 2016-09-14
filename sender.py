#!usr/bin/python

import socket
import pickle
import random
import sys
import time
#implement retransmit

def beginConnection(log,starttime,s,receiver_host_ip,receiver_port):
  
  #3 Way Handshake
  # value = {'SYN':True,'ACK':False,'FIN':False,'seq_num':random.randint(0,10000),'ack_num':0,'data':'','mss':MSS,'end_seq_num':0}
  value = {'SYN':True,'ACK':False,'FIN':False,'seq_num':0,'ack_num':0,'data':'','mss':MSS,'end_seq_num':0} #debug mode
  message = pickle.dumps(value)
  s.sendto(message,(receiver_host_ip, receiver_port)) #sends SYN
  #log writing chunk--------------------------------------------
  curtime = time.time()*1000
  curtime = curtime-starttime
  string = 'snd\t'+str(curtime)+'\tS\t'+str(value['seq_num'])+'\t'+str(len(value['data']))+'\t'+str(value['ack_num'])+'\n'
  log.write(string)
  #-------------------------------------------------------------
  print 'SYN packet sent'
  message, client = s.recvfrom(1024) #reads SYN+ACK
  message = pickle.loads(message)
  #log writing chunk--------------------------------------------
  curtime = time.time()*1000
  curtime = curtime-starttime
  string = 'rcv\t'+str(curtime)+'\tSA\t'+str(message['seq_num'])+'\t'+str(len(message['data']))+'\t'+str(message['ack_num'])+'\n'
  log.write(string)
  #-------------------------------------------------------------
  print 'SYN+ACK received'
  print message
  if(message['SYN'] == True and message['ACK'] == True):
    value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':message['seq_num']+1,'data':'','end_seq_num':0}
    message = pickle.dumps(value)
    s.sendto(message,(receiver_host_ip, receiver_port)) #sends ACK
    #log writing chunk--------------------------------------------
    curtime = time.time()*1000
    curtime = curtime-starttime
    string = 'snd\t'+str(curtime)+'\tA\t'+str(value['seq_num'])+'\t'+str(len(value['data']))+'\t'+str(value['ack_num'])+'\n'
    log.write(string)
    #-------------------------------------------------------------
    print 'ACK packet sent'
    message = pickle.loads(message)
    return message
    
def fileRead(seq_num,MSS,f):
  EOFFlag = False
  size = 0
  while EOFFlag == False:
    chunk = f.read(MSS)
    size += len(chunk)
    if chunk == '':
      #reached EOF
      print 'EOF reached'
      EOFFlag = True
      break
    data[seq_num] = chunk
    seq_num += MSS
  return data, size

def endConnection(log,starttime,s,message,receiver_host_ip,receiver_port):
  #3 Way FIN
  value = {'SYN':False,'ACK':False,'FIN':True,'seq_num':message['seq_num'],'ack_num':message['ack_num'], 'data':'','end_seq_num':0}
  message = pickle.dumps(value)
  s.sendto(message,(receiver_host_ip,receiver_port))
  #log writing chunk--------------------------------------------
  curtime = time.time()*1000
  curtime = curtime-starttime
  string = 'snd\t'+str(curtime)+'\tF\t'+str(value['seq_num'])+'\t'+str(len(value['data']))+'\t'+str(value['ack_num'])+'\n'
  log.write(string)
  #-------------------------------------------------------------
  print 'FIN packet sent',value['seq_num'], value['ack_num']
  message, client = s.recvfrom(1024) #reads SYN+ACK
  message = pickle.loads(message)
  if(message['FIN'] == True and message['ACK'] == True):
    #log writing chunk--------------------------------------------
    curtime = time.time()*1000
    curtime = curtime-starttime
    string = 'rcv\t'+str(curtime)+'\tFA\t'+str(message['seq_num'])+'\t'+str(len(message['data']))+'\t'+str(message['ack_num'])+'\n'
    log.write(string)
    #-------------------------------------------------------------
    print 'FIN+ACK received'
    value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':message['seq_num']+1,'data':'','end_seq_num':0}
    message = pickle.dumps(value)
    s.sendto(message,(receiver_host_ip,receiver_port))
    #log writing chunk--------------------------------------------
    curtime = time.time()*1000
    curtime = curtime-starttime
    string = 'snd\t'+str(curtime)+'\tA\t'+str(value['seq_num'])+'\t'+str(len(value['data']))+'\t'+str(value['ack_num'])+'\n'
    log.write(string)
    #-------------------------------------------------------------
    print 'ACK packet sent, terminating connection'
    s.close()
    f.close()
    print 'Connection terminated'


if __name__ == '__main__':#might comment them first, then add as more are implemented
  starttime = time.time()*1000
  #arg reading chunk
  receiver_host_ip = sys.argv[1]
  receiver_port = int(sys.argv[2])
  f = open(sys.argv[3],'r') #use read() to read, argument is number of chars
  MSS = int(sys.argv[4])
  MWS = MSS
  timeout = int(sys.argv[5])
  pdrop = float(sys.argv[6])
  seed = int(sys.argv[7])
  
  #initialization chunk
  message = '' #initialise message
  EOFFlag = False
  finalACK = False
  goToFin = False
  data = {}
  allSent = False
  log = open('log.txt','w')#cleans file of previous content
  log.close()
  log = open('log.txt','a')
  random.seed(seed)
  #UDP packet structure SYN, ACK, FIN, seq_num, ack_num, data, end_seq_num
  
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    #3way handshake
    message = beginConnection(log,starttime,s,receiver_host_ip,receiver_port)
    
    #initiate correct seq_num
    start_seq_num = message['seq_num']
    sender_ack_num = message['ack_num']
    print message['seq_num']

    #send message here
    while goToFin == False:
      sent = 0
      firstSent = False
      ##data reading module------------------------------------------
      if EOFFlag == False:
        data, size = fileRead(start_seq_num,MSS,f)
        print data
        end_seq_num = size+start_seq_num
        print end_seq_num
        EOFFlag = True
      ##-------------------------------------------------------------
      
      ##data sending module------------------------------------------
      for i in range(0,MWS):#this is basically the window
        multiplier = i*MSS
        sequence = start_seq_num+multiplier
        
        if sequence < end_seq_num and allSent == False:
          value = {'SYN':True,'ACK':False,'FIN':False,'seq_num':sequence,'ack_num':sender_ack_num,'data':data[sequence],'end_seq_num':end_seq_num}
          message = pickle.dumps(value)
          
          if random.random() > pdrop:
            if i == 0:
              firstSent = True
            s.sendto(message,(receiver_host_ip,receiver_port))
            sent += 1
            #log writing chunk--------------------------------------------
            curtime = time.time()*1000
            curtime = curtime-starttime
            string = 'snd\t'+str(curtime)+'\tD\t'+str(value['seq_num'])+'\t'+str(len(value['data']))+'\t'+str(value['ack_num'])+'\n'
            log.write(string)
            #-------------------------------------------------------------
            print 'SYN+Data packet sent, seq_num is:',value['seq_num']
          else:
            if i == 0:
              firstSent = False
            #PLD module in action
            #log writing chunk--------------------------------------------
            curtime = time.time()*1000
            curtime = curtime-starttime
            string = 'drop\t'+str(curtime)+'\tD\t'+str(value['seq_num'])+'\t'+str(len(value['data']))+'\t'+str(value['ack_num'])+'\n'
            log.write(string)
            #-------------------------------------------------------------
            print 'packet dropped, seq_num is:',value['seq_num']
          message = pickle.loads(message)
          
        else:
          print 'all packet sent'
          allSent = True
          break
      ##--------------------------------------------------------------
      
      ##ACK checking module-------------------------------------------
      for j in range(0,sent):
        #checks acks with the same amount of undropped packets
        rec_message,client = s.recvfrom(1024)
        rec_message = pickle.loads(rec_message)
        #log writing chunk--------------------------------------------
        curtime = time.time()*1000
        curtime = curtime-starttime
        string = 'rcv\t'+str(curtime)+'\tA\t'+str(rec_message['seq_num'])+'\t'+str(len(rec_message['data']))+'\t'+str(rec_message['ack_num'])+'\n'
        log.write(string)
        #-------------------------------------------------------------
        #final data handling
        if allSent == True:
          print rec_message
        if rec_message['ack_num'] == end_seq_num:
          diff = sent-len(value['data'])
          final_size = sent-diff
        else:
          final_size = MSS
        
        print rec_message['ack_num']
        print start_seq_num+final_size
        if (rec_message['ACK'] == True and rec_message['ack_num'] == (start_seq_num+final_size) and rec_message['ack_num'] < end_seq_num and firstSent == True):
          print 'packet',start_seq_num,'successfully ACKed'
          start_seq_num += final_size
          print 'start_seq_num updated to:',start_seq_num
        ##final packet
        elif (rec_message['ACK'] == True and rec_message['ack_num'] == (start_seq_num+final_size) and rec_message['ack_num'] == end_seq_num and firstSent == True):
          print 'final packet',start_seq_num,'successfully ACKed'
          start_seq_num += final_size
          print 'start_seq_num updated to:',start_seq_num
          goToFin = True
          break
        else:
          print 'this leads to retransmit'
          #retransmit
      ##--------------------------------------------------------------------
    
    message['seq_num'] = start_seq_num
    #3way fin
    endConnection(log,starttime,s,message,receiver_host_ip,receiver_port)

    
  except socket.error:
    print 'Could not connect to server, terminating program.\n'
      
      
  
      
